from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.budget import BudgetPeriod
from app.models.transaction import TransactionCategory

class BudgetBase(BaseModel):
    category: TransactionCategory
    limit_amount: int # stored as paise
    period: BudgetPeriod = BudgetPeriod.monthly
    alert_at_percent: int = 80

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    limit_amount: Optional[int] = None
    period: Optional[BudgetPeriod] = None
    alert_at_percent: Optional[int] = None

class BudgetResponse(BudgetBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    current_spend: int = 0
    usage_percent: float = 0.0

    model_config = {"from_attributes": True}
