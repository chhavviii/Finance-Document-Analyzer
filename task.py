## Importing libraries and files
from crewai import Task, Crew

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query
verification = Task(
    description="""
You are responsible for verifying whether the uploaded document is a financial document.

The document is located at: {file_path}

Steps:
1. Use the Financial Document Reader tool to read the document located at {file_path}.
2. Identify whether it contains financial information such as:
   - Revenue
   - Profit or Loss
   - Expenses
   - Assets or Liabilities
   - Financial Ratios
   - Cash Flow statements
3. If financial data is present, analyze it to extract key insights such as:
   - Trends in revenue or profit
   - Financial health indicators
   - Investment opportunities or risks
4. If not, clearly state that it is not a financial document. Do not speculate or infer market relevance.
5. Base your conclusion strictly on the content of the document.
""",

    expected_output="""
Output format:
- Document Type: [Financial Document / Not a Financial Document]
- Key Financial Insights: [List of insights if it's a financial document, otherwise N/A]
- Evidence: Key phrases or indicators found in the document
- Short Justification: A brief explanation based strictly on the document content
""",

    agent=verifier,
    tools=[FinancialDocumentTool()],
    async_execution=False,
)

analyze_financial_document = Task(
    description="""
    Analyze the financial document located at {file_path}.

User query: {query}

Document content:
{chunk_text}

Extract key financial metrics and summarize performance.
Do not fabricate information.
    # """,
    expected_output="""
    Provide a structured analysis:

    1. Executive Summary
    2. Key Financial Metrics
    3. Performance Analysis
    4. Observed Trends
    5. Response to User Query
    """,
    agent=financial_analyst,
   tools=[FinancialDocumentTool()],
    async_execution=False,
)
## Creating a risk assessment task
risk_assessment = Task(
    description="""
    Assess the risks mentioned in the financial document located at {file_path}.

    Instructions:
    1. Identify risks explicitly mentioned in the document.
    2. Categorize risks into types such as:
    -Operational Risk
    -Financial Risk
    -Market Risk
    -Regulatory Risk
    3. Do not invent risks.
    4. If risks are not clearly mentioned, state that the document does not provide sufficient information for risk assessment.
    5. Provide evidence from the document to support each identified risk.    
""",

    expected_output="""Output format:
    -Risk Category
    -Description
    -Supporting Evidence
    -Risk Level (Low/Medium/High based only on document context)""",

    agent=risk_assessor,
    tools=[FinancialDocumentTool()],
    async_execution=False,
)
## Creating an investment analysis task
investment_analysis = Task(
    description="""

Provide a balanced investment insight based only on the financial analysis and risk assessment derived from the document at {file_path}.

Instructions:
1. Do not fabricate numbers.
2. Do not exaggerate claims.
3. Provide a neutral, professional summary.
4. Consider both strengths and risks. 
5. Avoid making definitive buy/sell recommendations.
6. Include a short disclaimer stating that this is not financial advice.

""",

    expected_output="""Output format:
    1. Investment Insight Summary(Positive/ Neutral/ Cautious)
    2. Supporting Strengths
    3. Key Risks
    4. Balanced Conclusion
    5. Disclaimer""",

    agent=investment_advisor,
    tools=[FinancialDocumentTool()],
    async_execution=False,
)



    
