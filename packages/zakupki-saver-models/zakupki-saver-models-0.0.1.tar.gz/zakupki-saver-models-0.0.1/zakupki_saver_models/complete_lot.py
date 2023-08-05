from pydantic import BaseModel

from zakupki_saver_models.lot import Lot


class CompleteLot(BaseModel):
    lot: Lot
