# Mumzworld AI Support Agent

A multilingual AI customer support triage system built for the Mumzworld AI Engineering Intern assignment.

This system processes free-form customer support messages, classifies intent, assigns urgency, and generates grounded customer-facing responses in both English and Arabic.

It is designed to demonstrate practical AI engineering: structured outputs, multilingual handling, retrieval grounding, schema validation, and safe fallback behavior.

---

## Features

- Multilingual customer support triage (English + Arabic)
- Intent classification
- Urgency detection
- Confidence scoring
- Grounded responses using FAQ context
- Structured JSON output
- Human escalation for uncertain or invalid cases
- Streamlit UI for interactive testing

---

## Project Structure

```bash
mumzworld-ai-support-agent/
│
├── app.py                # Main pipeline
├── streamlit_app.py      # Streamlit UI
├── rag.py                # FAQ retrieval
├── prompts.py            # Prompt builder
├── schema.py             # Output schema validation
├── requirements.txt      # Dependencies
├── .gitignore
│
├── data/
│   └── faq.txt           # Knowledge base
│
├── README.md
├── EVALS.md
├── TRADEOFFS.md
└── LICENSE

Architecture

The system follows a lightweight modular AI pipeline:

Input Processing
Accepts free-form customer messages.
Language Detection
Safely detects input language with fallback for malformed text.
Context Retrieval (RAG)
Retrieves support context from a lightweight FAQ knowledge base.
Prompt Construction
Builds a strict prompt with grounding and structured output constraints.
LLM Inference
Uses Groq with Llama 3.3 70B for fast multilingual inference.
Validation + Post-processing
Validates JSON output with Pydantic and enforces Arabic fallback.
Tech Stack
Python
Groq API
Llama 3.3 70B
Streamlit
Pydantic
Langdetect
How to Run
1. Clone the repository
git clone https://github.com/wildtigress/mumzworld-ai-support-agent.git
cd mumzworld-ai-support-agent

2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Set API key
setx GROQ_API_KEY "your_api_key_here"

Restart terminal after setting the key.

5. Run CLI
python app.py
6. Run Streamlit UI
streamlit run streamlit_app.py
Example Output
{
  "intent": "refund",
  "urgency": "medium",
  "confidence": 0.85,
  "language": "en",
  "reasoning": "User reports damaged product and requests refund",
  "reply": {
    "en": "We’re sorry your item arrived damaged. Please share images and we will process your refund.",
    "ar": "نأسف لأن المنتج وصل تالفًا. يرجى إرسال الصور وسنقوم بمعالجة طلب الاسترجاع."
  },
  "requires_human": false
}
Safety and Robustness

This system includes:

Safe language detection
Schema validation
JSON extraction
Arabic response enforcement
Human escalation for invalid or uncertain inputs

This prevents crashes, hallucinations, and malformed outputs.

Limitations
Retrieval uses simple FAQ lookup instead of semantic search
No vector database
No persistent memory or feedback loop
No fine-tuning

These were intentional tradeoffs to prioritize reliability, simplicity, and speed.

Submission Links
GitHub Repository: https://github.com/wildtigress/mumzworld-ai-support-agent
Loom Walkthrough: [https://www.loom.com/share/629843dc62584200a24c822b6bbbf855]
License

This project is licensed under the MIT License.
See the LICENSE file for details.
