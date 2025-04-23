import tiktoken

def count_token(text: str):
    encoding = tiktoken.encoding_for_model("text-embedding-3-small")
    num_tokens = len(encoding.encode(text))
    return num_tokens