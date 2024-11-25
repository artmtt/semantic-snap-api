def is_query_text_valid(query_text: str) -> bool:
    text_len = len(query_text)
    return (isinstance(query_text, str) and text_len > 0 and text_len <= 1000)

def is_limit_valid(limit: int) -> bool:
    return (isinstance(limit, int) and limit > 0 and limit <= 10000)

def is_id_valid(id: int) -> bool:
    return (isinstance(id, int))
