from rag import retrieve_context
from schema import OutputSchema
from prompts import build_prompt
import json
import os


# ✅ Safe language detection
def safe_detect(text):
    from langdetect import detect, LangDetectException

    try:
        return detect(text)
    except LangDetectException:
        return "unknown"


# ✅ Check if text contains Arabic characters
def is_arabic(text):
    return any('\u0600' <= c <= '\u06FF' for c in text)


# ✅ Ensure Arabic reply is always present
def ensure_arabic(reply_dict):
    en = reply_dict.get("en", "").strip()
    ar = reply_dict.get("ar", "").strip()

    if not ar or not is_arabic(ar):
        return {
            "en": en if en else "We will assist you shortly.",
            "ar": "نأسف، سنقوم بمساعدتك قريبًا. يرجى التواصل مع فريق الدعم."
        }

    return reply_dict


# ✅ Call Groq model
def call_model(prompt):
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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
                    "No text outside JSON."
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


# ✅ Extract JSON safely
def extract_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return text[start:end]
    except:
        return text


# ✅ Validate output
def validate_output(raw):
    try:
        cleaned = extract_json(raw)
        data = json.loads(cleaned)
        return OutputSchema(**data)
    except Exception as e:
        print("\n⚠️ Validation Error:", e)
        print("Raw Output:", raw)
        return None


# ✅ Main pipeline
def pipeline(message):
    # Handle invalid input
    if not message.strip() or len(message) < 5:
        return {
            "error": "Input too short or invalid",
            "requires_human": True
        }

    # Language detection
    lang = safe_detect(message)

    # Retrieve context
    context = retrieve_context(message)

    # Build prompt
    prompt = build_prompt(message, context)

    # Call model
    raw = call_model(prompt)

    # Validate response
    validated = validate_output(raw)

    if not validated:
        return {
            "error": "Invalid output from model",
            "raw": raw,
            "requires_human": True
        }

    result = validated.model_dump()

    # Ensure Arabic response
    result["reply"] = ensure_arabic(result["reply"])

    return result


# ✅ CLI runner
if __name__ == "__main__":
    while True:
        message = input("\nEnter customer message: ")

        if message.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        result = pipeline(message)

        print("\nResult:")
        print(json.dumps(result, indent=2, ensure_ascii=False))