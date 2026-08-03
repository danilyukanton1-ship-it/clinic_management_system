from pydantic import BaseModel, ConfigDict, EmailStr, Field, PositiveInt

from common.enums.user_role import UserRole


class MeSchema(BaseModel):
    id: PositiveInt = Field(
        description="User identifier.",
        examples=[1],
    )

    email: EmailStr = Field(
        description="User email address.",
        examples=["john.doe@example.com"],
    )

    phone: str = Field(
        description="User phone number.",
        examples=["+375291234567"],
    )

    first_name: str = Field(
        description="User first name.",
        examples=["John"],
    )

    last_name: str = Field(
        description="User last name.",
        examples=["Doe"],
    )

    middle_name: str | None = Field(
        default=None,
        description="User middle name.",
        examples=["Michael"],
    )

    role: UserRole = Field(
        description="User role in the system.",
        examples=["PATIENT"],
    )

    specialization: PositiveInt | None = Field(
        default=None,
        description="Medical specialization identifier. Available only for doctors.",
        examples=[5],
    )

    is_active: bool = Field(
        description="Indicates whether the user account is active.",
        examples=[True],
    )

    is_verified: bool = Field(
        description="Indicates whether the user's email address has been verified.",
        examples=[True],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )
