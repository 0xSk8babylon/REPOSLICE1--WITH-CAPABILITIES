from typing import Dict, List, Optional

from pydantic import Field

from app.core.schemas import ORMModel
from app.core.types import DataOrigin, IssueCategory, Severity


class CompatibilityIssue(ORMModel):
    id: str
    design_id: str
    severity: Severity
    category: IssueCategory
    issue: str
    why_it_matters: str
    possible_solutions: List[str]
    tradeoff: str
    related_equipment_ids: List[str] = Field(default_factory=list)
    data_origin: DataOrigin = DataOrigin.user_created


class CompatibilityExplanation(ORMModel):
    issue: str
    why_it_matters: str
    possible_solutions: List[str]
    tradeoff: str
    severity: Severity
    category: IssueCategory
    related_equipment_ids: List[str] = Field(default_factory=list)
    data_origin: DataOrigin = DataOrigin.placeholder
    provenance_summary: Optional[Dict[str, object]] = None
