from dotenv import load_dotenv, find_dotenv
import sqlite3
import pandas as pd
from datasets import Dataset
import os
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_utilization
)

_ = load_dotenv(find_dotenv())

def load_data_to_pandas():
    conn = sqlite3.connect('rag_data.db')
    df = pd.read_sql_query("SELECT * FROM RAG_DATA", conn)
    conn.close()
    return df

def evaluate_rag():
    try:
        df = load_data_to_pandas()
        last_row = df.iloc[-1]

        data_samples = {
            'question': [last_row['prompt']],
            'answer': [last_row['response']],
            'contexts': [[last_row['context']]],
        }

        dataset = Dataset.from_dict(data_samples)
        score = evaluate(dataset, metrics=[answer_relevancy, faithfulness, context_utilization])

        score = dict(score)
        response = {'question': last_row['prompt']}
        response = {**response, **score}

        return response
    except Exception as e:
        return e
