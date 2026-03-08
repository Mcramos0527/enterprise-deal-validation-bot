from pathlib import Path
from models import ApprovalRecord, RuleDecision
from erp_client import FakeERPClient
from utils import ATTACHMENTS_DIR


def execute_action(
    erp_client: FakeERPClient,
    record: ApprovalRecord,
    decision: RuleDecision,
    portal_rate: float | None = None,
) -> list[str]:
    logs: list[str] = []

    if decision.update_exchange_rate and portal_rate is not None:
        logs.append(erp_client.update_exchange_rate(record.record_id, portal_rate))

    if decision.comment_to_add:
        logs.append(erp_client.add_comment(record.record_id, decision.comment_to_add))

    if decision.attach_file:
        file_path = ATTACHMENTS_DIR / "partner_pricing_report_demo.csv"
        if Path(file_path).exists():
            logs.append(erp_client.attach_file(record.record_id, file_path.name))
        else:
            logs.append(f"Attachment missing for {record.record_id}: {file_path.name}")

    if decision.output_status:
        logs.append(erp_client.set_status(record.record_id, decision.output_status))

    return logs