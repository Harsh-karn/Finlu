import re
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.transaction import TransactionType

class SMSParserService:
    # Compile regex patterns for efficiency
    AMOUNT_PATTERN = re.compile(r'(?i)(?:rs\.?|inr|₹)\s*([\d,]+\.?\d*)')
    
    # Types of transactions
    DEBIT_KEYWORDS = ["debited", "sent", "paid", "payment of", "deducted", "withdrawal"]
    CREDIT_KEYWORDS = ["credited", "received", "added", "deposited"]
    
    UPI_ID_PATTERN = re.compile(r'([a-zA-Z0-9.\-_]+@[a-zA-Z]+)')
    REF_ID_PATTERN = re.compile(r'(?i)(?:ref no|upi ref|ref|transaction id|txn id)[:\s]*([0-9a-zA-Z]+)')
    
    # To capture merchant, we often look around "to" or "from" or "at"
    MERCHANT_TO_PATTERN = re.compile(r'(?i)to\s+([a-zA-Z0-9\s]+?)(?=\s+(?:via|upi|ref|on|\.|$))')
    MERCHANT_AT_PATTERN = re.compile(r'(?i)at\s+([a-zA-Z0-9\s]+?)(?=\s+(?:via|upi|ref|on|\.|$))')
    MERCHANT_FROM_PATTERN = re.compile(r'(?i)from\s+([a-zA-Z0-9\s]+?)(?=\s+(?:via|upi|ref|on|\.|$))')

    @classmethod
    def parse_sms(cls, raw_sms: str, received_at: datetime) -> Optional[Dict[str, Any]]:
        raw_sms_lower = raw_sms.lower()
        
        # Determine Type
        txn_type = None
        if any(kw in raw_sms_lower for kw in cls.DEBIT_KEYWORDS):
            txn_type = TransactionType.debit
        elif any(kw in raw_sms_lower for kw in cls.CREDIT_KEYWORDS):
            txn_type = TransactionType.credit
            
        if not txn_type:
            return None # Not a clear financial transaction
            
        # Determine Amount
        amount_match = cls.AMOUNT_PATTERN.search(raw_sms)
        if not amount_match:
            return None
        
        try:
            amount_str = amount_match.group(1).replace(',', '')
            amount_paise = int(float(amount_str) * 100)
        except ValueError:
            return None
            
        # Determine UPI ID
        upi_id_match = cls.UPI_ID_PATTERN.search(raw_sms)
        upi_id = upi_id_match.group(1) if upi_id_match else None
        
        # Determine Reference ID
        ref_id_match = cls.REF_ID_PATTERN.search(raw_sms)
        ref_id = ref_id_match.group(1) if ref_id_match else None
        
        # Determine Merchant
        merchant_name = None
        if txn_type == TransactionType.debit:
            merchant_match = cls.MERCHANT_TO_PATTERN.search(raw_sms) or cls.MERCHANT_AT_PATTERN.search(raw_sms)
            if merchant_match:
                merchant_name = merchant_match.group(1).strip()
        else:
            merchant_match = cls.MERCHANT_FROM_PATTERN.search(raw_sms)
            if merchant_match:
                merchant_name = merchant_match.group(1).strip()
                
        # Confidence heuristic
        confidence = 0.5
        if amount_paise > 0:
            confidence += 0.2
        if upi_id or ref_id:
            confidence += 0.2
        if merchant_name:
            confidence += 0.1
            
        return {
            "is_upi_transaction": True,
            "amount": amount_paise,
            "type": txn_type,
            "merchant_name": merchant_name,
            "upi_id": upi_id,
            "reference_id": ref_id,
            "transaction_date": received_at, # Note: a real implementation would extract the date from the SMS body if available
            "raw_sms": raw_sms,
            "confidence": min(1.0, confidence)
        }
