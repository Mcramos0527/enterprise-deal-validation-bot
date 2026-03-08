import pandas as pd
from models import ApprovalRecord
from utils import DATA_DIR


class FakeERPClient:
    def __init__(self) -> None:
        self.pending_df = pd.read_csv(DATA_DIR / "pending_approvals.csv")

    def get_pending_records(self) -> list[ApprovalRecord]:
        records = []
        for _, row in self.pending_df.iterrows():
            records.append(
                ApprovalRecord(
                    record_id=row["record_id"],
                    version=int(row["version"]),
                    customer_name=row["customer_name"],
                    region=row["region"],
                    currency_primary=row["currency_primary"],
                    currency_secondary=row["currency_secondary"],
                    previous_version_status=row["previous_version_status"],
                    restriction_message=str(row["restriction_message"]) if pd.notna(row["restriction_message"]) else "",
                    agreement_number=row["agreement_number"],
                    is_complex=str(row["is_complex"]).lower() == "true",
                )
            )
        return records

    def update_exchange_rate(self, record_id: str, new_rate: float) -> str:
        return f"ERP exchange rate updated for {record_id} to {new_rate}"

    def add_comment(self, record_id: str, comment: str) -> str:
        return f"Comment added to {record_id}: {comment}"

    def set_status(self, record_id: str, status: str) -> str:
        return f"Status for {record_id} set to {status}"

    def attach_file(self, record_id: str, file_name: str) -> str:
        return f"File {file_name} attached to {record_id}"