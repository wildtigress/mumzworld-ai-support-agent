from rag import retrieve_context
from schema import OutputSchema
from prompts import build_prompt
import json
import os


# ---------------------------
# Language Detection
# ---------------------------
def safe_detect(text):
    from langdetect import detect, LangDetectException
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"


def is_arabic(text):
    return any('\u0600' <= c <= '\u06FF' for c in text)


def ensure_arabic(reply_dict):
    en = reply_dict.get("en", "").strip()
    ar = reply_dict.get("ar", "").strip()

    if not ar or not is_arabic(ar):
        return {
            "en": en if en else "We will assist you shortly.",
            "ar": "نأسف، سنقوم بمساعدتك قريبًا. يرجى التواصل مع فريق الدعم."
        }

    return reply_dict


# ---------------------------
# Confidence (ENGINEERED)
# ---------------------------
def compute_confidence(context, requires_human):
    if context == "NO_RELEVANT_CONTEXT":
        return 0.3
    if requires_human:
        return 0.4
    return 0.85


# ---------------------------
# Intent Normalization
# ---------------------------
def normalize_intent(intent: str):
    intent = intent.lower()

    if "return" in intent:
        return "return"
    if "refund" in intent:
        return "refund"

    return "unknown"


# ---------------------------
# Model Call
# ---------------------------
def call_model(prompt, lang):
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    if lang == "ar":
        system_lang = "Respond ONLY in fluent Arabic."
    else:
        system_lang = "Respond ONLY in fluent English."

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict AI assistant.\n"
                    "Return ONLY valid JSON.\n"
                    "Always include BOTH English and Arabic replies.\n"
                    "Never leave fields empty.\n"
                    "If unsure, set requires_human=true.\n"
                    "No text outside JSON.\n"
                    + system_lang
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# ---------------------------
# JSON Extraction
# ---------------------------
def extract_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return text[start:end]
    except:
        return text


# ---------------------------
# Validation
# ---------------------------
def validate_output(raw):
    try:
        cleaned = extract_json(raw)
        data = json.loads(cleaned)
        return OutputSchema(**data)
    except Exception as e:
        print("\n⚠️ Validation Error:", e)
        print("Raw Output:", raw)
        return None


# ---------------------------
# PIPELINE
# ---------------------------
def pipeline(message):

    # Input validation
    if not message.strip() or len(message) < 5:
        return {
            "intent": "unknown",
            "reasoning": "Invalid input",
            "reply": {
                "en": "Please provide a valid message.",
                "ar": "يرجى إدخال رسالة صحيحة."
            },
            "requires_human": True,
            "confidence": 0.3
        }

    # Detect language
    lang = safe_detect(message)

    # Retrieve context
    context = retrieve_context(message)

    # 🔥 HARD FAIL IF NO CONTEXT
    if context == "NO_RELEVANT_CONTEXT":
        return {
            "intent": "unknown",
            "reasoning": "No relevant policy found",
            "reply": {
                "en": "I'm not sure about this. Let me connect you to a human agent.",
                "ar": "لست متأكدًا من هذا. سأقوم بتحويلك إلى موظف دعم."
            },
            "requires_human": True,
            "confidence": 0.3
        }

    # Build prompt
    prompt = build_prompt(message, context)

    # Call model
    raw = call_model(prompt, lang)

    # Validate response
    validated = validate_output(raw)

    # 🔥 FIXED FALLBACK (correct placement)
    if not validated:
        return {
            "intent": "unknown",
            "reasoning": "Model output invalid",
            "reply": {
                "en": "Let me connect you to a human agent.",
                "ar": "سأقوم بتحويلك إلى موظف دعم."
            },
            "requires_human": True,
            "confidence": 0.3
        }

    result = validated.model_dump()

    # 🔥 Normalize intent
    result["intent"] = normalize_intent(result["intent"])

    # Ensure Arabic correctness
    result["reply"] = ensure_arabic(result["reply"])

    # 🔥 Add real confidence
    result["confidence"] = compute_confidence(context, result["requires_human"])

    return result


# ---------------------------
# CLI RUNNER
# ---------------------------
if __name__ == "__main__":
    while True:
        message = input("\nEnter customer message: ")

        if message.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        result = pipeline(message)

        print("\nResult:")
        print(json.dumps(result, indent=2, ensure_ascii=False))