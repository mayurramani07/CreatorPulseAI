from app.services.embedding_service import generate_embeddings


texts = [
    "Vote for AWS full course",
    "Please make a complete AWS tutorial",
    "Can you teach AWS from beginner to advanced?",
    "This video is really funny 😂",
]


embeddings = generate_embeddings(texts)

print("Number of embeddings:", len(embeddings))
print("Embedding dimensions:", len(embeddings[0]))