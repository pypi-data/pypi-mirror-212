import logging
from datetime import datetime
from typing import Iterable

import pytz

from fetchfox.apis.algorand import (
    algonodecloud,
    nfdomains,
    randswapcom,
    algoxnftcom,
    nftexplorerapp,
)
from fetchfox.blockchains.base import Blockchain
from fetchfox.constants.blockchains import ALGORAND
from fetchfox.constants.currencies import ALGO
from fetchfox.constants.marketplaces import (
    ALGOXNFT_COM,
    RANDGALLERY_COM,
    SHUFL_APP,
    UNKNOWN,
)
from fetchfox.dtos import AssetDTO, HoldingDTO, ListingDTO, SaleDTO
from . import utils

logger = logging.getLogger(__name__)


class Algorand(Blockchain):
    def __init__(self, nftexplorerapp_api_key: str = None):
        super().__init__(ALGORAND, ALGO)

        self.nftexplorerapp_api_key: str = nftexplorerapp_api_key

    def get_assets(
        self,
        collection_id: str,
        fetch_metadata: bool = True,
        *args,
        **kwargs,
    ) -> Iterable[AssetDTO]:
        for asset_id in algonodecloud.get_assets(collection_id):
            if fetch_metadata:
                yield self.get_asset(
                    collection_id=collection_id,
                    asset_id=asset_id,
                )
            else:
                yield AssetDTO(
                    collection_id=collection_id,
                    asset_id=asset_id,
                    metadata={},
                )

    def get_asset(self, collection_id: str, asset_id: str, *args, **kwargs) -> AssetDTO:
        data = algonodecloud.get_asset_data(asset_id)
        metadata = algonodecloud.get_asset_metadata(asset_id)
        metadata["name"] = data["name"]

        return AssetDTO(
            collection_id=collection_id,
            asset_id=asset_id,
            metadata=metadata,
        )

    def get_holdings(self, wallet: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        if utils.is_nf_domain(wallet):
            wallet = nfdomains.resolve_nf_domain(wallet)

        holdings = algonodecloud.get_holdings(wallet)

        for holding in holdings:
            asset_id = holding["asset-id"]
            quantity = holding["amount"]

            if quantity < 1:
                continue

            yield HoldingDTO(
                collection_id=None,
                asset_id=asset_id,
                address=wallet,
                quantity=quantity,
            )

    def get_snapshot(self, collection_id: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        for asset in self.get_assets(collection_id, fetch_metadata=False):
            holding = algonodecloud.get_owner(
                str(asset.asset_id),
            )

            yield HoldingDTO(
                collection_id=asset.collection_id,
                asset_id=holding["asset_id"],
                address=holding["address"],
                quantity=holding["amount"],
            )

    def get_listings(self, collection_id: str, *args, **kwargs) -> Iterable[ListingDTO]:
        listings = randswapcom.get_listings(collection_id)

        for listing in listings:
            asset_ids = [str(listing["assetId"])]
            asset_names = [""]

            listed_at = datetime.fromtimestamp(
                listing["timestamp"] // 1000,
            ).replace(
                tzinfo=pytz.UTC,
            )

            yield ListingDTO(
                identifier=listing["timestamp"],
                collection_id=collection_id,
                asset_ids=asset_ids,
                asset_names=asset_names,
                listing_id=listing["timestamp"],
                marketplace=RANDGALLERY_COM,
                price=listing["price"],
                currency=ALGO,
                listed_at=listed_at,
                listed_by=listing["sellerAddress"],
            )

        listings = algoxnftcom.get_listings(collection_id)

        for listing in listings:
            asset_ids = [str(listing["asset_id"])]
            asset_names = [""]

            listed_at = datetime.now(tz=pytz.utc)

            yield ListingDTO(
                identifier=listing["buy_it_now_listing_id"],
                collection_id=collection_id,
                asset_ids=asset_ids,
                asset_names=asset_names,
                listing_id=listing["buy_it_now_listing_id"],
                marketplace=ALGOXNFT_COM,
                price=listing["price"] // 10**6,
                currency=self.currency,
                listed_at=listed_at,
                listed_by=listing["seller"],
            )

    def get_sales(self, collection_id: str, *args, **kwargs) -> Iterable[SaleDTO]:
        venues = {
            "algoxnft": ALGOXNFT_COM,
            "randgallery": RANDGALLERY_COM,
            "shufl": SHUFL_APP,
            None: UNKNOWN,
        }

        sales = nftexplorerapp.get_sales(
            collection_id,
            api_key=self.nftexplorerapp_api_key,
        )

        for sale in sales:
            asset_ids = [str(sale["asset"])]
            asset_names = [sale["assetName"]]

            confirmed_at = datetime.fromtimestamp(
                sale["epochMs"] // 1000,
            ).replace(
                tzinfo=pytz.UTC,
            )

            yield SaleDTO(
                identifier=sale["txnId"],
                collection_id=collection_id,
                asset_ids=asset_ids,
                asset_names=asset_names,
                tx_hash=sale["txnId"],
                marketplace=venues[sale.get("venue")],
                price=sale["ualgos"] // 10**6,
                currency=self.currency,
                confirmed_at=confirmed_at,
                sold_by=sale["sender"],
                bought_by=sale["receiver"],
            )
