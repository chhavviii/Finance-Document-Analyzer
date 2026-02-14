## Importing libraries
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool


# -------------------------------
# 🔎 Search Tool
# -------------------------------

search_tool = SerperDevTool()


# -------------------------------
# 📄 Input Schema
# -------------------------------

class FinancialDocumentInput(BaseModel):
    path: str = Field(..., description="Path to the financial PDF document.")


# -------------------------------
# 📄 Custom PDF Reader Tool
# -------------------------------

class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads and extracts text from a financial PDF document."
    args_schema: type[BaseModel] = FinancialDocumentInput

    def _run(self, path: str) -> str:
        loader = PyPDFLoader(path)
        docs = loader.load()

        full_report = ""
        for doc in docs:
            content = doc.page_content.strip()
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            full_report += content + "\n"

        # Split into 5000-char chunks (to avoid LLM token limits)
        chunk_size = 5000
        chunks = [full_report[i:i+chunk_size] for i in range(0, len(full_report), chunk_size)]
        return "\n".join(chunks)

