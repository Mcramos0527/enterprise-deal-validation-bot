from erp_client import FakeERPClient
from portal_client import FakePortalClient
from rules_engine import evaluate_rules
from actions import execute_action
from report_generator import write_change_report, write_execution_log
from utils import timestamp


def main() -> None:
    erp_client = FakeERPClient()
    portal_client = FakePortalClient()

    execution_logs: list[str] = []
    report_rows: list[dict] = []

    execution_logs.append(f"[{timestamp()}] Starting Enterprise Deal Validation Bot")
    execution_logs.append(f"[{timestamp()}] {portal_client.login()}")

    pending_records = erp_client.get_pending_records()
    execution_logs.append(f"[{timestamp()}] Loaded {len(pending_records)} pending records from ERP queue")

    for record in pending_records:
        execution_logs.append(
            f"[{timestamp()}] Processing record {record.record_id} / agreement {record.agreement_number}"
        )

        portal_deal = portal_client.get_deal_by_agreement(record.agreement_number)
        previous_erp_rate = portal_client.get_previous_erp_exchange_rate(record.agreement_number)

        decision = evaluate_rules(record, portal_deal, previous_erp_rate)

        action_logs = execute_action(
            erp_client=erp_client,
            record=record,
            decision=decision,
            portal_rate=portal_deal.portal_exchange_rate if portal_deal else None,
        )

        for log in action_logs:
            execution_logs.append(f"[{timestamp()}] {log}")

        report_rows.append(
            {
                "record_id": record.record_id,
                "agreement_number": record.agreement_number,
                "version": record.version,
                "customer_name": record.customer_name,
                "decision_action": decision.action,
                "decision_reason": decision.reason,
                "final_status": decision.output_status,
                "portal_comment": portal_deal.portal_comment if portal_deal else "",
                "portal_rate": portal_deal.portal_exchange_rate if portal_deal else "",
                "processed_at": timestamp(),
            }
        )

    report_path = write_change_report(report_rows)
    log_path = write_execution_log(execution_logs)

    print("Run completed successfully.")
    print(f"Change report: {report_path}")
    print(f"Execution log: {log_path}")


if __name__ == "__main__":
    main()