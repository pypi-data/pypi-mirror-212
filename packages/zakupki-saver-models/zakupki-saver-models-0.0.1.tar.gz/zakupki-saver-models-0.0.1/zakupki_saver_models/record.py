from typing import List

from pydantic import BaseModel

from zakupki_saver_models.company import Company
from zakupki_saver_models.complete_lot import CompleteLot
from zakupki_saver_models.representative import Representative
from zakupki_saver_models.supervisor import Supervisor
from zakupki_saver_models.tender import Tender


class Record(BaseModel):
    platform_id: str
    tender: Tender
    organizer: Company
    winner: Company
    complete_lots: List[CompleteLot]
    representative: Representative
    supervisor: Supervisor
