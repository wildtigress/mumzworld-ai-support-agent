import re

FAQ_DATA = {
    "return": [
        "return", "refund", "send back",
        "إرجاع", "ارجاع", "استرجاع"
    ],
    "refund": [
        "refund", "money back",
        "استرداد", "استرجاع"
    ],
    "shipping": [
        "shipping", "delivery",
        "شحن", "توصيل"
    ],
    "cancel": [
        "cancel", "stop order",
        "إلغاء", "الغاء"
    ]
}


def retrieve_context(query: str) -> str:
    query = query.lower()
    matches = []

    for intent, keywords in FAQ_DATA.items():
        for keyword in keywords:
            if keyword in query:
                if intent == "return":
                    matches.append("Customers can return items within 30 days with receipt.")
                elif intent == "refund":
                    matches.append("Refunds are processed within 5–7 business days.")
                elif intent == "shipping":
                    matches.append("Shipping takes 2–5 days depending on location.")
                elif intent == "cancel":
                    matches.append("Orders can be canceled before shipment.")

    if not matches:
        return "NO_RELEVANT_CONTEXT"

    return "\n".join(matches)