from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.models.transaction import TransactionType, TransactionCategory, TransactionSource

class TransactionBase(BaseModel):
    amount: int
    type: TransactionType
    category: TransactionCategory = TransactionCategory.other
    sub_category: Optional[str] = None
    description: Optional[str] = None
    merchant_name: Optional[str] = None
    upi_id: Optional[str] = None
    reference_id: Optional[str] = None
    source: TransactionSource
    transaction_date: datetime

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    category: Optional[TransactionCategory] = None
    sub_category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[int] = None

class TransactionResponse(TransactionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    is_deleted: bool

    model_config = {"from_attributes": True}

class TransactionListResponse(BaseModel):
    items: List[TransactionResponse]
    total: int
    page: int
    limit: int
