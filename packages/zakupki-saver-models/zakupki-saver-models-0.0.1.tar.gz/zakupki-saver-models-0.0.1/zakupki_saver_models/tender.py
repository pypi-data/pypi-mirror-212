from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Tender(BaseModel):
    number: str
    publication_date_time: datetime
    begin_date_time: datetime
    end_date_time: datetime
    lot_amount: str
    lot_sum_total: str
    url: str

    name_ru: Optional[str]
    name_kk: Optional[str]
    description_ru: Optional[str]
    description_kk: Optional[str]
    tender_type: Optional[str]
    tender_priority: Optional[str]
