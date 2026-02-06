def classify_intent(query: str):
    q = query.lower()

    if any(word in q for word in ["show", "find", "get"]):
        return "SEARCH_PHOTOS"

    if any(word in q for word in ["send", "share", "email", "whatsapp"]):
        return "SHARE_PHOTOS"

    if any(word in q for word in ["upload", "add"]):
        return "UPLOAD_PHOTO"

    return "UNKNOWN"
