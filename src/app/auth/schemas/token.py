from pydantic import BaseModel, ConfigDict, Field


class TokenResponseSchema(BaseModel):
    access_token: str = Field(
        description="JWT access token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )

    refresh_token: str = Field(
        description="JWT refresh token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )

    token_type: str = Field(
        default="bearer",
        description="Authentication scheme.",
        examples=["bearer"],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


class RefreshTokenSchema(BaseModel):
    refresh_token: str = Field(
        description="JWT refresh token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )


class AccessTokenSchema(BaseModel):
    access_token: str = Field(
        description="JWT access token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
