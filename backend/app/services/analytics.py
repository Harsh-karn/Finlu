from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any, List
from uuid import UUID
from datetime import datetime
import calendar
from app.models.transaction import Transaction, TransactionType

class AnalyticsService:
    @classmethod
    def get_summary(cls, db: Session, user_id: UUID, year: int, month: int) -> Dict[str, Any]:
        start_date, end_date = cls._get_month_bounds(year, month)
        
        base_query = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.is_deleted == False,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        )
        
        income = base_query.filter(Transaction.type == TransactionType.credit).scalar() or 0
        expense = base_query.filter(Transaction.type == TransactionType.debit).scalar() or 0
        
        # Top category
        top_cat_query = db.query(Transaction.category, func.sum(Transaction.amount).label('total'))\
            .filter(
                Transaction.user_id == user_id,
                Transaction.is_deleted == False,
                Transaction.type == TransactionType.debit,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )\
            .group_by(Transaction.category)\
            .order_by(func.sum(Transaction.amount).desc())\
            .first()
            
        top_category = top_cat_query[0] if top_cat_query else None
        
        # Avg daily spend
        _, num_days = calendar.monthrange(year, month)
        avg_daily = expense / num_days if num_days > 0 else 0
        
        return {
            "total_income": income,
            "total_expense": expense,
            "net_savings": income - expense,
            "top_category": top_category,
            "avg_daily_spend": int(avg_daily)
        }

    @classmethod
    def get_category_breakdown(cls, db: Session, user_id: UUID, year: int, month: int) -> List[Dict[str, Any]]:
        start_date, end_date = cls._get_month_bounds(year, month)
        
        # Total expense
        total_expense = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.is_deleted == False,
            Transaction.type == TransactionType.debit,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).scalar() or 0
        
        if total_expense == 0:
            return []
            
        results = db.query(Transaction.category, func.sum(Transaction.amount).label('total'))\
            .filter(
                Transaction.user_id == user_id,
                Transaction.is_deleted == False,
                Transaction.type == TransactionType.debit,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )\
            .group_by(Transaction.category)\
            .order_by(func.sum(Transaction.amount).desc())\
            .all()
            
        breakdown = []
        for cat, amount in results:
            breakdown.append({
                "category": cat,
                "amount": amount,
                "percentage": round((amount / total_expense) * 100, 2)
            })
            
        return breakdown

    @classmethod
    def _get_month_bounds(cls, year: int, month: int):
        start_date = datetime(year, month, 1)
        _, last_day = calendar.monthrange(year, month)
        end_date = datetime(year, month, last_day, 23, 59, 59, 999999)
        return start_date, end_date
