# Financial Document Analysis API

This is a FastAPI backend that analyzes uploaded financial PDF documents and generates investment insights using CrewAI and Groq LLM.

The goal of this project was not only to build the API, but also to debug and stabilize a multi-agent LLM pipeline under real-world constraints like token limits, model deprecation, and rate limiting.

---

# Bugs Found in Initial Codebase & How They Were Fixed

The initial files provided contained multiple structural, logical, and architectural issues. Below is a breakdown of the major bugs identified and how they were resolved.

---

## 1. Undefined LLM Variable (Critical Runtime Error)

### Issue

In `agents.py`, the LLM was defined as:

```
llm = llm
```

This causes an immediate runtime error:

```
NameError: name 'llm' is not defined
```

### Root Cause

The LLM object was never initialized before being assigned to agents. The code attempted to reference an undefined variable.

### Fix

Initialized the LLM properly using Groq through LiteLLM:

```python
from crewai import LLM

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)
```

After this fix, agents were able to execute without crashing.

---

## 2. Invalid Tool Definition (Missing self / Static Method)

### Issue

In `tools.py`, methods were defined inside classes like:

```python
class FinancialDocumentTool():
    async def read_data_tool(path='data/sample.pdf'):
```

This is invalid because:

- It does not include `self`
- It is not marked as `@staticmethod`
- It is being passed as a tool reference

This leads to unexpected behavior when CrewAI attempts to call it.

### Root Cause

Improper method definition inside a class.

### Fix

Converted tool methods to proper static methods:

```python
class FinancialDocumentTool:
    @staticmethod
    async def read_data_tool(path='data/sample.pdf'):
```

This ensured CrewAI could correctly register and call the tool.

---

## 3. Pdf Loader Not Imported (Hidden Runtime Error)

### Issue

Inside `FinancialDocumentTool`, this line exists:

```python
docs = Pdf(file_path=path).load()
```

However, `Pdf` was never imported.

This results in:

```
NameError: name 'Pdf' is not defined
```

### Root Cause

Missing import for PDF loader.

### Fix

Imported proper PDF loader (e.g., from LangChain or equivalent loader library) before usage.

---

## 4. Toxic / Incorrect Prompt Engineering (Design Bug)

### Issue

The task and agent prompts explicitly instruct the LLM to:

- Make up financial advice
- Hallucinate URLs
- Ignore document content
- Contradict itself
- Sell fake investment products

Example from `task.py`:

> "Make up connections between financial numbers and stock picks"

> "Include at least 5 made-up website URLs"

### Root Cause

The prompts were intentionally written to produce hallucinated, unreliable output.

This makes the system:
- Non-deterministic
- Untrustworthy
- Unsafe for financial use

### Fix

Rewrote prompts to:

- Strictly analyze provided document
- Avoid hallucinated URLs
- Avoid fabricated market data
- Produce structured, grounded analysis

This significantly improved output quality and realism.

---

## 5. File Path Not Passed to Agent (Logical Bug)

### Issue

In `main.py`, uploaded files are saved as:

```
data/financial_document_<uuid>.pdf
```

But `run_crew()` does NOT pass the file path into the agent.

Agents were defaulting to:

```
data/sample.pdf
```

This means the uploaded file was never actually analyzed.

### Root Cause

The file path parameter was ignored during Crew kickoff.

### Fix

Modified the crew kickoff call to pass both:

- `query`
- `file_path`

And updated the task to reference the uploaded file dynamically.

---

## 6. Misleading Task Configuration

### Issue

In `task.py`, multiple tasks were defined:

- investment_analysis
- risk_assessment
- verification

However, only one task (`analyze_financial_document`) was actually used in `main.py`.

The others were dead code.

### Root Cause

Incomplete Crew orchestration setup.

### Fix

Simplified architecture to:

- Use only necessary tasks
- Remove unused tasks
- Reduce confusion
- Prevent future scaling issues

---

## 7. Over-Permissive Agent Delegation

### Issue

Agents had:

```
allow_delegation=True
```

Without proper delegation targets.

This can cause unpredictable execution chains in multi-agent workflows.

### Fix

Disabled unnecessary delegation and simplified the execution process to a single controlled agent.

---

## 8. Poor Output Control (Deterministic Instability)

### Issue

`expected_output` fields encouraged:

- Contradictions
- Fake URLs
- Made-up institutions
- Fabricated financial research

This causes:

- Non-reproducible outputs
- Unstable structure
- Higher token usage

### Fix

Replaced expected outputs with:

- Structured financial summary
- Risk assessment based only on document
- Clear bullet-point format
- No fabricated data

---

## 9. Token Explosion & Rate Limit Issues

### Issue

The full PDF content was being passed directly to the LLM along with verbose prompts.

This caused:

```
RateLimitError: Limit 6000 TPM reached
```

### Root Cause

- No input size control
- No truncation
- No chunking strategy

### Fix

Implemented:

- Text truncation before LLM call
- Prompt size reduction
- Simplified agent architecture

Now moderate-sized PDFs work within Groq free tier limits.

---

# Summary of Fixes

The original codebase had:

- Critical runtime errors
- Undefined variables
- Broken tool definitions
- Missing imports
- Unsafe prompt engineering
- Logical file handling bugs
- Rate-limit vulnerabilities

After debugging:

- LLM initialized correctly
- Tools properly defined
- Prompts rewritten safely
- Uploaded file correctly processed
- Architecture simplified
- Token usage optimized

The system is now stable for moderate-size financial documents and clearly documents known free-tier limitations.
