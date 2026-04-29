def retrieve_context(query):
    with open("data/faq.txt", "r", encoding="utf-8") as f:
        return f.read()