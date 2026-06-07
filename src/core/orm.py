from datetime import datetime, date
from typing import Annotated
from uuid import UUID

from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Text, Date, DateTime

id_pk = Annotated[int, mapped_column(primary_key=True)]

uuid_pk = Annotated[UUID, mapped_column(primary_key=True)]

str_64 = Annotated[str, mapped_column(String(64))]
str_128 = Annotated[str, mapped_column(String(128))]
str_256 = Annotated[str, mapped_column(String(256))]
str_512 = Annotated[str, mapped_column(String(512))]

text_column = Annotated[str, mapped_column(Text)]

bool_column = Annotated[bool, mapped_column(default=False)]

date_column = Annotated[date, mapped_column(Date)]
datetime_column = Annotated[datetime, mapped_column(DateTime(timezone=True))]

email_column = Annotated[str, mapped_column(String(256), unique=True)]
phone_column = Annotated[str, mapped_column(String(20), index=True)]
filename_column = Annotated[str, mapped_column(String(256))]
