from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


model = SentenceTransformer(
    MODEL_NAME,
    device="cpu",
)


def generate_embeddings(texts: list[str]):
    """
    Generate embeddings for a list of texts.

    The model runs locally on CPU, so no external
    embedding API is required.
    """

    return model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )