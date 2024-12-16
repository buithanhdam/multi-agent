from src.agents.base import BaseAgent, AgentOptions
from src.agents.llm import BaseLLM
from llama_index.core.llms import ChatMessage
from typing import List, Dict, Any

class FallbackAgent(BaseAgent):
    """
    A simple fallback agent that provides basic conversational responses
    using a straightforward LLM interaction
    """
    def __init__(self, llm: BaseLLM, options: AgentOptions):
        super().__init__(llm, options)
        
    async def run(
        self, 
        query: str, 
        verbose: bool = False,
        **kwargs
    ) -> str:
        """
        Provide a simple response to any query
        
        Args:
            query (str): User's input query
            verbose (bool): Whether to print verbose logging
            
        Returns:
            str: A generated response
        """
        try:
            
            # Prepare chat history with system prompt
            chat_history = [
                ChatMessage(role="user", content=query)
            ]
            
            # Generate response using LLM
            response = await self.llm.achat(
                query=query,
                chat_history=chat_history
            )
            
            # Optional verbose logging
            if verbose:
                print(f"Fallback Agent Response: {response}")
            
            return response
        
        except Exception as e:
            # Fallback error handling
            error_message = f"I'm sorry, I encountered an error: {str(e)}"
            return error_message

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Minimal cleanup if needed
        pass