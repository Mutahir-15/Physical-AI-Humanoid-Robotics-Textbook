import os
import google.generativeai as genai
from typing import List, Dict, Optional

class GeminiAgent:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        
        genai.configure(api_key=self.gemini_api_key)
        # Using gemini-1.5-flash which is the current standard efficient model
        self.model = genai.GenerativeModel('gemini-2.5-flash') 

    async def generate_grounded_answer(
        self, 
        user_query: str, 
        context_chunks: List[str], 
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Generates a grounded answer using the Gemini API based on provided context.
        The prompt strictly enforces using only the provided context.
        """
        system_instruction = (
            "You are a helpful assistant expert in robotics, specialized in the 'Physical AI & Humanoid Robotics Course' book. "
            "Your task is to answer user questions truthfully and based *only* on the provided context information. "
            "If the answer cannot be found in the context, explicitly state 'I cannot answer this question based on the provided book content.' "
            "Do not make up information or use outside knowledge. Keep your answers concise and to the point."
        )

        full_prompt = f"{system_instruction}\n\n--- Provided Context from the Book ---\n"
        for i, chunk in enumerate(context_chunks):
            full_prompt += f"Chunk {i+1}: {chunk}\n"
        full_prompt += f"\n--- End of Provided Context ---\n\nUser Question: {user_query}\nAnswer:"

        messages = []
        if chat_history:
            for item in chat_history:
                if "role" in item and "content" in item:
                    messages.append({"role": item["role"], "parts": [item["content"]]})
                else:
                    print(f"WARNING: Malformed chat_history item skipped: {item}")
        
        messages.append({"role": "user", "parts": [full_prompt]})

        try:
            # For Gemini, the 'generate_content' method is used for chat-like interactions.
            # Safety settings can be adjusted if needed, but defaults are generally good.
            response = await self.model.generate_content_async(messages)
            return response.text
        except Exception as e:
            print(f"Error generating content from Gemini: {e}")
            raise
