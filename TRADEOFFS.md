
---

## `TRADEOFFS.md`

```md
# Tradeoffs and Design Decisions

This project was designed to prioritize reliability, clarity, and fast iteration within the scope of the assignment.

The goal was not to build the most complex system possible, but to build a robust and practical AI support pipeline that demonstrates sound engineering judgment.

---

## 1. Model Choice: Groq + Llama 3.3 70B

### Choice
Used Groq with Llama 3.3 70B for inference.

### Why
- Fast inference speed
- Good multilingual support
- No credit card required
- Easy setup for reproducible testing
- Strong enough for structured support tasks

### Tradeoff
This is not the most controllable production setup compared to fine-tuned hosted models, but it is significantly faster to iterate and easier to reproduce.

---

## 2. Retrieval Strategy: Simple FAQ RAG

### Choice
Used a lightweight FAQ text file (`faq.txt`) as the retrieval layer.

### Why
- Simple
- Fast
- Transparent
- Easy to debug
- Sufficient for assignment scope

### Tradeoff
This is less scalable than semantic retrieval using embeddings and vector search, but simpler and more interpretable for a small knowledge base.

In production, this would be upgraded to embedding-based retrieval with ranking.

---

## 3. Structured Outputs with Schema Validation

### Choice
Used strict JSON output with Pydantic schema validation.

### Why
- Predictable outputs
- Easier downstream integration
- Prevents malformed responses
- Production-friendly

### Tradeoff
Strict schema constraints reduce flexibility, but greatly improve reliability and observability.

---

## 4. Multilingual Strategy

### Choice
Generated both English and Arabic responses for every valid interaction.

### Why
- Matches Mumzworld’s multilingual customer base
- Improves accessibility
- Demonstrates multilingual robustness

### Tradeoff
Always generating bilingual output increases token usage, but ensures consistent multilingual support and simplifies UI behavior.

---

## 5. Arabic Fallback Enforcement

### Choice
Enforced Arabic output at three levels:
1. Prompt constraints
2. System constraints
3. Post-processing fallback

### Why
LLMs may occasionally omit or degrade multilingual outputs. This fallback ensures reliability.

### Tradeoff
Fallback Arabic may be less context-rich than model-generated Arabic, but guarantees non-empty multilingual output.

---

## 6. Human Escalation Strategy

### Choice
Used `requires_human = true` for uncertain, invalid, or out-of-scope requests.

### Why
Safer than hallucinating
More realistic for customer support systems
Improves trust and production readiness

### Tradeoff
This may escalate more often than necessary, but is preferable to incorrect automation.

---

## 7. UI Choice: Streamlit

### Choice
Used Streamlit for the demo interface.

### Why
- Fast to build
- Easy to demo
- Good for interactive testing
- Minimal overhead

### Tradeoff
Not suitable for full production frontend, but ideal for prototyping and reviewer evaluation.

---

## 8. What Was Intentionally Not Included

The following were intentionally omitted to prioritize clarity and execution speed:

- Vector database
- Embedding search
- Fine-tuning
- Agentic tool use
- Persistent user memory
- Feedback learning loop
- Authentication / production deployment

These are valid next steps, but not required to demonstrate core AI engineering ability in this assignment.

---

## Final Tradeoff Summary

This project intentionally prioritizes:

- Reliability over complexity
- Interpretability over abstraction
- Fast iteration over infrastructure
- Safe fallbacks over aggressive automation

These tradeoffs were chosen to produce a robust, testable, and reviewer-friendly AI system within assignment scope.