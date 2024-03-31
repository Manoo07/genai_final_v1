import tiktoken

tokenizer = tiktoken.get_encoding('cl100k_base')
def tiktoken_len(text):
        print(text)
        tokens = tokenizer.encode(
            text,
            disallowed_special=()
        )
        return len(tokens)