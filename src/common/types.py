from typing import Annotated

from fastapi import Path
from pydantic import EmailStr, StringConstraints

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
