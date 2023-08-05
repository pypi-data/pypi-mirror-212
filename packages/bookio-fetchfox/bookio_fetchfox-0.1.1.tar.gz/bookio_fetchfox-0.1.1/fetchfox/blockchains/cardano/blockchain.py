import base64
import logging
from datetime import datetime
from functools import lru_cache
from typing import Iterable

import pytz

from fetchfox.apis import bookio
from fetchfox.apis.cardano import blockfrostio, cnfttools, handleme, jpgstore
from fetchfox.blockchains.base import Blockchain
from fetchfox.constants.blockchains import CARDANO
from fetchfox.constants.currencies import ADA
from fetchfox.constants.marketplaces import JPG_STORE
from fetchfox.dtos import (
    AssetDTO,
    CampaignDTO,
    HoldingDTO,
    ListingDTO,
    RankDTO,
    SaleDTO,
)
from fetchfox.helpers import formatters
from . import utils

logger = logging.getLogger(__name__)


class Cardano(Blockchain):
    def __init__(self, blockfrostio_project_id: str = None):
        super().__init__(CARDANO, ADA)

        self.blockfrostio_project_id: str = blockfrostio_project_id

    @lru_cache
    def get_stake_address(self, wallet: str) -> str:
        if utils.is_stake_key(wallet):
            return wallet

        if utils.is_address(wallet):
            return blockfrostio.get_stake_address(
                wallet,
                project_id=self.blockfrostio_project_id,
            )

        if utils.is_ada_handle(wallet):
            return handleme.resolve_handle(wallet)

        return None

    def get_assets(
        self,
        collection_id: str,
        collection_discriminator: str = None,
        fetch_metadata: bool = True,
        *args,
        **kwargs,
    ) -> Iterable[AssetDTO]:
        response = blockfrostio.get_assets(
            collection_id,
            project_id=self.blockfrostio_project_id,
        )

        for asset_id in response:
            policy_id, asset_name = utils.split_asset_id(asset_id)

            # required for multi-book policies (e.g. monsters, greek classics)
            if collection_discriminator:
                if collection_discriminator not in asset_name.lower():
                    continue

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
        response = blockfrostio.get_asset_data(
            asset_id,
            project_id=self.blockfrostio_project_id,
        )

        metadata = response.get("onchain_metadata", {})

        return AssetDTO(
            collection_id=collection_id,
            asset_id=asset_id,
            metadata=metadata,
        )

    def get_campaigns(self) -> Iterable[CampaignDTO]:
        for campaign in bookio.campaigns():
            if campaign["blockchain"] != CARDANO:
                continue

            landing = campaign["landing"]
            start_at = campaign["start_at"]

            yield CampaignDTO(
                blockchain=CARDANO,
                parlamint_id=campaign["id"],
                collection_id=landing["lottery"]["collection_id"],
                name=campaign["display_name"],
                description=campaign["landing"]["opener"],
                supply=campaign["total_deas"],
                limit=campaign["max_quantity"],
                price=landing["price"],
                pricing=landing["price_description"]
                .replace(" (+2 ADA that will be returned with your eBook)", "")
                .strip(),
                rarity_chart_url=landing["rarity_chart_url"],
                start_at=formatters.timestamp(start_at["start_at"]),
            )

    def get_holdings(self, wallet: str, *args, **kwargs) -> Iterable[HoldingDTO]:
        stake_address = self.get_stake_address(wallet)

        holdings = blockfrostio.get_holdings(
            stake_address,
            project_id=self.blockfrostio_project_id,
        )

        for holding in holdings:
            asset_id = holding["unit"]

            if asset_id == "lovelace":
                continue

            quantity = int(holding["quantity"])

            policy_id, _ = utils.split_asset_id(asset_id)

            yield HoldingDTO(
                collection_id=policy_id,
                asset_id=asset_id,
                address=stake_address,
                quantity=quantity,
            )

    def get_ranks(self, collection_id: str, *args, **kwargs) -> Iterable[RankDTO]:
        for asset_name, rank in cnfttools.get_ranks(collection_id):
            asset_name_bytes = asset_name.encode()
            asset_name_base16 = base64.b16encode(asset_name_bytes).decode("utf-8")
            asset_id = f"{collection_id}{asset_name_base16}"

            yield RankDTO(
                collection_id=collection_id,
                asset_id=asset_id.lower(),
                asset_name=asset_name,
                rank=int(rank),
            )

    def get_snapshot(
        self,
        collection_id: str,
        collection_discriminator: str = None,
        *args,
        **kwargs,
    ) -> Iterable[HoldingDTO]:
        for asset in self.get_assets(
            collection_id,
            collection_discriminator=collection_discriminator,
            fetch_metadata=False,
        ):
            holding = blockfrostio.get_owner(
                asset.asset_id,
                project_id=self.blockfrostio_project_id,
            )

            stake_address = self.get_stake_address(holding["address"])

            yield HoldingDTO(
                collection_id=collection_id,
                asset_id=holding["asset_id"],
                address=stake_address,
                quantity=holding["amount"],
            )

    def get_listings(
        self, collection_id: str, collection_discriminator: str = None, *args, **kwargs
    ) -> Iterable[ListingDTO]:
        for listing in jpgstore.get_listings(collection_id):
            asset_id = listing["asset_id"]
            policy_id, asset_name = utils.split_asset_id(asset_id)

            # required for multi-book policies (e.g. monsters, greek classics)
            if collection_discriminator:
                if collection_discriminator not in asset_name.lower():
                    continue

            asset_ids = []
            asset_names = []

            if listing["listing_type"] == "BUNDLE":
                for bundled_asset in listing["bundled_assets"]:
                    asset_ids.append(bundled_asset["asset_id"])
                    asset_names.append(bundled_asset["display_name"])
            else:
                asset_ids.append(listing["asset_id"])
                asset_names.append(listing["display_name"])

            if listing.get("confirmed_at"):
                listed_at = datetime.fromisoformat(
                    listing["confirmed_at"].replace("Z", "+00:00")
                )
            else:
                listed_at = datetime.now(tz=pytz.utc)

            yield ListingDTO(
                identifier=listing["tx_hash"],
                collection_id=policy_id,
                asset_ids=asset_ids,
                asset_names=asset_names,
                listing_id=listing["listing_id"],
                marketplace=JPG_STORE,
                price=int(listing["price_lovelace"]) // 10**6,
                currency=self.currency,
                listed_at=listed_at,
                listed_by=None,
                tx_hash=listing["tx_hash"],
            )

    def get_sales(
        self, collection_id: str, collection_discriminator: str = None, *args, **kwargs
    ) -> Iterable[SaleDTO]:
        for sale in jpgstore.get_sales(collection_id):
            asset_id = sale["asset_id"]
            policy_id, asset_name = utils.split_asset_id(asset_id)

            # required for multi-book policies (e.g. monsters, greek classics)
            if collection_discriminator:
                if collection_discriminator not in asset_name.lower():
                    continue

            if sale["action"] == "ACCEPT_OFFER":
                buyer = sale["seller_address"]
                seller = sale["signer_address"]
            elif sale["action"] == "ACCEPT_COLLECTION_OFFER":
                buyer = sale["signer_address"]
                seller = sale["seller_address"]
            else:
                buyer = sale["signer_address"]
                seller = sale["seller_address"]

            asset_ids = []
            asset_names = []

            if sale["listing_from_tx_history"]["bundled_assets"]:
                for bundled_asset in sale["listing_from_tx_history"]["bundled_assets"]:
                    asset_ids.append(bundled_asset["asset_id"])
                    asset_names.append(bundled_asset["display_name"])
            else:
                asset_ids.append(sale["asset_id"])
                asset_names.append(sale["display_name"])

            if sale.get("confirmed_at"):
                confirmed_at = datetime.fromisoformat(
                    sale["confirmed_at"].replace("Z", "+00:00")
                )
            else:
                confirmed_at = datetime.now(tz=pytz.utc)

            yield SaleDTO(
                identifier=sale["tx_hash"],
                collection_id=policy_id,
                asset_ids=asset_ids,
                asset_names=asset_names,
                tx_hash=sale["tx_hash"],
                marketplace=JPG_STORE,
                price=int(sale["amount_lovelace"]) // 10**6,
                currency=self.currency,
                confirmed_at=confirmed_at,
                sold_by=seller,
                bought_by=buyer,
            )
