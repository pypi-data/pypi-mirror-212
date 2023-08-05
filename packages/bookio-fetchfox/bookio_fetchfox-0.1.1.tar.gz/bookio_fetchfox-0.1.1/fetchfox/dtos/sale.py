from datetime import datetime
from typing import List


class SaleDTO:
    def __init__(
        self,
        identifier: str,
        collection_id: str,
        asset_ids: List[str],
        asset_names: List[str],
        tx_hash: str,
        marketplace: str,
        price: float,
        currency: str,
        confirmed_at: datetime,
        sale_id: str = None,
        sold_by: str = None,
        bought_by: str = None,
    ):
        self.identifier: str = identifier
        self.collection_id: str = collection_id
        self.asset_ids: List[str] = asset_ids
        self.asset_names: List[str] = asset_names
        self.tx_hash: str = tx_hash
        self.marketplace: str = marketplace
        self.price: float = price
        self.currency: str = currency
        self.confirmed_at: datetime = confirmed_at
        self.sale_id: str = sale_id
        self.sold_by: str = sold_by
        self.bought_by: str = bought_by

    @property
    def first(self) -> str:
        return self.asset_ids[0]

    @property
    def is_bundle(self) -> bool:
        return len(self.asset_ids) > 1

    def __repr__(self) -> str:
        return f"{self.collection_id}/{self.first} x {self.price} {self.currency} ({self.marketplace})"
