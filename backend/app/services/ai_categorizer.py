import google.generativeai as genai
import json
from typing import Dict, Any, Optional
from app.config import settings

# Initialize Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

class AICategorizerService:
    CATEGORY_KEYWORDS = {
        "food": ["zomato", "swiggy", "dominos", "mcdonalds", "kfc", "subway", "blinkit", "instamart", "zepto", "restaurant", "hotel", "dhaba", "cafe", "pizza"],
        "transport": ["ola", "uber", "rapido", "metro", "irctc", "redbus", "petrol", "fuel", "parking", "toll", "makemytrip", "ixigo", "indigo", "spicejet"],
        "shopping": ["amazon", "flipkart", "myntra", "ajio", "meesho", "nykaa", "reliance", "dmart", "bigbasket"],
        "utilities": ["electricity", "jio", "airtel", "vi", "bsnl", "water", "gas", "wifi", "broadband", "recharge"],
        "health": ["pharmacy", "apollo", "medplus", "practo", "1mg", "hospital", "clinic", "doctor", "lab", "test"],
        "entertainment": ["netflix", "spotify", "hotstar", "prime", "bookmyshow", "pvr", "inox", "youtube"],
        "education": ["udemy", "coursera", "byju", "unacademy", "leetcode", "college", "school", "tuition"]
    }

    @classmethod
    def fallback_categorize(cls, merchant_or_description: str) -> str:
        text = merchant_or_description.lower()
        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                return category
        return "other"

    @classmethod
    async def categorize_transaction(
        cls, 
        description: str, 
        merchant_or_upi: str, 
        amount: int, 
        debit_or_credit: str
    ) -> Dict[str, Any]:
        
        # If API key is missing, fallback immediately
        if not settings.GEMINI_API_KEY:
            category = cls.fallback_categorize(merchant_or_upi or description)
            return {
                "category": category,
                "sub_category": None,
                "merchant_normalized": merchant_or_upi,
                "confidence": 0.5
            }

        prompt = f"""
        You are a financial transaction categorizer for Indian UPI transactions.

        Given this transaction, return ONLY a JSON object with:
        - category: one of [food, transport, shopping, entertainment, utilities, health, education, rent, salary, investment, transfer, other]
        - sub_category: specific type (e.g., "restaurant", "grocery", "cab", "movie", "electricity")
        - merchant_normalized: cleaned merchant name
        - confidence: 0.0 to 1.0

        Transaction:
        - Description: {description}
        - Merchant/UPI ID: {merchant_or_upi}
        - Amount: ₹{amount/100:.2f}
        - Type: {debit_or_credit}

        Return ONLY valid JSON. No explanation.
        """

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            # Extract JSON string from response
            text = response.text.strip()
            if text.startswith('```json'):
                text = text[7:-3]
            elif text.startswith('```'):
                text = text[3:-3]
                
            data = json.loads(text.strip())
            return data
            
        except Exception as e:
            # Fallback to keyword if Gemini fails
            category = cls.fallback_categorize(merchant_or_upi or description)
            return {
                "category": category,
                "sub_category": None,
                "merchant_normalized": merchant_or_upi,
                "confidence": 0.3
            }
