from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
    identifier: str
    reg_date: datetime

    bin: Optional[str]
    iin: Optional[str]
    address: Optional[str]
    name_ru: Optional[str]
    name_kk: Optional[str]
    role: Optional[str]
    kato: Optional[str]
    phone: Optional[str]
    email: Optional[str]
