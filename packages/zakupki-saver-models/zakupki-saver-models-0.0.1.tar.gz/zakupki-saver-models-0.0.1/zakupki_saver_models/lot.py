from typing import Optional

from pydantic import BaseModel


class Lot(BaseModel):
    number: str
    name: str
    price: str
    url: str

    tru_code: Optional[str] = None
    count: Optional[str] = None
    tender_subject_type: Optional[str] = None
    total_sum: Optional[str] = None
    delivery_address: Optional[str] = None
