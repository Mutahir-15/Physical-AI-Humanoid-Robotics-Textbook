import re
from typing import List, Dict, Any

import cohere
from cohere.tokenizer import CohereTokenizer

tokenizer = CohereTokenizer()

def get_token_count(text: str) -> int:
    """
    Estimates token count for a given text using the Cohere tokenizer.
    """
    return len(tokenizer.tokenize(text))

def chunk_mdx_content(
    text: str,
    max_tokens: int = 550,
    overlap_tokens: int = 50,
    file_metadata: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """
    Chunks cleaned MDX content into smaller, semantically coherent units.
    Adheres to the chunking strategy using token counts and overlap.
    Calculates start_position and end_position for each chunk based on character offsets.
    """
    if not text:
        return []

    # Split text into sentences and store their original character spans
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentence_spans = []
    current_char_offset = 0
    for sentence in sentences:
        sentence_spans.append((current_char_offset, current_char_offset + len(sentence)))
        current_char_offset += len(sentence) + 1  # +1 for the space or separator removed by split

    chunks = []
    current_chunk_sentences_indices = []
    current_chunk_tokens_count = 0
    
    for i, sentence in enumerate(sentences):
        sentence_tokens_count = len(tokenizer.tokenize(sentence))

        # Check if adding the current sentence would exceed the max_tokens
        if current_chunk_tokens_count + sentence_tokens_count > max_tokens and current_chunk_sentences_indices:
            # Finalize the current chunk
            chunk_start_sentence_idx = current_chunk_sentences_indices[0]
            chunk_end_sentence_idx = current_chunk_sentences_indices[-1]
            
            chunk_text = " ".join(sentences[idx] for idx in current_chunk_sentences_indices)
            
            chunks.append({
                "text_content": chunk_text,
                "token_count": current_chunk_tokens_count,
                "metadata": {
                    **(file_metadata or {}),
                    "original_order": len(chunks),
                    "start_position": sentence_spans[chunk_start_sentence_idx][0],
                    "end_position": sentence_spans[chunk_end_sentence_idx][1]
                }
            })

            # Prepare for the next chunk with overlap
            # Determine how many sentences to include for overlap based on tokens
            overlap_sentences_indices = []
            overlap_tokens_current_count = 0
            
            # Iterate backwards from the end of the current chunk to find sentences for overlap
            for j in reversed(current_chunk_sentences_indices):
                s_tokens_count = len(tokenizer.tokenize(sentences[j]))
                if overlap_tokens_current_count + s_tokens_count <= overlap_tokens:
                    overlap_sentences_indices.insert(0, j) # Add to the beginning to maintain order
                    overlap_tokens_current_count += s_tokens_count
                else:
                    break
            
            current_chunk_sentences_indices = overlap_sentences_indices
            current_chunk_tokens_count = overlap_tokens_current_count
        
        # Add the current sentence to the working chunk
        current_chunk_sentences_indices.append(i)
        current_chunk_tokens_count += sentence_tokens_count
    
    # Add the last chunk if any sentences remain in the working chunk
    if current_chunk_sentences_indices:
        chunk_start_sentence_idx = current_chunk_sentences_indices[0]
        chunk_end_sentence_idx = current_chunk_sentences_indices[-1]
        
        chunk_text = " ".join(sentences[idx] for idx in current_chunk_sentences_indices)
        
        chunks.append({
            "text_content": chunk_text,
            "token_count": current_chunk_tokens_count,
            "metadata": {
                **(file_metadata or {}),
                "original_order": len(chunks),
                "start_position": sentence_spans[chunk_start_sentence_idx][0],
                "end_position": sentence_spans[chunk_end_sentence_idx][1]
            }
        })
        
    return chunks