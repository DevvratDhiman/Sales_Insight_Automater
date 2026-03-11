import pandas as pd
import io
import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def parse_sales_file(file):

    filename = file.filename.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(file.file.read()))

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(file.file.read()))

    else:
        raise ValueError("Unsupported file format")

    return df


def generate_ai_summary(df):
   
    dataset_preview = f"""
Dataset has {len(df)} rows and {len(df.columns)} columns.

Columns:
{', '.join(df.columns)}

   Sample companies:
{', '.join(df['Company'].head(5).astype(str))}

Sample countries:
{', '.join(df['Country'].head(5).astype(str))}
"""

    prompt = dataset_preview

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": prompt,
            "parameters": {
                "max_length": 120,
                "min_length": 40,
                "do_sample": False
            }
        }
    )

    result = response.json()

    print(result)

    if isinstance(result, list):
        return result[0].get("summary_text", result[0].get("generated_text", "No summary"))

    if "error" in result:
        return result["error"]

    return str(result)