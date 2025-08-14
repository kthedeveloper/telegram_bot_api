def write_file(path: str, content: bytes):
    with open(path, "wb") as f:
        f.write(content)
