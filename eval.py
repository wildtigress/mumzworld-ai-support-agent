from app import pipeline

test_cases = [
    {"input": "I want to return my order", "expected_intent": "return"},
    {"input": "Where is my refund?", "expected_intent": "refund"},
    {"input": "asdasdasd", "expected_intent": "unknown"},
    {"input": "هل يمكنني إرجاع المنتج؟", "expected_intent": "return"},
]

def run_eval():
    correct = 0

    for case in test_cases:
        result = pipeline(case["input"])
        predicted = result.get("intent")

        if predicted == case["expected_intent"]:
            correct += 1
        else:
            print(f"❌ Failed: {case['input']}")
            print(f"Expected: {case['expected_intent']}, Got: {predicted}")

    print(f"\n✅ Accuracy: {correct}/{len(test_cases)}")

if __name__ == "__main__":
    run_eval()