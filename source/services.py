import os
import numpy as np
import openai


from models import Message
from utils import word_wrap, process_title

from prompts import system_prompt
from database import insert_data_into_db

openai.api_key = os.environ['OPENAI_API_KEY']
openai_client = openai.OpenAI()


def rag(prompt, retrieved_documents, model="gpt-3.5-turbo"):
    context = "\n\n".join(retrieved_documents)

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Answer this question: {prompt}. \n Use this information: {context}"
        }
    ]

    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )
    response = response.choices[0].message.content
    insert_data_into_db(prompt, response, context)

    return response


def fetch_data(query: Message, chroma_client):
    """Fetch documents and metadata from a collection based on the query."""
    chroma_collection = chroma_client.get_collection("mojo")
    results = chroma_collection.query(query_texts=[query], n_results=20, include=[
                                      'documents', 'embeddings', 'metadatas'])
    return results


def process_metadata(metadata):
    """Process metadata to extract and format necessary information."""
    base_url = 'http://path.to.files/'
    processed_metadata = [(data['filename'], process_title(data['title']))
                          for data in metadata if data]
    markdown_links = [f"[{title}]({base_url + filename})" for filename, title in processed_metadata]
    return list(set(markdown_links))


def calculate_scores(query, documents, cross_encoder):
    """Calculate similarity scores between the query and each document."""
    pairs = [[query, doc] for doc in documents]
    scores = cross_encoder.predict(pairs)
    return scores


def filter_and_sort_scores(scores):
    """Filter and sort the scores, returning sorted indices of the documents."""
    filtered_scores = [score for score in scores if score > 0]
    sorted_indices = np.argsort(-np.array(filtered_scores))
    return sorted_indices


def generate_output(query, retrieved_documents, indexes, markdown_links):
    """Generate the final output, including formatted response and sources."""

    reranked_documents = [retrieved_documents[i] for i in indexes[:5]]
    output = rag(prompt=query, retrieved_documents=reranked_documents)
    sources = "\n\n**Sources:**\n\n" + "\n\n".join(markdown_links[:5])

    # Check if there are more than 5 indexes and handle additional sources
    further_reading_start = 5
    further_reading_end = min(len(indexes), 8)  # Ensure we do not go out of bounds
    if len(indexes) > further_reading_start:
        further_reading_links = markdown_links[further_reading_start:further_reading_end]
        if further_reading_links:
            sources += "\n\n**Further reading:**\n\n" + "\n\n".join(further_reading_links)

    return {"response": word_wrap(output), "sources": sources}


def get_answer(query: Message, chroma_client, cross_encoder, expand_context=False):

    if expand_context:
        results = fetch_expanded_data(query, chroma_client)
    else:
        results = fetch_data(query, chroma_client)

    documents, metadata = results['documents'][0], results['metadatas'][0]
    markdown_links = process_metadata(metadata)
    scores = calculate_scores(query, documents, cross_encoder)
    sorted_indices = filter_and_sort_scores(scores)
    return generate_output(query, documents, sorted_indices, markdown_links)


def augment_multiple_query(query, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful expert Mojo assistant. Your users are asking questions about Mojo documentation. "
            "Suggest up to five additional related questions to help them find the information they need, for the provided question. "
            "Suggest only short questions without compound sentences. Suggest a variety of questions that cover different aspects of the topic."
            "Make sure they are complete questions, and that they are related to the original question."
            "Output one question per line. Do not number the questions."
        },
        {"role": "user", "content": query}
    ]

    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    content = response.choices[0].message.content
    content = content.split("\n")
    return content


def fetch_expanded_data(query, chroma_client):

    augmented_queries = augment_multiple_query(query, model="gpt-3.5-turbo")
    print(augmented_queries)
    queries = [query] + augmented_queries
    chroma_collection = chroma_client.get_collection("mojo")
    results = chroma_collection.query(query_texts=queries, n_results=20, include=['documents', 'embeddings', 'metadatas'])
    
    return results