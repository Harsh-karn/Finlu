from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from app.models.statement import StatementStatus

class StatementResponse(BaseModel):
    id: UUID
    user_id: UUID
    file_name: str
    file_url: str
    bank_name: str | None
    status: StatementStatus
    transactions_extracted: int
    uploaded_at: datetime

    model_config = {"from_attributes": True}
