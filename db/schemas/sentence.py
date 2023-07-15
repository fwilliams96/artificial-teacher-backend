def sentence_schema(sentence) -> dict:
    return {
        "id": str(sentence["_id"]),
        "word": sentence["word"],
        "sentence": sentence["sentence"],
        "user_id": str(sentence["user_id"]),
        "audio": sentence["audio"]
    }