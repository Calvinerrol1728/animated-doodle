# -*- coding: utf-8 -*-
"""
Exact text content for the MONTHLY BUDGET PLANNER.

Every string is rendered verbatim into the PDF. Nothing is paraphrased.
No invented figures, no financial advice, no guarantees.
"""

TITLE = "MONTHLY BUDGET PLANNER"
SUBTITLE = "A Simple & Beautiful Way to Organize Your Money"
TAGLINE = "Plan  \u2022  Track  \u2022  Save  \u2022  Grow"

BELONGS = {
    "title": "THIS PLANNER BELONGS TO",
    "fields": ["Name:", "Year:", "My financial focus this year:"],
    "quote": "\u201cSmall steps, consistently taken, can create meaningful change.\u201d",
}

WELCOME = {
    "title": "WELCOME TO YOUR MONTHLY BUDGET PLANNER",
    "body": [
        "Budgeting is not about restriction. It is about understanding where your "
        "money goes, planning intentionally, and creating a system that fits your "
        "own lifestyle.",
        "This planner gives you a clear place to record what comes in, plan what "
        "goes out, track what actually happens, and adjust as you learn.",
    ],
    "principles": [
        ("PLAN", "Know what is coming in and what needs to go out."),
        ("TRACK", "Pay attention to where your money actually goes."),
        ("REFLECT", "Learn from each month and adjust your plan."),
    ],
    "quote": "\u201cA budget is a plan for your money, not a punishment "
             "for spending it.\u201d",
}

HOWTO = {
    "title": "HOW TO USE YOUR PLANNER",
    "steps": [
        "Record your expected income.",
        "Plan your essential expenses.",
        "Set savings and financial goals.",
        "Track your actual spending.",
        "Review your month and make adjustments.",
    ],
    "quote": "\u201cYour budget doesn\u2019t need to be perfect. "
             "It needs to be useful.\u201d",
}

VISION = {
    "title": "MY FINANCIAL VISION",
    "prompts": [
        "What do I want my money to help me accomplish?",
        "What would financial peace look like for me?",
        "What am I working toward?",
        "Why does financial organization matter to me?",
    ],
}

GOALS = {
    "title": "MY FINANCIAL GOALS",
    "sections": ["SHORT-TERM GOAL", "MEDIUM-TERM GOAL", "LONG-TERM GOAL"],
    "fields": ["Goal:", "Target Amount:", "Target Date:", "Why it matters:"],
}

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

YEAR_VIEW = {
    "title": "MY YEAR AT A GLANCE",
    "cols": ["MONTH", "INCOME", "EXPENSES", "SAVINGS", "NOTES"],
}

MONTH_OVERVIEW = {
    "title": "MONTHLY OVERVIEW",
    "fields": ["MONTH:", "MONTHLY FOCUS:", "TOP FINANCIAL GOAL:",
               "EXPECTED INCOME:", "SAVINGS TARGET:", "SPENDING LIMIT:"],
    "calendar_note": "IMPORTANT FINANCIAL DATES",
}

INCOME = {
    "title": "INCOME TRACKER",
    "cols": ["DATE", "INCOME SOURCE", "EXPECTED", "ACTUAL", "NOTES"],
    "widths": [0.13, 0.32, 0.16, 0.16, 0.23],
    "rows": 14,
    "totals": ["TOTAL EXPECTED INCOME:", "TOTAL ACTUAL INCOME:"],
}

FIXED = {
    "title": "FIXED EXPENSES",
    "cols": ["EXPENSE", "DUE DATE", "BUDGETED", "ACTUAL", "PAID"],
    "widths": [0.34, 0.16, 0.17, 0.17, 0.16],
    "examples": ["Rent / Mortgage", "Utilities", "Internet", "Insurance",
                 "Subscriptions", "Loan Payments", "Other"],
    "extra_rows": 7,
}

VARIABLE = {
    "title": "VARIABLE EXPENSES",
    "categories": ["FOOD", "TRANSPORTATION", "SHOPPING",
                   "ENTERTAINMENT", "PERSONAL", "OTHER"],
    "fields": ["BUDGETED", "ACTUAL", "DIFFERENCE"],
}

BUDGET = {
    "title": "MY MONTHLY BUDGET",
    "cols": ["CATEGORY", "PLANNED", "ACTUAL", "DIFFERENCE"],
    "widths": [0.40, 0.20, 0.20, 0.20],
    "sections": ["INCOME", "HOUSING", "UTILITIES", "FOOD", "TRANSPORTATION",
                 "HEALTH", "PERSONAL", "ENTERTAINMENT", "DEBT", "SAVINGS", "OTHER"],
    "total": "TOTAL",
}

NEEDS_WANTS = {
    "title": "NEEDS VS. WANTS",
    "needs_title": "MY NEEDS",
    "needs_examples": ["Housing", "Food", "Utilities", "Transportation",
                       "Essential personal expenses"],
    "wants_title": "MY WANTS",
    "wants_examples": ["Entertainment", "Dining out", "Shopping", "Hobbies",
                       "Optional subscriptions"],
    "prompt": "\u201cIs there one want I can reduce this month to support "
              "a bigger goal?\u201d",
}

BILLS = {
    "title": "BILL PAYMENT TRACKER",
    "cols": ["BILL", "DUE DATE", "AMOUNT", "PAID DATE", "STATUS"],
    "widths": [0.30, 0.16, 0.17, 0.18, 0.19],
    "rows": 18,
    "note": "\u201cMark each bill as you pay it.\u201d",
}

SUBS = {
    "title": "SUBSCRIPTION CHECKUP",
    "cols": ["SUBSCRIPTION", "MONTHLY COST", "RENEWAL DATE",
             "KEEP / CANCEL", "NOTES"],
    "widths": [0.26, 0.17, 0.18, 0.17, 0.22],
    "rows": 14,
    "prompts": ["\u201cWhich subscriptions are genuinely useful to me?\u201d",
                "\u201cWhich ones could I live without?\u201d"],
}

SAVINGS_GOALS = {
    "title": "MY SAVINGS GOALS",
    "fields": ["GOAL:", "TARGET AMOUNT:", "CURRENT SAVINGS:", "DEADLINE:"],
    "count": 3,
    "notes": "NOTES",
}

CHALLENGE = {
    "title": "MY SAVINGS CHALLENGE",
    "target": "MY 30-DAY TARGET:",
    "cols": ["DAY", "AMOUNT SAVED", "TOTAL SAVED"],
}

EMERGENCY = {
    "title": "EMERGENCY FUND",
    "prompts": ["My current emergency fund:", "My target amount:",
                "My monthly contribution:"],
    "quote": "\u201cProgress is progress, even when the amount feels small.\u201d",
}

DEBT = {
    "title": "DEBT TRACKER",
    "cols": ["DEBT", "STARTING BALANCE", "CURRENT BALANCE", "MINIMUM PAYMENT",
             "EXTRA PAYMENT", "DUE DATE", "NOTES"],
    "widths": [0.17, 0.14, 0.14, 0.14, 0.13, 0.12, 0.16],
    "rows": 12,
    "totals": ["TOTAL DEBT:", "TOTAL PAID THIS MONTH:"],
}

DEBT_PLAN = {
    "title": "MY DEBT PAYMENT PLAN",
    "sections": ["DEBT #1", "DEBT #2", "DEBT #3"],
    "fields": ["Balance:", "Minimum Payment:", "Extra Payment:", "Target Date:"],
    "quote": "\u201cFocus on progress, consistency, and a plan that fits "
             "your budget.\u201d",
}

WEEKLY = {
    "titles": ["WEEK 1 \u2014 SPENDING TRACKER", "WEEK 2 \u2014 SPENDING TRACKER",
               "WEEK 3 \u2014 SPENDING TRACKER", "WEEK 4 \u2014 SPENDING TRACKER"],
    "cols": ["DATE", "WHAT I SPENT ON", "CATEGORY", "AMOUNT",
             "NEED / WANT", "NOTES"],
    "widths": [0.11, 0.26, 0.16, 0.13, 0.15, 0.19],
    "rows": 20,
}

NO_SPEND = {
    "title": "NO-SPEND CHALLENGE",
    "cols": ["DAY", "NO-SPEND DAY", "WHAT I DID INSTEAD", "MONEY I KEPT"],
    "reflection": "\u201cWhat did I learn from spending less?\u201d",
}

GROCERY = {
    "title": "GROCERY & MEAL BUDGET",
    "top": ["GROCERY BUDGET", "ACTUAL SPENDING", "DIFFERENCE"],
    "days": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY",
             "SATURDAY", "SUNDAY"],
    "list_title": "GROCERY LIST",
}

SHOPPING = {
    "title": "SHOPPING PLANNER",
    "cols": ["ITEM", "PRICE", "NEED / WANT", "PRIORITY", "PURCHASED"],
    "widths": [0.34, 0.15, 0.18, 0.16, 0.17],
    "rows": 18,
    "prompt": "\u201cBefore buying, ask: Do I need it? Do I love it? "
              "Does it fit my budget?\u201d",
}

TRIGGERS = {
    "title": "UNDERSTANDING MY SPENDING",
    "prompts": [
        "When am I most likely to overspend?",
        "What emotions influence my spending?",
        "What purchases do I regret most often?",
        "What usually helps me pause before buying?",
    ],
}

HABITS = {
    "title": "MY MONEY HABITS",
    "keep": "HABITS I WANT TO KEEP",
    "change": "HABITS I WANT TO CHANGE",
    "new": "ONE NEW MONEY HABIT I WILL PRACTICE THIS MONTH:",
}

CHECKIN = {
    "title": "WEEKLY MONEY CHECK-IN",
    "sections": [("WEEK 1", "How did I do?"), ("WEEK 2", "What changed?"),
                 ("WEEK 3", "What did I learn?"), ("WEEK 4", "What will I improve?")],
}

REVIEW = {
    "title": "MONTH-END BUDGET REVIEW",
    "cols": ["CATEGORY", "PLANNED", "ACTUAL", "DIFFERENCE"],
    "widths": [0.40, 0.20, 0.20, 0.20],
    "rows": ["Income", "Housing", "Utilities", "Food", "Transportation",
             "Personal", "Entertainment", "Debt", "Savings", "Other"],
    "totals": ["TOTAL INCOME", "TOTAL EXPENSES", "TOTAL SAVINGS"],
}

WHERE = {
    "title": "WHERE DID MY MONEY GO?",
    "categories": ["Housing", "Food", "Transportation", "Bills", "Personal",
                   "Entertainment", "Debt", "Savings", "Other"],
    "cols": ["CATEGORY", "AMOUNT", "PERCENTAGE"],
}

SAVINGS_REVIEW = {
    "title": "MY SAVINGS REVIEW",
    "prompts": ["How much did I plan to save?", "How much did I actually save?",
                "What helped me save?", "What made saving difficult?",
                "What can I change next month?"],
}

WINS = {
    "title": "CELEBRATE YOUR FINANCIAL WINS",
    "prompts": ["Something I saved for:", "A purchase I avoided:",
                "A bill I paid on time:", "A financial habit I improved:",
                "Something I\u2019m proud of:"],
}

REFLECTION = {
    "title": "MONTHLY MONEY REFLECTION",
    "prompts": ["What worked well this month?", "What didn\u2019t work?",
                "Where did I overspend?", "Where did I make progress?",
                "What surprised me?", "What will I do differently next month?"],
}

NEXT_MONTH = {
    "title": "NEXT MONTH\u2019S MONEY PLAN",
    "sections": ["MY TOP FINANCIAL PRIORITY", "MY SAVINGS TARGET",
                 "MY SPENDING LIMIT", "A BILL I NEED TO PREPARE FOR",
                 "A FINANCIAL GOAL I WANT TO WORK TOWARD",
                 "ONE MONEY HABIT I WILL PRACTICE"],
}

DASHBOARD = {
    "title": "MY FINANCIAL DASHBOARD",
    "tiles": ["TOTAL INCOME", "TOTAL EXPENSES", "TOTAL SAVINGS",
              "TOTAL DEBT PAYMENT", "SAVINGS RATE", "BIGGEST EXPENSE"],
    "wide": ["BIGGEST FINANCIAL WIN", "MAIN FOCUS FOR NEXT MONTH"],
}

MASTER = {
    "title": "MY MONEY GOALS",
    "cols": ["GOAL", "TARGET AMOUNT", "TARGET DATE", "PROGRESS", "PRIORITY"],
    "widths": [0.34, 0.17, 0.16, 0.17, 0.16],
    "rows": 12,
}

RESET = {
    "title": "MY FINANCIAL RESET",
    "items": ["Review my income", "Review my expenses",
              "Cancel unnecessary subscriptions", "Check upcoming bills",
              "Update savings goals", "Review debt payments",
              "Review spending habits", "Set next month\u2019s budget",
              "Choose one financial priority", "Celebrate my progress"],
    "quote": "\u201cA fresh month is another opportunity to make "
             "intentional choices.\u201d",
}

FINAL = {
    "statement": "\u201cMY MONEY HAS A PLAN.\u201d",
    "body": "\u201cI don\u2019t need to have everything figured out. I can make "
            "thoughtful choices, learn from each month, and keep moving toward "
            "the life I want.\u201d",
    "prompts": ["My biggest financial lesson:", "My next financial goal:",
                "One promise I am making to myself:"],
}
