from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import os

from app.database import get_db
from app.models.user import User
from app.models.statement import Statement, StatementStatus
from app.models.transaction import Transaction
from app.schemas.statement import StatementResponse
from app.schemas.transaction import TransactionResponse
from app.utils.dependencies import get_current_user

# In a real app, this would use Celery. 
# For now, we'll use FastAPI BackgroundTasks for simplicity and demonstration,
# and later refactor to Celery tasks in Phase 3.
from app.services.pdf_parser import PDFParserService
from app.services.ai_categorizer import AICategorizerService

router = APIRouter(prefix="/api/v1/statements", tags=["statements"])

def process_statement_background(statement_id: UUID, file_bytes: bytes, user_id: UUID, db: Session):
    statement = db.query(Statement).filter(Statement.id == statement_id).first()
    if not statement:
        return
        
    try:
        statement.status = StatementStatus.processing
        db.commit()
        
        # 1. Parse PDF
        raw_txs = PDFParserService.parse_pdf(file_bytes, statement.bank_name)
        
        # 2. Categorize and Insert
        inserted_count = 0
        for tx_data in raw_txs:
            # Check duplicate by reference id
            if tx_data.get("reference_id"):
                exists = db.query(Transaction).filter(
                    Transaction.user_id == user_id,
                    Transaction.reference_id == tx_data["reference_id"]
                ).first()
                if exists:
                    continue
                    
            # We would await AI categorization here if it was fully async,
            # but for background task simplicity we use the fallback synchronous categorization
            category = AICategorizerService.fallback_categorize(tx_data["description"])
            
            new_tx = Transaction(
                user_id=user_id,
                amount=tx_data["amount"],
                type=tx_data["type"],
                category=category,
                description=tx_data["description"],
                reference_id=tx_data.get("reference_id"),
                source="pdf_upload",
                transaction_date=tx_data["transaction_date"]
            )
            db.add(new_tx)
            inserted_count += 1
            
        statement.transactions_extracted = inserted_count
        statement.status = StatementStatus.completed
        db.commit()
        
    except Exception as e:
        statement.status = StatementStatus.failed
        db.commit()

@router.post("/upload", response_model=StatementResponse, status_code=status.HTTP_201_CREATED)
async def upload_statement(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith('.pdf') and not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only PDF and CSV files are supported")
        
    file_bytes = await file.read()
    
    # In production, upload file to Cloudinary/S3 and get URL.
    # For now, we mock the URL.
    file_url = f"mock://{file.filename}"
    
    statement = Statement(
        user_id=current_user.id,
        file_name=file.filename,
        file_url=file_url,
        status=StatementStatus.pending
    )
    db.add(statement)
    db.commit()
    db.refresh(statement)
    
    # Process in background
    background_tasks.add_task(process_statement_background, statement.id, file_bytes, current_user.id, db)
    
    return statement

@router.get("/", response_model=List[StatementResponse])
def get_statements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statements = db.query(Statement).filter(Statement.user_id == current_user.id).order_by(Statement.uploaded_at.desc()).all()
    return statements

@router.get("/{statement_id}/status", response_model=StatementResponse)
def get_statement_status(
    statement_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = db.query(Statement).filter(Statement.id == statement_id, Statement.user_id == current_user.id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    return statement

@router.delete("/{statement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_statement(
    statement_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = db.query(Statement).filter(Statement.id == statement_id, Statement.user_id == current_user.id).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
        
    db.delete(statement)
    db.commit()
    return None
