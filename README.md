# Financial Document Analysis API

This is a FastAPI backend that analyzes uploaded financial PDF documents and generates investment insights using CrewAI and Groq LLM.

The goal of this project was not only to build the API, but also to debug and stabilize a multi-agent LLM pipeline under real-world constraints like token limits, model deprecation, and rate limiting.

---

# What This API Does

1. Accepts a financial PDF file.
2. Extracts text from the document.
3. Sends the content to a CrewAI agent.
4. Uses Groq LLM to generate structured investment insights.
5. Returns the result as JSON.

Main endpoint:

```
POST /analyze
```

---

# Bugs Found & How I Fixed Them

During development, several issues occurred. Below is the actual debugging journey.

---

## 1. Model Decommission Error

### Issue

Initially, the system failed with:

```
The model `llama3-8b-8192` has been decommissioned
```

### Cause

Groq had deprecated the model being used in the configuration.

### Fix

Updated the model to:

```
groq/llama-3.1-8b-instant
```

After this change, LLM calls started working again.

---

## 2. Empty / Invalid LLM Response

### Issue

The API returned:

```
Invalid response from LLM call - None or empty
```

### Cause

- Incorrect LLM configuration
- API key not properly loaded
- Model provider prefix missing (`groq/`)

### Fix

- Verified `GROQ_API_KEY` environment variable
- Corrected model naming format
- Added validation to ensure non-empty response before returning

This stabilized the output generation.

---

## 3. Token Explosion (Request Too Large)

### Issue

The server started returning 500 errors:

```
Request too large for model
```

or

```
RateLimitError: Limit 6000 TPM
```

### Cause

The full extracted PDF text was being passed directly into the LLM along with verbose system prompts.

This exceeded Groq's free tier token limits (6000 tokens per minute).

### Fix

- Implemented text truncation before sending to LLM
- Reduced prompt verbosity
- Simplified agent instructions
- Removed unnecessary multi-agent chaining

After reducing the input size, the API handled moderate-size PDFs correctly.

---

## 4. Deterministic Output Instability

### Issue

Sometimes the agent returned incomplete analysis or inconsistent structure.

### Cause

Prompts were too open-ended and did not strictly define the expected output format.

### Fix

- Added clear output formatting instructions
- Simplified the agent’s role
- Ensured structured response expectation

This made the responses more predictable.

---

## 5. Rate Limit Errors (Groq Free Tier)

### Issue

Frequent 500 errors caused by:

```
RateLimitError: Limit 6000 TPM reached
```

### Cause

Groq free tier enforces strict Tokens Per Minute limits.

Large documents triggered this quickly.

### Fix

- Reduced input size
- Documented limitation clearly
- Avoided unnecessary repeated LLM calls

Note: Very large documents may still hit free tier limits.

---

## 6. API Endpoint Confusion

### Issue

Confusion between:

```
/docs#/default/analyze_document_analyze_post
```

and

```
/analyze
```

### Cause

`/docs` is the Swagger UI documentation route.

The actual API endpoint is:

```
POST /analyze
```

### Fix

Clarified usage in documentation.

---

# Setup Instructions

Follow these steps to run locally.

---

## 1. Clone the repository

```
git clone <your-repo-link>
cd financial-document-analysis
```

---

## 2. Create virtual environment

```
python -m venv venv
```

Activate:

Windows:
```
venv\Scripts\activate
```

Mac/Linux:
```
source venv/bin/activate
```

---

## 3. Install dependencies

```
pip install -r requirements.txt
```

Note:

CrewAI is intentionally locked to:

```
crewai==0.130.0
```

as required in the assignment instructions.

---

## 4. Set API key

Windows:
```
set GROQ_API_KEY=your_api_key_here
```

Mac/Linux:
```
export GROQ_API_KEY=your_api_key_here
```

---

## 5. Run the server

```
uvicorn main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

for Swagger testing.

---

# API Documentation

## Endpoint

```
POST /analyze
```

## Description

Uploads a financial PDF and returns investment insights.

## Request Type

`multipart/form-data`

### Parameters

- `file` (PDF, required) – Financial document
- `query` (string, required) – Instruction for analysis

---

## Example cURL Request

```
curl -X POST \
  'http://127.0.0.1:8000/analyze' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@test.pdf;type=application/pdf' \
  -F 'query=Analyze this financial document for investment insights'
```

---

## Example Success Response

```
{
  "analysis": "Structured investment insights extracted from the document..."
}
```

---

## Possible Errors

500 Internal Server Error may occur if:

- Document is too large
- Groq rate limit exceeded
- API key invalid
- Unexpected LLM failure

---

# Known Limitations

- Groq free tier TPM limits apply.
- Large PDFs may require manual size reduction.
- No automatic retry mechanism implemented.
- Not optimized for batch document processing.

---

# Summary

This project demonstrates:

- Building an LLM-powered FastAPI backend
- Managing token limits and rate limits
- Debugging real-world model deprecation issues
- Stabilizing prompt design for consistent output
- Documenting API usage clearly

---
