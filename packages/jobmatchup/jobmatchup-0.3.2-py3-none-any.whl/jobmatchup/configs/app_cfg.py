import logging
from os import getenv
from dataclasses import dataclass, field
from typing import Any

from jobmatchup.entity.api import AuthInfo, AppInfo, TokenInfo

from pydantic import ValidationError


__all__ = ["Config"]


@dataclass
class Config:
    """
    Config.
    """

    without_auth: bool = True

    cfg_file_path: str = None

    login_pass_auth: bool = False

    from_env: bool = False
    from_json: bool = False
    from_toml: bool = False

    auth_info: AuthInfo | None = field(repr=False, init=False)
    app_info: AppInfo | None = field(repr=False, init=False)

    token_info: TokenInfo = field(repr=False, init=False)

    def __post_init__(self):
        self._set_auth_values()

    def _set_auth_values(self):
        if not self.without_auth:
            try:
                self._load_app_info()
                self._load_auth_info()

                if not self.login_pass_auth:
                    self._load_token()
                else:
                    self._set_new_token()
            except ValidationError:
                logging.fatal("! ENV's not found !")

    def _load_token(self):
        self.token_info = TokenInfo(
            token=getenv("SJ_TOKEN"),
            refresh_token=getenv("SJ_REFRESH_TOKEN"),
            expires_in=getenv("SJ_EXPIRES_IN"),
        )

    def _load_app_info(self):
        self.app_info = AppInfo(
            app_id=getenv("SJ_APP_ID"),
            secret_key=getenv("SJ_SECRET_KEY"),
        )

    def _load_auth_info(self) -> None:
        self.auth_info = AuthInfo(
            login=getenv("SJ_LOGIN"),
            password=getenv("SJ_PASSWORD"),
        )

    def _load_cfg_from_toml(self) -> dict[str, Any]:
        from tomllib import load as load_toml

        # Read .toml file
        with open(self.cfg_file_path, "rb") as f:
            data = load_toml(f)

        return data

    def _set_cfg_var_from_toml(self):
        data: dict[str, Any] = self._load_cfg_from_toml()
        self.auth_info, self.app_info = AuthInfo(**data), AppInfo(**data)

    def _get_new_token(self) -> TokenInfo:
        """
        Obtaining a token and info to change it.
        :return: token, refresh token and expire time (sec)
        """
        from urllib import request
        from json import loads as json_loads

        url_auth = "{}/oauth2/password/?login={}&password={}&client_id={}&client_secret={}".format(
            "https://api.superjob.ru/2.0",
            self.auth_info.login,
            self.auth_info.password,
            self.app_info.app_id,
            self.app_info.secret_key,
        )

        with request.urlopen(url_auth) as url:
            data: dict[str, str | int] = json_loads(url.read().decode())

        return TokenInfo.parse_obj(
            [
                data["access_token"],
                data["refresh_token"],
                data["expires_in"],
            ]
        )

    def _set_new_token(self):
        self.token_info = self._get_new_token()
