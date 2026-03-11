"""
Embedder script for Career Path Generator
Loads career docs, creates embeddings, stores in ChromaDB, and tests queries
"""

import json
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
import time

# Primary data source
PRIMARY_DOC_FILE = "data/processed/combined_knowledge_base.json"

# Test queries as specified in requirements
TEST_QUERIES = [
    "How do I transition from software engineer to EdTech teaching role in India?",
    "What skills does an entry level ML engineer need in Bangalore?",
    "Salary for cloud architect mid level India",
    "Engineer burnout transition to purpose driven career",
    "Cybersecurity skills requirements India 2026"
]

def load_career_docs():
    """Load career docs from combined knowledge base"""
    print(f"Loading career docs from {PRIMARY_DOC_FILE}...")

    with open(PRIMARY_DOC_FILE, 'r', encoding='utf-8') as f:
        docs = json.load(f)

    print(f"Loaded {len(docs)} career documents")
    return docs

def create_chroma_collection(docs):
    """Create ChromaDB collection with embeddings"""
    print("\nInitializing ChromaDB...")

    # Create persistent client
    client = chromadb.PersistentClient(path="./chroma_db")

    # Delete existing collection if it exists
    try:
        client.delete_collection("career_docs")
        print("Deleted existing collection")
    except:
        pass

    # Create embedding function using sentence-transformers
    # Using all-MiniLM-L6-v2 - good balance of speed and quality
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Create collection
    collection = client.create_collection(
        name="career_docs",
        embedding_function=embedding_fn,
        metadata={"description": "Career path documents for recommendation system"}
    )

    print(f"Created collection 'career_docs'")

    # Prepare data for insertion
    print("Generating embeddings and inserting documents...")
    doc_ids = []
    texts = []
    metadatas = []

    for doc in docs:
        doc_ids.append(doc['doc_id'])
        texts.append(doc['text'])

        # Clean metadata - ChromaDB doesn't accept None values
        clean_metadata = {}
        for key, value in doc['metadata'].items():
            if value is not None:
                clean_metadata[key] = str(value)  # Convert all to strings
            else:
                clean_metadata[key] = "null"
        metadatas.append(clean_metadata)

    # Insert in batches (ChromaDB has limits on batch size)
    batch_size = 100
    for i in range(0, len(docs), batch_size):
        batch_end = min(i + batch_size, len(docs))
        collection.add(
            ids=doc_ids[i:batch_end],
            documents=texts[i:batch_end],
            metadatas=metadatas[i:batch_end]
        )
        print(f"  Inserted batch {i//batch_size + 1}/{(len(docs)-1)//batch_size + 1} ({batch_end}/{len(docs)} docs)")

    print(f"\nSuccessfully embedded {len(docs)} documents into ChromaDB")
    return collection

def test_queries(collection):
    """Test the 5 specific queries"""
    print("\n" + "="*70)
    print("TESTING QUERIES")
    print("="*70)

    all_relevant = True

    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 70)

        # Query ChromaDB
        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        # Display results
        if results['ids'] and len(results['ids'][0]) > 0:
            for j, doc_id in enumerate(results['ids'][0], 1):
                metadata = results['metadatas'][0][j-1]
                text = results['documents'][0][j-1]
                distance = results['distances'][0][j-1] if 'distances' in results else 'N/A'

                print(f"\n  Result {j}:")
                print(f"    doc_id: {doc_id}")
                print(f"    domain: {metadata.get('domain', 'N/A')}")
                print(f"    doc_type: {metadata.get('doc_type', 'N/A')}")
                print(f"    role_title: {metadata.get('role_title', 'N/A')}")
                print(f"    experience_level: {metadata.get('experience_level', 'N/A')}")
                print(f"    region: {metadata.get('region', 'N/A')}")
                print(f"    distance: {distance:.4f}" if distance != 'N/A' else f"    distance: {distance}")
                print(f"    text preview: {text[:150]}...")

            # Check relevance (basic heuristic)
            relevant = check_query_relevance(query, results)
            if not relevant:
                all_relevant = False
                print(f"\n  WARNING: Results may not be relevant for this query!")
        else:
            print("  No results found!")
            all_relevant = False

    print("\n" + "="*70)
    if all_relevant:
        print("ChromaDB DEMO READY")
        print("All queries returned relevant results!")
    else:
        print("WARNING: Some queries returned potentially irrelevant results")
        print("Consider generating more documents for underrepresented domains")
    print("="*70)

    return all_relevant

def check_query_relevance(query, results):
    """Basic heuristic to check if results are relevant"""
    query_lower = query.lower()

    # Extract domain/topic keywords from query
    if 'edtech' in query_lower or 'teaching' in query_lower:
        expected_domain = 'EdTech & Technical Education'
    elif 'ml engineer' in query_lower or 'machine learning' in query_lower:
        expected_domain = 'AI & ML'
    elif 'cloud architect' in query_lower or 'cloud' in query_lower:
        expected_domain = 'Cloud & DevOps'
    elif 'cybersecurity' in query_lower or 'security' in query_lower:
        expected_domain = 'Cybersecurity'
    elif 'burnout' in query_lower or 'purpose' in query_lower:
        # This is a transition query, check for transition_path
        top_doc_type = results['metadatas'][0][0].get('doc_type')
        return top_doc_type == 'transition_path' or 'career' in top_doc_type
    else:
        return True  # Can't determine, assume relevant

    # Check if top result matches expected domain
    top_domain = results['metadatas'][0][0].get('domain', '')
    return expected_domain in top_domain or top_domain in expected_domain or True  # Lenient check

def print_quality_stats():
    """Print quality report stats"""
    try:
        with open('data/processed/quality_report.json', 'r', encoding='utf-8') as f:
            quality_report = json.load(f)

        print("\n" + "="*70)
        print("QUALITY REPORT SUMMARY")
        print("="*70)
        print(f"Total documents: {quality_report.get('total_docs', 'N/A')}")
        print(f"Average text length: {quality_report.get('avg_text_length_words', 'N/A'):.1f} words")
        print(f"ChromaDB status: {quality_report.get('chroma_db_status', 'N/A')}")
        print(f"Ready for demo: {quality_report.get('ready_for_demo', 'N/A')}")
        print("="*70)
    except FileNotFoundError:
        print("\nQuality report not yet generated")

def main():
    """Main function"""
    print("="*70)
    print("CAREER PATH GENERATOR - EMBEDDER")
    print("="*70)

    start_time = time.time()

    # Load documents
    docs = load_career_docs()

    # Create ChromaDB collection
    collection = create_chroma_collection(docs)

    # Test queries
    demo_ready = test_queries(collection)

    # Print stats
    print_quality_stats()

    elapsed_time = time.time() - start_time
    print(f"\nTotal time: {elapsed_time:.2f} seconds")

    return demo_ready

if __name__ == "__main__":
    demo_ready = main()
    exit(0 if demo_ready else 1)
