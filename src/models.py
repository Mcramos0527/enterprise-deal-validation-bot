from dataclasses import dataclass


@dataclass
class ApprovalRecord:
    record_id: str
    version: int
    customer_name: str
    region: str
    currency_primary: str
    currency_secondary: str
    previous_version_status: str
    restriction_message: str
    agreement_number: str
    is_complex: bool


@dataclass
class PortalDeal:
    agreement_number: str
    version: int
    deal_won: bool
    portal_exchange_rate: float
    portal_comment: str
    partner_report_available: bool


@dataclass
class RuleDecision:
    action: str
    reason: str
    comment_to_add: str = ""
    update_exchange_rate: bool = False
    attach_file: bool = False
    output_status: str = ""