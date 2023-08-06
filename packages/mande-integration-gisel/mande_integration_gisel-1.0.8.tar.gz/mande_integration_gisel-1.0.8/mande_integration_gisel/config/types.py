from dataclasses import dataclass, InitVar, field
from typing import Any, Dict, List, Union
from mande_integration_gisel.organizations import organizations
from enum import Enum, auto

@dataclass
class ExpenditureReport:
    category: str
    lc_total: str
    usd_total: str
    percent_by_category: str
    current_spend: str
    spend_to_date_lc: str
    spend_to_date_usd: str
    
    def to_list(self) -> List[str]:
        return [self.category, self.lc_total, self.usd_total, self.percent_by_category, self.current_spend, self.spend_to_date_lc, self.spend_to_date_usd]


@dataclass
class ExpenditureReportDetail:
    description: str
    narrative: str
    lc_total: str
    usd_total: str
    percent_by_category: str
    unexpended_balance: str
    current_spend_lc: str
    spend_to_date: str
    exch_rate: str
    
    def to_list(self) -> List[str]:
        return [self.description, self.narrative, self.lc_total, self.usd_total, self.percent_by_category, self.unexpended_balance, self.current_spend_lc, self.spend_to_date, self.exch_rate]
    
    
@dataclass
class Project:
    code: str
    name: str
    start_date: str
    end_date: str
    budget_total_amount: str
    status: str
    grant_type: str
    country: str
    organization_name: InitVar[str] = 'USADF'
    description: InitVar[str] = None
    
    @property
    def organization(self) -> Dict[str, Any]:
        return organizations[self.organization]
    
    def to_mande_format(self) -> Dict[str, Union[str, dict]]:
        grantTypes = ["YAL", "OAG", "EEG", "CB", "ELG"]
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "budgetTotalAmount": self.budget_total_amount,
            "status": self.status,
            "grantType": self.grant_type if self.grant_type in grantTypes else "OTHER",
            "country": self.country,
            "organization": organizations[self.organization_name]
        }


class PaginationDirection(Enum):
    LEFT = auto()
    RIGHT = auto()