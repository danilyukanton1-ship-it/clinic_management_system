from typing import Annotated
from pydantic import StringConstraints, EmailStr
from fastapi import Path

ID = Annotated[
    int,
    Path(
        ge=1,
        le=2_147_483_647,
    ),
]

Phone = Annotated[
    str,
    StringConstraints(
        pattern=r"^\+?[1-9]\d{7,14}$",
    ),
]

Email = EmailStr
