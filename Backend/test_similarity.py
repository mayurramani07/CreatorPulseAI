import numpy as np

from app.services.embedding_service import generate_embeddings


reference = "Vote for AWS full course"

examples = [
    "Please make a complete AWS course",
    "Can you teach AWS from beginner to advanced?",
    "AWS full course please",
    "Can you make an AWS playlist?",
    "This video is hilarious 😂",
    "I got Rickrolled again",
    "Amazing video",
    "This song is really good",
]


texts = [reference] + examples

embeddings = generate_embeddings(texts)

reference_embedding = embeddings[0]

print("\nReference:")
print(reference)

print("\nSimilarity scores:\n")

for text, embedding in zip(examples, embeddings[1:]):

    similarity = np.dot(
        reference_embedding,
        embedding,
    )

    print(f"{similarity:.4f}  →  {text}")