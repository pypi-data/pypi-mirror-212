from enum import Enum
from typing import List, Optional
from uuid import uuid4

import dash_bootstrap_components as dbc
from pydantic import BaseSettings, SecretStr, validator


class DashSettings(BaseSettings):
    HTTP_HOST: str = "127.0.0.1"
    HTTP_PORT: str = "8050"
    DBC_THEME: str = "SKETCHY"
    DEBUG: bool = False

    APP_SECRET_KEY: SecretStr = SecretStr(uuid4().hex)

    AUTH0_CLIENT_ID: Optional[str] = None
    AUTH0_CLIENT_SECRET: Optional[SecretStr] = None
    AUTH0_DOMAIN: Optional[str] = None
    AUTH0_LOGIN_PATH: str = "/login"
    AUTH0_LOGOUT_PATH: str = "/logout"
    AUTH0_CALLBACK_PATH: str = "/callback"
    AUTH0_CALLBACK_REDIRECT_PATH: str = "/"
    AUTH0_SCOPE: str = "openid profile email"

    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    METRICS_COMPONENT_UPDATE_RESPONSE_SIZE_BUCKETS: List[int] = [
        1000,
        5000,
        10_000,
        100_000,
        1_000_000,
        10_000_000,
        100_000_000,
    ]

    GUNICORN_WORKERS: int = 2
    GUNICORN_WORKER_TIMEOUT: int = 30

    THREAD_POOL_EXECUTOR_WORKERS: int = 5

    class Config:
        env_prefix = "AMORA_DASH_"

    @property
    def auth0_login_enabled(self) -> bool:
        return (
            bool(self.AUTH0_CLIENT_ID)
            and bool(self.AUTH0_CLIENT_SECRET)
            and bool(self.AUTH0_DOMAIN)
        )

    @property
    def dbc_theme_stylesheet(self) -> str:
        return getattr(dbc.themes, self.DBC_THEME)

    @property
    def external_stylesheets(self) -> List[str]:
        return [self.dbc_theme_stylesheet, dbc.icons.FONT_AWESOME]

    @validator("DBC_THEME")
    def is_valid_dash_dbc_theme(cls, v):
        assert hasattr(dbc.themes, v)
        return v


settings = DashSettings()


class Size(str, Enum):
    extra_small = "xs"
    small = "sm"
    medium = "md"
    large = "lg"
    extra_large = "xl"


class Color(str, Enum):
    primary = "primary"
    secondary = "secondary"
    success = "success"
    warning = "warning"
    info = "info"
    danger = "danger"
