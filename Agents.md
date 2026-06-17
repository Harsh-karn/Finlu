Here's your complete master prompt — ready to paste into Cursor, Claude, or any AI coding tool:

---

```
# 💸 UPI Money Manager — Full-Stack Production App

## PROJECT OVERVIEW
Build a production-ready UPI expense tracking and money management 
web application called "FlowMoney" (or rename as preferred). The app 
automatically tracks expenses from three sources:
1. Android SMS auto-parsing (via a companion Android app)
2. Bank statement PDF/CSV upload with AI extraction
3. Manual transaction entry with smart categorization

All three sources feed into a single unified backend and dashboard.

---

## TECH STACK

### Backend
- Framework: FastAPI (Python 3.11+)
- Database: PostgreSQL with SQLAlchemy ORM + Alembic migrations
- Auth: JWT (python-jose) + bcrypt password hashing
- AI/LLM: Google Gemini 1.5 Flash API for PDF parsing & categorization
- PDF Parsing: pdfplumber + PyMuPDF (fallback)
- CSV Parsing: pandas
- Task Queue: Celery + Redis (for async PDF processing)
- Email: FastAPI-Mail (for budget alerts)
- Validation: Pydantic v2

### Frontend
- Framework: Next.js 15 (App Router) + TypeScript
- Styling: Tailwind CSS + shadcn/ui components
- Charts: Recharts
- State: Zustand
- Forms: React Hook Form + Zod
- HTTP: Axios with interceptors
- Auth: NextAuth.js (JWT strategy)

### Android App
- Language: Kotlin
- Architecture: MVVM + Clean Architecture
- SMS Reading: BroadcastReceiver + WorkManager
- HTTP: Retrofit2 + OkHttp
- Local DB: Room (offline queue)
- DI: Hilt

### Infrastructure
- Backend Deployment: Railway or Render
- Frontend Deployment: Vercel
- DB Hosting: Supabase PostgreSQL or Railway PostgreSQL
- Redis: Upstash Redis
- Storage: Cloudinary or Supabase Storage (for statement files)
- CI/CD: GitHub Actions

---

## DATABASE SCHEMA

### Users Table
- id (UUID, PK)
- email (unique)
- password_hash
- name
- phone_number
- currency (default: INR)
- monthly_budget (nullable)
- created_at, updated_at

### Transactions Table
- id (UUID, PK)
- user_id (FK → users)
- amount (Decimal 10,2)
- type (ENUM: debit, credit)
- category (ENUM: food, transport, shopping, entertainment, 
  utilities, health, education, rent, salary, investment, other)
- sub_category (text, nullable)
- description (text)
- merchant_name (text, nullable)
- upi_id (text, nullable) — the UPI VPA of sender/receiver
- reference_id (text, nullable) — UPI transaction reference
- source (ENUM: sms, pdf_upload, manual)
- transaction_date (timestamp)
- created_at (timestamp)
- is_deleted (boolean, default false) — soft delete

### Statements Table
- id (UUID, PK)
- user_id (FK → users)
- file_name (text)
- file_url (text)
- bank_name (text, nullable)
- status (ENUM: pending, processing, completed, failed)
- transactions_extracted (integer)
- uploaded_at (timestamp)

### Budgets Table
- id (UUID, PK)
- user_id (FK → users)
- category (ENUM — same as transactions)
- limit_amount (Decimal 10,2)
- period (ENUM: weekly, monthly)
- alert_at_percent (integer, default: 80)
- created_at, updated_at

### SMS_Devices Table
- id (UUID, PK)
- user_id (FK → users)
- device_name (text)
- api_key (text, unique) — device-specific key for SMS posting
- last_sync (timestamp)
- is_active (boolean)

---

## BACKEND — FastAPI

### Project Structure
```
backend/
├── app/
│   ├── main.py
│   ├── config.py               # Pydantic settings from .env
│   ├── database.py             # SQLAlchemy engine + session
│   ├── models/
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── statement.py
│   │   ├── budget.py
│   │   └── sms_device.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── statement.py
│   │   └── budget.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── transactions.py
│   │   ├── statements.py
│   │   ├── sms.py
│   │   ├── budgets.py
│   │   └── analytics.py
│   ├── services/
│   │   ├── sms_parser.py       # Regex-based UPI SMS parser
│   │   ├── pdf_parser.py       # pdfplumber + Gemini extraction
│   │   ├── csv_parser.py       # pandas-based CSV parser
│   │   ├── ai_categorizer.py   # Gemini for category detection
│   │   ├── budget_checker.py   # Alert logic
│   │   └── analytics.py       # Aggregation queries
│   ├── workers/
│   │   └── tasks.py            # Celery tasks (async PDF processing)
│   └── utils/
│       ├── security.py         # JWT + bcrypt
│       └── dependencies.py     # get_current_user, etc.
├── alembic/
├── tests/
├── .env.example
├── requirements.txt
└── Dockerfile
```

### API Endpoints

#### Auth Routes (/api/v1/auth)
- POST /register — email, password, name, phone
- POST /login — returns access_token + refresh_token
- POST /refresh — refresh access token
- POST /logout
- GET /me — current user profile
- PATCH /me — update profile + monthly_budget

#### Transaction Routes (/api/v1/transactions)
- GET / — paginated list with filters:
  ?page=1&limit=20&category=food&type=debit
  &start_date=2025-01-01&end_date=2025-01-31
  &source=sms&search=zomato
- POST / — manual transaction entry
- GET /{id} — single transaction
- PATCH /{id} — edit category, description, amount
- DELETE /{id} — soft delete
- POST /bulk — bulk insert (used internally by SMS/PDF parsers)
- GET /duplicates — detect potential duplicates by ref_id or amount+date

#### SMS Routes (/api/v1/sms)
- POST /ingest — Android app posts raw SMS text here
  Body: { raw_sms: str, received_at: datetime, device_api_key: str }
  Returns: parsed transaction object or null if not UPI SMS
- POST /devices/register — register an Android device
- GET /devices — list user's registered devices
- DELETE /devices/{id}

#### Statement Routes (/api/v1/statements)
- POST /upload — multipart file upload (PDF or CSV)
  Accepts: SBI, HDFC, ICICI, Axis, Kotak, IDFC, Yes Bank formats
  Triggers async Celery task for processing
- GET / — list all uploaded statements
- GET /{id}/status — check processing status + progress
- GET /{id}/transactions — transactions extracted from a statement
- DELETE /{id}

#### Budget Routes (/api/v1/budgets)
- GET / — list all budgets with current usage %
- POST / — create budget for a category
- PATCH /{id}
- DELETE /{id}
- GET /alerts — categories currently exceeding alert threshold

#### Analytics Routes (/api/v1/analytics)
- GET /summary?period=monthly&date=2025-01 
  Returns: total_income, total_expense, net_savings, 
           top_category, avg_daily_spend
- GET /category-breakdown?period=monthly&date=2025-01
  Returns: per-category totals + % of total spend
- GET /trends?months=6
  Returns: monthly income vs expense for last N months
- GET /daily?month=2025-01
  Returns: day-by-day spend for the month (for heatmap)
- GET /merchants/top?limit=10&period=monthly
  Returns: top merchants by spend
- GET /cashflow?period=monthly
  Returns: daily running balance for the month

---

## SMS PARSER SERVICE

Parse UPI SMS from all major Indian banks. The parser must handle 
messages from: SBI, HDFC, ICICI, Axis, Kotak, Yes Bank, IDFC First, 
PNB, Canara, Bank of Baroda, IndusInd, Federal Bank, AU Small Finance.

Also parse confirmation messages from UPI apps: 
GPay, PhonePe, Paytm, BHIM, Amazon Pay.

### Regex Patterns to Extract:
1. Transaction type: "debited", "credited", "sent", "received", 
   "paid", "payment of"
2. Amount: Rs., INR, ₹ followed by amount
3. Merchant/Receiver name: "to [name]", "from [name]", "at [merchant]"
4. UPI ID: anything with @[bank/upi]
5. Reference number: UPI Ref, Ref No, Transaction ID patterns
6. Date/Time: from SMS timestamp

### Example SMS formats to handle:
- "INR 500.00 debited from A/c XX1234 on 15-01-25 to VPA zomato@okaxis 
   Ref No 123456789. Call 18001234 for dispute."
- "Rs.250 Paid to SWIGGY via UPI. UPI Ref:987654321. 
   If not done by you call 1800XXXX"
- "Your a/c XXXX1234 is credited with INR 5000.00 on 15/01/2025 
   by UPI-IMPS from Rahul Kumar Ref 112233445566"
- "PhonePe: Rs 1200.00 sent to Flipkart. UPI Ref: 123456789012"
- "GPay: Payment of Rs.450 to Ola successfully processed. 
   Ref: 9876543210"

### Parser Output Schema:
```json
{
  "is_upi_transaction": true,
  "amount": 500.00,
  "type": "debit",
  "merchant_name": "Zomato",
  "upi_id": "zomato@okaxis",
  "reference_id": "123456789",
  "transaction_date": "2025-01-15T00:00:00",
  "raw_sms": "original SMS text",
  "confidence": 0.95
}
```

---

## AI CATEGORIZATION SERVICE (Gemini)

After parsing SMS or extracting from PDF, call Gemini 1.5 Flash 
to auto-categorize transactions.

### Prompt Template:
```
You are a financial transaction categorizer for Indian UPI transactions.

Given this transaction, return ONLY a JSON object with:
- category: one of [food, transport, shopping, entertainment, 
  utilities, health, education, rent, salary, investment, 
  transfer, other]
- sub_category: specific type (e.g., "restaurant", "grocery", 
  "cab", "movie", "electricity")
- merchant_normalized: cleaned merchant name
- confidence: 0.0 to 1.0

Transaction:
- Description: {description}
- Merchant/UPI ID: {merchant_or_upi}
- Amount: ₹{amount}
- Type: {debit_or_credit}

Return ONLY valid JSON. No explanation.
```

### Batch Processing:
- Batch up to 20 transactions per Gemini call to save API costs
- Cache results by merchant name in Redis (TTL: 7 days)
- Fallback to keyword-based categorization if Gemini fails

### Keyword Fallback Map:
```python
CATEGORY_KEYWORDS = {
  "food": ["zomato", "swiggy", "dominos", "mcdonalds", "kfc", 
           "subway", "blinkit", "instamart", "zepto", "restaurant",
           "hotel", "dhaba", "cafe", "pizza"],
  "transport": ["ola", "uber", "rapido", "metro", "irctc", 
                "redbus", "petrol", "fuel", "parking", "toll",
                "makemytrip", "ixigo", "indigo", "spicejet"],
  "shopping": ["amazon", "flipkart", "myntra", "ajio", "meesho",
               "nykaa", "reliance", "dmart", "bigbasket"],
  "utilities": ["electricity", "jio", "airtel", "vi", "bsnl",
                "water", "gas", "wifi", "broadband", "recharge"],
  "health": ["pharmacy", "apollo", "medplus", "practo", "1mg",
             "hospital", "clinic", "doctor", "lab", "test"],
  "entertainment": ["netflix", "spotify", "hotstar", "prime",
                    "bookmyshow", "pvr", "inox", "youtube"],
  "education": ["udemy", "coursera", "byju", "unacademy", 
                "leetcode", "college", "school", "tuition"]
}
```

---

## PDF/CSV STATEMENT PARSER

### Supported Bank Formats:

#### SBI (State Bank of India)
- PDF: Table with columns: Txn Date, Value Date, Description, 
  Ref No./Cheque No., Debit, Credit, Balance
- CSV: Same column names, comma-separated

#### HDFC Bank
- PDF: Date, Narration, Chq./Ref.No., Value Dt, 
  Withdrawal Amt., Deposit Amt., Closing Balance
- CSV: Same

#### ICICI Bank  
- PDF: Transaction Date, Value Date, Transaction Remarks, 
  Ref No./Cheque No., Debit, Credit, Balance (INR)

#### Axis Bank
- PDF: Tran Date, Chq No, Particulars, Debit, Credit, Balance

#### Kotak Mahindra
- PDF: Date, Description, Chq/Ref No, Debit, Credit, Balance

### PDF Parsing Strategy:
1. Use pdfplumber to extract tables from PDF
2. Auto-detect bank format from header row keywords
3. Map columns to unified schema
4. If table extraction fails, use Gemini Vision to extract 
   transaction data from PDF pages as images
5. Deduplicate against existing transactions by reference_id

### Gemini PDF Fallback Prompt:
```
Extract all bank transactions from this bank statement image.
Return a JSON array where each object has:
- date (YYYY-MM-DD)
- description (text)
- debit (number or null)
- credit (number or null)  
- balance (number)
- reference_number (text or null)

Return ONLY valid JSON array. No markdown.
```

---

## FRONTEND — Next.js

### Project Structure
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (dashboard)/
│   │   ├── layout.tsx          # Sidebar + header
│   │   ├── page.tsx            # Overview dashboard
│   │   ├── transactions/
│   │   │   ├── page.tsx        # Transaction list
│   │   │   └── [id]/page.tsx
│   │   ├── upload/page.tsx     # Statement upload
│   │   ├── budgets/page.tsx    
│   │   ├── analytics/page.tsx  # Charts & insights
│   │   └── settings/page.tsx
│   └── api/
│       └── auth/[...nextauth]/route.ts
├── components/
│   ├── dashboard/
│   │   ├── StatsCards.tsx      # Income, expense, savings cards
│   │   ├── SpendingChart.tsx   # Recharts line/bar chart
│   │   ├── CategoryDonut.tsx   # Donut chart by category
│   │   ├── RecentTransactions.tsx
│   │   ├── BudgetProgress.tsx  # Progress bars per category
│   │   └── CashflowChart.tsx   # Daily balance line chart
│   ├── transactions/
│   │   ├── TransactionTable.tsx
│   │   ├── TransactionFilters.tsx
│   │   ├── AddTransactionModal.tsx
│   │   ├── EditTransactionModal.tsx
│   │   └── TransactionBadge.tsx # Category color badge
│   ├── upload/
│   │   ├── FileDropzone.tsx
│   │   ├── UploadProgress.tsx
│   │   └── StatementHistory.tsx
│   ├── budgets/
│   │   ├── BudgetCard.tsx
│   │   └── CreateBudgetModal.tsx
│   └── shared/
│       ├── Sidebar.tsx
│       ├── Header.tsx
│       ├── LoadingSpinner.tsx
│       └── EmptyState.tsx
├── lib/
│   ├── api.ts                  # Axios instance with auth interceptors
│   ├── utils.ts                # formatCurrency, formatDate, etc.
│   └── constants.ts            # category colors, icons map
├── store/
│   └── useAppStore.ts          # Zustand store
├── types/
│   └── index.ts                # TypeScript interfaces
└── hooks/
    ├── useTransactions.ts
    ├── useAnalytics.ts
    └── useBudgets.ts
```

### Dashboard Page Layout:
- Top row: 4 stat cards — Total Income, Total Expense, 
  Net Savings, Savings Rate %
- Second row: Monthly trend chart (bar — income vs expense) 
  + Category donut chart
- Third row: Budget progress bars + Recent transactions list
- All data fetched via SWR or React Query with 30s revalidation

### Transaction Table Features:
- Sortable columns (date, amount, category)
- Filter sidebar: date range, category (multi-select), 
  type (debit/credit), source (sms/pdf/manual)
- Search by merchant name or description
- Inline edit for category and description
- Color-coded category badges
- Source icon (SMS icon, PDF icon, pencil icon)
- Pagination (20 per page)
- Export to CSV button

### Upload Page:
- Drag & drop zone accepting PDF and CSV
- Bank selector dropdown (auto-detected but overridable)
- Upload progress bar with status polling
- Preview of extracted transactions before confirming
- Duplicate detection warning with merge options

### Analytics Page:
- Date range picker (this month, last month, last 3/6/12 months, custom)
- Monthly Income vs Expense bar chart
- Category breakdown donut + table with % and amounts
- Top 10 merchants by spend (horizontal bar chart)
- Daily spending heatmap (calendar view)
- Running balance line chart
- Savings trend over months

### UI Design System:
- Color scheme: Dark mode by default, toggle for light
- Primary: #6366f1 (indigo)
- Success/Credit: #22c55e (green)
- Danger/Debit: #ef4444 (red)
- Background: #0f0f0f / #1a1a2e
- Cards: #1e1e2e with subtle border
- Font: Inter
- Category color map:
  food → orange, transport → blue, shopping → purple,
  entertainment → pink, utilities → yellow, health → green,
  education → cyan, rent → red, salary → emerald,
  investment → teal, other → gray

---

## ANDROID APP — Kotlin

### Project Structure
```
android/
├── app/src/main/java/com/flowmoney/
│   ├── data/
│   │   ├── local/
│   │   │   ├── AppDatabase.kt      # Room DB
│   │   │   └── PendingSmsDao.kt    # Queue for offline SMS
│   │   ├── remote/
│   │   │   ├── ApiService.kt       # Retrofit interface
│   │   │   └── ApiClient.kt        # OkHttp + interceptors
│   │   └── repository/
│   │       └── SmsRepository.kt
│   ├── domain/
│   │   └── SmsParser.kt            # Regex-based SMS parsing
│   ├── receivers/
│   │   └── SmsReceiver.kt          # BroadcastReceiver
│   ├── workers/
│   │   └── SmsUploadWorker.kt      # WorkManager background sync
│   ├── ui/
│   │   ├── MainActivity.kt
│   │   ├── setup/SetupActivity.kt  # Enter server URL + API key
│   │   └── status/StatusFragment.kt # Last sync, count uploaded
│   └── di/
│       └── AppModule.kt            # Hilt modules
```

### SMS Flow:
1. SmsReceiver catches incoming SMS broadcast
2. SmsParser checks if it's a bank/UPI transaction SMS
3. If yes, create PendingSms record in Room DB
4. WorkManager SmsUploadWorker picks it up and POSTs to
   /api/v1/sms/ingest with device_api_key
5. On success, mark as synced. On failure, retry with backoff.
6. App shows minimal notification: "Transaction detected: ₹500 to Zomato"

### Permissions Required:
- RECEIVE_SMS
- READ_SMS (for historical SMS import on first setup)
- INTERNET
- FOREGROUND_SERVICE (for background sync)

### Historical SMS Import:
On first launch, offer to scan last 90 days of SMS inbox,
parse all UPI transactions, and bulk upload to backend.
Show progress: "Found 47 UPI transactions in your SMS"

---

## ENVIRONMENT VARIABLES

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host/dbname
SECRET_KEY=your-jwt-secret-256-bit
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
GEMINI_API_KEY=your-gemini-api-key
REDIS_URL=redis://localhost:6379
CLOUDINARY_URL=cloudinary://...
FRONTEND_URL=https://flowmoney.vercel.app
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=app-password
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://api.flowmoney.app/api/v1
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000
```

---

## KEY FEATURES TO IMPLEMENT

1. **Duplicate Detection**: Before inserting any transaction, check 
   if a transaction with same reference_id exists for that user.
   If no reference_id, check amount + date + type within 2-minute 
   window. Flag suspected duplicates for user review.

2. **Smart Merge**: When same transaction appears from both SMS 
   and PDF upload, merge into one record, keeping SMS as primary 
   source and enriching with PDF data.

3. **Budget Alerts**: After every transaction insert, run 
   budget_checker service. If category spend crosses alert_at_percent 
   of monthly limit, send email + in-app notification.

4. **Monthly Report**: Cron job on 1st of every month emails 
   previous month summary: total spend, top category, 
   vs last month comparison, savings achieved.

5. **Split Transaction**: Allow user to split one transaction 
   into multiple categories (e.g., a BigBasket order split 
   between groceries and household).

6. **Notes & Tags**: Allow adding personal notes and custom 
   tags to any transaction.

7. **Recurring Detection**: Detect recurring transactions 
   (same merchant, similar amount, monthly) and flag them 
   as subscriptions/EMIs.

---

## SECURITY REQUIREMENTS

- All passwords bcrypt hashed with cost factor 12
- JWT tokens stored in httpOnly cookies (not localStorage)
- Rate limiting: 5 login attempts per IP per minute
- API key for Android devices is SHA-256 hashed in DB
- File uploads validated: max 10MB, only PDF/CSV MIME types
- SQL injection protection via SQLAlchemy ORM (no raw queries)
- CORS restricted to frontend domain only
- All amounts stored as integers (paise) internally to avoid 
  floating point errors, converted to rupees in API response

---

## TESTING REQUIREMENTS

### Backend Tests (pytest)
- Unit tests for SMS parser: cover 20+ real SMS formats
- Unit tests for PDF parser: test with sample bank statements
- Integration tests for all API endpoints
- Test auth flow: register, login, refresh, logout
- Test duplicate detection logic

### Frontend Tests
- Component tests with React Testing Library
- E2E tests with Playwright for critical flows:
  login → upload statement → view transactions → set budget

---

## DEPLOYMENT

### Docker Compose (local development)
```yaml
services:
  postgres:
    image: postgres:15
  redis:
    image: redis:7-alpine
  backend:
    build: ./backend
    depends_on: [postgres, redis]
  celery:
    build: ./backend
    command: celery -A app.workers.tasks worker
  frontend:
    build: ./frontend
```

### Production Checklist
- [ ] SSL/TLS via Railway/Render auto-provision
- [ ] Database connection pooling (min 5, max 20)
- [ ] Celery workers scaled to 2 minimum
- [ ] Redis maxmemory-policy: allkeys-lru
- [ ] Logs: structured JSON to Railway/Render log drain
- [ ] Health check endpoints: GET /health (backend)
- [ ] Error tracking: Sentry (both backend and frontend)
- [ ] Uptime monitoring: BetterStack or UptimeRobot

---

## DELIVERABLES

Build the app in this order:
1. FastAPI backend with all models, schemas, auth, and basic CRUD
2. SMS parser service with regex patterns for 10+ bank formats
3. Statement upload endpoint with SBI + HDFC PDF parsing
4. Gemini AI categorization service
5. All analytics endpoints
6. Next.js frontend with dashboard, transactions, upload pages
7. Budget system with alerts
8. Android Kotlin SMS receiver app
9. Docker Compose setup
10. README with setup instructions, API docs link, demo GIF

The codebase should be clean, well-commented, and follow 
production conventions. Each service should be independently 
testable. No hardcoded secrets anywhere.
```

---