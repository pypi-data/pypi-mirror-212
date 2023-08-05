from typing import Optional

from pydantic import BaseModel


class Supervisor(BaseModel):
    iin: Optional[str]
    fullname: Optional[str]
