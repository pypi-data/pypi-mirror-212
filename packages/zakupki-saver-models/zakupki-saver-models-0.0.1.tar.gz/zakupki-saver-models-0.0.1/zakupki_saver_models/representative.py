from typing import Optional

from pydantic import BaseModel


class Representative(BaseModel):
    fullname: Optional[str]
    phone: Optional[str]
    position: Optional[str]
    email: Optional[str]
