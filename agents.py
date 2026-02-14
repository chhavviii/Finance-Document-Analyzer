## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()


from crewai import Agent
from crewai import LLM

from tools import FinancialDocumentTool


### Loading LLM
from crewai import LLM
import os

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)



# Creating an Experienced Financial Analyst agent
financial_analyst=Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents accurately and provide structured, fact-based insights based only on provided document content.",
    verbose=True,
    memory=False,
    backstory=(
         """
         You are an experienced financial analyst with expertise in interpreting financial statements, identifying trends, and summarizing company performance. You prioritize accuracy, obectivity, and evidence-based analysis.
         """
    ),
   tools=[FinancialDocumentTool()],
    llm=llm,
    max_iter=3,
    max_rpm=2,
    allow_delegation=True  # Allow delegation to other specialists
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="""
Determine whether the uploded document contains financial information and confirm its relevance for financial analysis.
""",
    verbose=True,
    memory=False,
    backstory=(
        """
        You specialize in reviewing documents to identify whether they contain financial data such as income statements, balance sheets, cash flow statements, or financial metrics. You base conclusions strictly on observable evidence.
"""
    ),
    tools=[FinancialDocumentTool()],
    llm=llm,
    max_iter=3,
    max_rpm=2,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Financial Risk Assessment Specialist",
    goal="""
     Identify and categorize risks explicitly mentioned in the financial document without introducing assumptions.
""",
    verbose=True,
    memory=False,
    backstory=(
        """You are a risk analysis specialist who evaluates financial, operational, and market risks based strictly on documented evidence. You avoid exaggeration and unsupported claims."""
    ),
    tools=[FinancialDocumentTool()],
    llm=llm,
    max_iter=3,
    max_rpm=2,
    allow_delegation=False
)


investment_advisor = Agent(
    role="Investment Insights Specialist",
    goal="""Provide balanced investment insights based only on the financial analysis and identified risks, without exaggeration or speculation.""",
    verbose=True,
    memory=False,
    backstory=(
        """
        You provide professional, neutral investment insights. You do not fabricate data and you avoid making aggressuive buy/sell recommendations. Your recommendations are balanced and supported by document-based reasoning.

"""
    ),
    tools=[FinancialDocumentTool()],
    llm=llm,
    max_iter=3,
    max_rpm=2,
    allow_delegation=False
)
