from models import ApprovalRecord, PortalDeal, RuleDecision


def evaluate_rules(
    record: ApprovalRecord,
    portal_deal: PortalDeal | None,
    previous_erp_rate: float | None,
) -> RuleDecision:
    if portal_deal is None:
        return RuleDecision(
            action="HOLD",
            reason="No matching portal record found",
            comment_to_add="No portal match found. Manual review required.",
            output_status="ON_HOLD",
        )

    if record.previous_version_status.upper() == "REJECTED":
        return RuleDecision(
            action="REJECT",
            reason="Previous version was rejected",
            comment_to_add="Rejected automatically because prior version was rejected.",
            output_status="REJECTED",
        )

    if not portal_deal.deal_won:
        return RuleDecision(
            action="SKIP",
            reason="Deal is not marked as won in portal",
            comment_to_add="No action taken because deal is not won.",
            output_status="SKIPPED",
        )

    if "INCOMPLETE CUSTOMER MAPPING" in record.restriction_message.upper():
        return RuleDecision(
            action="ATTACH_AND_HOLD",
            reason="Restriction requires support evidence",
            comment_to_add="Restriction detected. Supporting pricing report attached for review.",
            attach_file=True,
            output_status="ON_HOLD",
        )

    if record.is_complex and portal_deal.portal_comment:
        return RuleDecision(
            action="HOLD",
            reason="Complex record with external portal comment",
            comment_to_add=f"Complex workflow flagged. Portal comment: {portal_deal.portal_comment}",
            output_status="ON_HOLD",
        )

    if portal_deal.portal_comment:
        return RuleDecision(
            action="COMMENT_AND_HOLD",
            reason="Portal comment requires manual review",
            comment_to_add=f"Portal comment received: {portal_deal.portal_comment}",
            output_status="ON_HOLD",
        )

    if previous_erp_rate is not None and abs(previous_erp_rate - portal_deal.portal_exchange_rate) > 0.01:
        return RuleDecision(
            action="UPDATE_AND_APPROVE",
            reason="FX mismatch detected against previous ERP rate",
            comment_to_add=f"Exchange rate updated from {previous_erp_rate} to {portal_deal.portal_exchange_rate}.",
            update_exchange_rate=True,
            output_status="APPROVED",
        )

    return RuleDecision(
        action="APPROVE",
        reason="Validation checks passed",
        comment_to_add="Approved automatically after successful validation.",
        output_status="APPROVED",
    )