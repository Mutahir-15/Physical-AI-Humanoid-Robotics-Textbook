# sample_ingest_demo.py

import os
import re
from content_cleaner import clean_mdx_content
from mdx_chunker import chunk_mdx_content
# from cohere_tokenizer import CohereTokenizer # Assuming this will be installed

# Placeholder for CohereTokenizer
class MockCohereTokenizer:
    def tokenize(self, text):
        return text.split() # Naive tokenization for demo
    
    def detokenize(self, tokens):
        return " ".join(tokens)

# tokenizer = CohereTokenizer() # Use actual tokenizer when available
tokenizer = MockCohereTokenizer()


def get_sample_mdx_files(directory: str) -> list[str]:
    """Retrieves paths of sample MDX files for ingestion."""
    mdx_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".mdx"):
                mdx_files.append(os.path.join(root, file))
    return mdx_files

def process_document(filepath: str):
    """Processes a single MDX document: cleans, chunks, and prints info."""
    print(f"Processing: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        mdx_content = f.read()

    cleaned_content = clean_mdx_content(mdx_content)
    chunks = chunk_mdx_content(cleaned_content, chunk_size=550, chunk_overlap=50) # Use spec's range

    print(f"  Cleaned content length: {len(cleaned_content)} characters")
    print(f"  Generated {len(chunks)} chunks.")
    
    for i, chunk in enumerate(chunks):
        print(f"    Chunk {i+1}:")
        print(f"      Token count (naive): {chunk['metadata']['token_count']}")
        print(f"      Content (first 100 chars): {chunk['text_content'][:100]}...")
        print(f"      Metadata: {chunk['metadata']}")
    print("-" * 50)

if __name__ == "__main__":
    docs_dir = "docs" # Assuming 'docs' is relative to the project root
    
    # Get a few sample MDX files, ideally from the course content
    sample_mdx_paths = get_sample_mdx_files(docs_dir)
    
    if not sample_mdx_paths:
        print(f"No .mdx files found in '{docs_dir}'. Please ensure your Docusaurus docs are present.")
        # Fallback to creating a dummy MDX for demonstration if no actual docs are found
        dummy_mdx_path = os.path.join(docs_dir, "rag_chatbot", "dummy_doc.mdx")
        os.makedirs(os.path.dirname(dummy_mdx_path), exist_ok=True)
        with open(dummy_mdx_path, 'w', encoding='utf-8') as f:
            f.write(
                """---
title: Dummy Document for Testing
---
This is a dummy document to test the ingestion pipeline. It contains several sentences to simulate real content. Each sentence adds to the overall token count. We are testing the chunking strategy and how overlap is handled. This should provide enough text for multiple chunks."""
            )
        sample_mdx_paths.append(dummy_mdx_path)
    
    for path in sample_mdx_paths:
        process_document(path)
