from pydantic import BaseModel, Field, NonNegativeInt


__all__ = ["AppInfo", "AuthInfo", "TokenInfo"]


class AppInfo(BaseModel):
    app_id: int = Field(
        None,
        title="app ID",
        description="Сan be found in your account",
    )
    secret_key: str = Field(
        None,
        title="app secret key",
        description="Сan be found in your account",
    )


class AuthInfo(BaseModel):
    login: str = Field(
        None,
        title="login",
        description="Site login",
    )
    password: str = Field(
        None,
        title="password",
        description="Account password",
    )


class TokenInfo(BaseModel):
    token: str = Field(
        None,
        title="token",
        description="Received token",
    )
    refresh_token: str = Field(
        None,
        title="refresh token",
        description="To refresh the token",
    )
    expires_in: NonNegativeInt = Field(
        None,
        title="expires in",
        description="How long the token lives (seconds)",
    )
