from pydantic import BaseModel, ConfigDict


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

    model_config = ConfigDict(
        from_attributes=True,
    )

class RefreshTokenSchema(BaseModel):
    refresh_token: str

class AccessTokenSchema(BaseModel):
    access_token: str

