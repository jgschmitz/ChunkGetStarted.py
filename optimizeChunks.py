def chunk_text(text, chunk_size=None, chunk_overlap=100):
    """Dynamically adjust chunk size based on text length."""
    if chunk_size is None:
        chunk_size = max(200, min(len(text) // 10, 800))  # Auto-size between 200-800

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)
