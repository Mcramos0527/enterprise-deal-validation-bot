import pandas as pd
from models import PortalDeal
from utils import DATA_DIR


class FakePortalClient:
    def __init__(self) -> None:
        self.portal_df = pd.read_csv(DATA_DIR / "portal_deals.csv")
        self.history_df = pd.read_csv(DATA_DIR / "approval_history.csv")

    def login(self) -> str:
        return "Portal login successful"

    def get_deal_by_agreement(self, agreement_number: str) -> PortalDeal | None:
        match = self.portal_df[self.portal_df["agreement_number"] == agreement_number]
        if match.empty:
            return None

        row = match.iloc[0]
        return PortalDeal(
            agreement_number=row["agreement_number"],
            version=int(row["version"]),
            deal_won=str(row["deal_won"]).lower() == "true",
            portal_exchange_rate=float(row["portal_exchange_rate"]),
            portal_comment=str(row["portal_comment"]) if pd.notna(row["portal_comment"]) else "",
            partner_report_available=str(row["partner_report_available"]).lower() == "true",
        )

    def get_previous_erp_exchange_rate(self, agreement_number: str) -> float | None:
        match = self.history_df[self.history_df["agreement_number"] == agreement_number]
        if match.empty:
            return None
        return float(match.iloc[-1]["erp_exchange_rate"])