import os

from google import genai
from google.genai import types
import numpy as np

gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

data = {
    "mango": {},
    "strawberry": {},
    "watermelon": {},
    "orange": {},
    "jabuticaba": {},
    "feijoa": {},
    "Spruce Goose": {}
}
task_types = ["CLUSTERING", "CODE_RETRIEVAL_QUERY"]

for term in data:
    for task_type in task_types:
        result = gemini.models.embed_content(
            model="gemini-embedding-exp-03-07",
            contents=term,
            config=types.EmbedContentConfig(task_type=task_type)
        )
        data[term][task_type] = result.embeddings[0].values

baseline = "mango"
for task_type in task_types:
    print("==========")
    print(task_type)
    for term in data:
        if term == baseline:
            continue
        print("---")
        print(f"Comparing {term} to {baseline}")
        dot_product = np.dot(data[term][task_type], data[baseline][task_type])
        print(f"Dot product: {dot_product}")
