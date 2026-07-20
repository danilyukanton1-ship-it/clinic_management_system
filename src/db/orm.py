from datetime import datetime, date
from typing import Annotated
from uuid import UUID

from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Text, Date, DateTime, Integer

id_pk = Annotated[int, mapped_column(primary_key=True)]

uuid_pk = Annotated[UUID, mapped_column(primary_key=True)]

str_64 = Annotated[str, mapped_column(String(64))]
str_128 = Annotated[str, mapped_column(String(128))]
not_nullable_str_128 = Annotated[str, mapped_column(String(128), nullable=False)]
not_nullable_str_64 = Annotated[str, mapped_column(String(64), nullable=False)]
not_nullable_unique_str_128 = Annotated[str, mapped_column(String(128), nullable=False, unique=True)]
not_nullable_str_512 = Annotated[str, mapped_column(String(512), nullable=False)]
unique_str_128 = Annotated[str, mapped_column(String(128), unique=True)]
str_256 = Annotated[str, mapped_column(String(256))]
str_512 = Annotated[str, mapped_column(String(512))]

not_nullable_int = Annotated[int, mapped_column(Integer, nullable=False)]

text_column = Annotated[str, mapped_column(Text)]
nullable_text_column = Annotated[str | None, mapped_column(Text, nullable=True)]

bool_column = Annotated[bool, mapped_column(default=False)]

date_column = Annotated[date, mapped_column(Date)]
datetime_column = Annotated[datetime, mapped_column(DateTime(timezone=True))]

email_column = Annotated[str, mapped_column(String(256), unique=True)]
phone_column = Annotated[str | None, mapped_column(String(20), index=True, nullable=True)]
filename_column = Annotated[str, mapped_column(String(256))]
