# -*- coding: utf-8 -*-
import asyncio
import json
import ssl
from typing import Tuple

import aiohttp
from aiohttp import ContentTypeError

from .accountgroup import AccountGroup
from .accounts import Account
from .applications import Applications
from .config import Config
from .exceptions import CyberarkException, GetTokenException, AiobastionException, CyberarkAPIException, \
    ChallengeResponseException
from .platforms import Platform
from .safe import Safe
from .system_health import SystemHealth
from .users import User, Group
from .utilities import Utilities


class EPV:
    """
    Class that represent the connection, or future connection, to the Vault.
    """
    def __init__(self, configfile: str = None, serialized: dict = None, token: str = None):
        if configfile is None and serialized is None:
            raise AiobastionException("You must provide either configfile or serialized to init EPV")
        if configfile is not None and serialized is not None:
            raise AiobastionException("You must provide either configfile or serialized to init EPV, not both")
        if configfile is not None:
            self.config = Config(configfile)

            if self.config.PVWA_CA is not False:
                self.request_params = {"timeout": self.config.timeout,
                                       "ssl": ssl.create_default_context(cafile=self.config.PVWA_CA)}
            else:
                self.request_params = {"timeout": self.config.timeout, "ssl": False}

            self.api_host = self.config.PVWA
            self.authtype = self.config.authtype
            self.cpm = self.config.CPM
            self.retention = self.config.retention
            self.max_concurrent_tasks = self.config.max_concurrent_tasks
            self.__token = token

        if serialized is not None:
            if "verify" in serialized:
                if serialized["verify"] is not False:
                    self.request_params = {"timeout": serialized["timeout"],
                                           "ssl": ssl.create_default_context(cafile=serialized["verify"])}
                else:
                    self.request_params = {"timeout": serialized["timeout"], "ssl": False}
            else:
                self.request_params = {"timeout": 20, "ssl": False}

            self.api_host = serialized['api_host']

            if "authtype" in serialized:
                self.authtype = serialized["authtype"]
            else:
                self.authtype = None

            if "cpm" in serialized:
                self.cpm = serialized['cpm']
            else:
                self.cpm = ""
            if "retention" in serialized:
                self.retention = serialized['retention']
            else:
                self.retention = 10
            if "max_concurrent_tasks" in serialized:
                self.max_concurrent_tasks = serialized['max_concurrent_tasks']
            else:
                self.max_concurrent_tasks = 10
            if "token" in serialized:
                self.__token = serialized['token']
            else:
                self.__token = None

        # self.session = requests.Session()

        self.user_list = None

        # Session management
        self.session = None
        self.__sema = None

        # utilities
        self.account = Account(self)
        self.platform = Platform(self)
        self.safe = Safe(self)
        self.user = User(self)
        self.group = Group(self)
        self.application = Applications(self)
        self.accountgroup = AccountGroup(self)
        self.system_health = SystemHealth(self)
        self.utils = Utilities(self)

    # Context manager
    async def __aenter__(self):
        await self.login()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return await self.close_session()

    # start of functions definition
    async def __login_cyberark(self, username: str, password: str, auth_type: str) -> str:
        assert self.__token is None
        assert auth_type.upper() in ("CYBERARK", "WINDOWS", "LDAP", "RADIUS")
        url, head = self.get_url("API/Auth/" + auth_type + "/Logon")
        request_data = {"username": username, "password": password, "concurrentSession": True}
        try:
            session = self.get_session()
            async with session.post(url, json=request_data, **self.request_params) as req:
                if req.status != 200:
                    try:
                        error = await req.text()
                    except Exception as err:
                        error = f"Unable to get error message {err}"
                    if req.status == 403:
                        raise CyberarkException("Invalid credentials ! ")
                    elif req.status == 409:
                        raise CyberarkException("Password expired !")
                    elif req.status == 500 and "ITATS542I" in error:
                        raise ChallengeResponseException
                    else:
                        raise CyberarkException(error)

                tok = await req.text()
                # Closing session because now we are connected and we need to update headers which can be done
                # only by recreating a new session (or passing the headers on each request)
                await session.close()
                return tok.replace('"', '')

            # Cleaning password after authentication
            self.__password = ""
        except ChallengeResponseException:
            raise
        except (ConnectionError, TimeoutError):
            raise CyberarkException("Network problem connecting to PVWA")
        except Exception as err:
            raise CyberarkException(err)

    async def logoff(self):
        url, head = self.get_url("API/Auth/Logoff")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=head, **self.request_params) as req:
                if req.status != 200:
                    raise CyberarkException("Error disconnecting to PVWA with code : %s" % str(req.status))
        await self.close_session()
        self.__token = None
        return True

    async def check_token(self) -> bool or None:
        if self.__token is None:
            return None

        try:
            await self.handle_request("get", "api/LoginsInfo")
            return True
        except CyberarkException:
            return False
        # url, head = self.get_url("api/LoginsInfo")
        # session = self.get_session()
        # # async with aiohttp.ClientSession() as session:
        # async with session.get(url, headers=head, **self.request_params) as req:
        #     if req.status != 200:
        #         self.__token = None
        #         return False
        #     return True

    async def get_aim_secret(self, aim_host, appid, username, cert_file: str, cert_key: str, ca_file):
        if appid is None:
            raise AiobastionException("Missing mandatory parameter : AppID")

        if cert_file is None and cert_key is None:
            raise AiobastionException("Provide cert_file and cert_key arguments in order to connect")

        try:

            url = f"https://{aim_host}/AIMWebService/api/Accounts"
            data = {
                "AppId": appid,
                "Username": username
            }

            if ca_file is not False:
                sslcontext = ssl.create_default_context(cafile=ca_file)
                sslcontext.load_cert_chain(cert_file, cert_key)
            else:
                sslcontext = ssl.create_default_context()
                sslcontext.load_cert_chain(cert_file, cert_key)

            req_params = {"timeout": self.config.timeout, "ssl": sslcontext}

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=data, **req_params) as req:
                    result = await req.json()

            if "ErrorCode" in result:
                raise CyberarkException(f"AIM Request failed : {result}")

            return result["Content"]

        except Exception:
            raise

    async def login_with_aim(self, aim_host, appid, username, cert_file: str, cert_key: str, root_ca=False):
        if self.check_token():
            return
        password = await self.get_aim_secret(aim_host, appid, username, cert_file, cert_key, root_ca)

        try:
            self.__token = self.__login_cyberark(username, password, self.config.authtype)
        except CyberarkException as err:
            raise GetTokenException(err)

    async def login(self, username=None, password=None, auth_type=""):
        if await self.check_token():
            return

        if username is None:
            if self.config.username is None:
                raise AiobastionException("Username must be provided on login call or in configuration file")
            username = self.config.username
        if password is None:
            if self.config.password is None:
                if self.config.AIM is not None:
                    if self.config.AIM:
                        # All infos regarding AIM auth were given in the configuration file
                        password = await self.get_aim_secret(self.config.AIM_HOST, self.config.AIM_AppID, username,
                                                             self.config.AIM_Cert, self.config.AIM_Key,
                                                             self.config.AIM_CA)
                    else:
                        raise AiobastionException(
                            "Missing AIM information to perform AIM authentication, see documentation")
                else:
                    raise AiobastionException("Password must be provided on login call or in configuration file")
            else:
                password = self.config.password

        if auth_type == "":
            if self.authtype is not None:
                auth_type = self.authtype
            else:
                auth_type = "Cyberark"


        try:
            self.__token = await self.__login_cyberark(username, password, auth_type)
            # head = {'Content-type': 'application/json',
            #         'Authorization': self.__token}

            # update the session
            await self.close_session()
            # self.session = aiohttp.ClientSession(headers=head)
        except ChallengeResponseException:
            # User should enter passcode now
            raise

        except CyberarkException as err:
            raise GetTokenException(err)

    def get_session(self):
        if self.__token is None and self.session is None:
            head = {"Content-type": "application/json", "Authorization": "None"}
            self.session = aiohttp.ClientSession(headers=head)
        elif self.__token is None and self.session is not None:
            # This should never happen
            return self.session
        elif self.session is None:
            head = {'Content-type': 'application/json',
                    'Authorization': self.__token}
            self.session = aiohttp.ClientSession(headers=head)
        elif self.session.closed:
            # This should never happen, but it's a security in case of unhandled exceptions
            head = {'Content-type': 'application/json',
                    'Authorization': self.__token}
            self.session = aiohttp.ClientSession(headers=head)

        if self.__sema is None:
            self.__sema = asyncio.Semaphore(self.max_concurrent_tasks)
        return self.session

    async def close_session(self):
        try:
            await self.session.close()
        except (CyberarkException, AttributeError):
            pass
        self.session = None
        self.__sema = None

    def get_url(self, url) -> Tuple[str, dict]:
        addr = 'https://' + self.api_host + '/PasswordVault/' + url
        if self.__token is None:
            head = {"Content-type": "application/json", "Authorization": "None"}
        else:
            head = {'Content-type': 'application/json',
                    'Authorization': self.__token}

        return addr, head

    def to_json(self):
        serialized = {
            "api_host": self.config.PVWA,
            "authtype": self.config.authtype,
            "timeout": self.config.timeout,
            "verify": self.config.PVWA_CA,
            "cpm": self.config.CPM,
            "retention": self.config.retention,
            "max_concurrent_tasks": self.config.max_concurrent_tasks,
            "token": self.__token,
        }
        return serialized

    async def get_version(self):
        server_infos = await self.handle_request("GET", "WebServices/PIMServices.svc/Server",
                                                 filter_func=lambda x: x["ExternalVersion"])
        return server_infos

    def versiontuple(self, v):
        return tuple(map(int, (v.split("."))))

    async def handle_request(self, method: str, short_url: str, data=None, params: dict = None,
                             filter_func=lambda x: x):
        """
        Function that handles requests to the API
        :param filter_func:
        :param params:
        :param method:
        :param short_url: piece of URL after PasswordVault/
        :param data: valid json data if needed
        :return:
        """
        assert method.lower() in ("post", "delete", "get", "patch")

        url, head = self.get_url(short_url)

        session = self.get_session()

        async with self.__sema:
            async with session.request(method, url, json=data, params=params, **self.request_params) as req:
                if req.status in (200, 201, 204):
                    try:
                        if len(await req.read()) == 0:
                            return True
                        else:
                            return filter_func(await req.json())
                        # return filter_func(await req.json())
                    except ContentTypeError:
                        response = await req.text()
                        try:
                            return json.loads(response)
                        except (ContentTypeError, json.decoder.JSONDecodeError):
                            if len(response) > 0:
                                return response
                            else:
                                return True
                        except:
                            raise
                else:
                    if req.status == 404:
                        raise CyberarkException(f"404 error with URL {url}")
                    elif req.status == 401:
                        raise CyberarkException(f"You are not logged, you need to login first")
                    elif req.status == 405:
                        raise CyberarkException("Your PVWA version does not support this function")
                    try:
                        content = await req.json(content_type=None)
                    except (KeyError, ValueError, ContentTypeError):
                        raise CyberarkException(f"Error with Cyberark status code {str(req.status)}")

                    if "Details" in content:
                        details = content["Details"]
                    else:
                        details = ""
                    if "ErrorCode" in content and "ErrorMessage" in content:
                        raise CyberarkAPIException(req.status, content["ErrorCode"], content["ErrorMessage"], details)
                    else:
                        raise CyberarkAPIException(req.status, "NO_ERR_CODE", content)
            # except Exception as err:
            #     raise CyberarkException(err)
