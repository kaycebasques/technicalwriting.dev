import os

from google import genai
from google.genai import types
import numpy as np

gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

task_types = [
    "TASK_TYPE_UNSPECIFIED",
    "RETRIEVAL_QUERY",
    "RETRIEVAL_DOCUMENT",
    "SEMANTIC_SIMILARITY",
    "CLASSIFICATION",
    "CLUSTERING",
    "QUESTION_ANSWERING",
    "FACT_VERIFICATION",
    "CODE_RETRIEVAL_QUERY"
]
embeddings = {}
undisputed_best_fruit_in_world = "mango"

for task_type in task_types:
    result = gemini.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents=undisputed_best_fruit_in_world,
        config=types.EmbedContentConfig(task_type=task_type)
    )
    embeddings[task_type] = result.embeddings[0].values

baseline = "SEMANTIC_SIMILARITY"
baseline_embedding = embeddings[baseline]

for task_type in embeddings:
    if task_type == baseline:
        continue
    print("---")
    print(f"Comparing {task_type} to {baseline}")
    target = embeddings[task_type]
    # Element-wise comparison of the two lists of floats.
    n = 0
    for index, value in enumerate(target):
        if baseline_embedding[index] == value:
            n += 1
    print(f"Identical dimensions: {n}")
    # Magnitude and direction comparison of the two vectors.
    dot_product = np.dot(target, baseline_embedding)
    print(f"Dot product: {dot_product}")
