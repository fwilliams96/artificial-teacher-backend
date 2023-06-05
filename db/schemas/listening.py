def listening_schema(listening) -> dict:
    return {
        "id": str(listening["_id"]),
        "topic": listening["topic"],
        "sentences": sentences_chema(listening["sentences"])
    }

def sentences_chema(sentences) -> list:
    return [sentence_chema(sentence) for sentence in sentences] 

def sentence_chema(sentence: dict) -> dict:
    return {
        "correct_sentence": sentence["correct_sentence"],
        "incomplete_sentence": sentence["incomplete_sentence"]
    }