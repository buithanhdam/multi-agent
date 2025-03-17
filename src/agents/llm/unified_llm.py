from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generator, List, Optional
from llama_index.core.llms import ChatMessage
from src.logger import get_formatted_logger
import asyncio
from .base import BaseLLM

logger = get_formatted_logger(__file__)

class UnifiedLLM(BaseLLM):
    def __init__(
        self, 
        api_key: str = None, 
        model_name: str = "gemini", 
        model_id: str = None, 
        temperature: float = None, 
        max_tokens: int = None, 
        system_prompt: str = None,
    ):
        super().__init__(
            api_key=api_key,
            model_name=model_name,
            model_id=model_id,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt
        )
        self._initialize_model()

    def _prepare_messages(
        self,
        query: str,
        chat_history: Optional[List[ChatMessage]] = None
    ) -> List[ChatMessage]:
        messages = []
        if self.system_prompt:
            messages.append(ChatMessage(role="system", content=self.system_prompt))
            messages.append(ChatMessage(role="assistant", content="I understand and will follow these instructions."))
        
        if chat_history:
            messages.extend(chat_history)
        
        messages.append(ChatMessage(role="user", content=query))
        return messages

    def chat(
        self,
        query: str,
        chat_history: Optional[List[ChatMessage]] = None
    ) -> str:
        try:
            messages = self._prepare_messages(query, chat_history)
            response = self.model.chat(messages)
            return self._extract_response(response)
        except Exception as e:
            logger.error(f"Error in {self.model_name} chat: {str(e)}")
            raise

    async def achat(
        self,
        query: str,
        chat_history: Optional[List[ChatMessage]] = None
    ) -> str:
        try:
            messages = self._prepare_messages(query, chat_history)
            response = await self.model.achat(messages)
            return self._extract_response(response)
        except Exception as e:
            logger.error(f"Error in {self.model_name} async chat: {str(e)}")
            raise

    def stream_chat(
        self,
        query: str,
        chat_history: Optional[List[ChatMessage]] = None
    ) -> Generator[str, None, None]:
        try:
            messages = self._prepare_messages(query, chat_history)
            response_stream = self.model.stream_chat(messages)
            for response in response_stream:
                yield self._extract_response(response)
        except Exception as e:
            logger.error(f"Error in {self.model_name} stream chat: {str(e)}")
            raise

    async def astream_chat(
        self,
        query: str,
        chat_history: Optional[List[ChatMessage]] = None
    ) -> AsyncGenerator[str, None]:
        try:
            messages = self._prepare_messages(query, chat_history)
            response = await self.model.astream_chat(messages)
            
            if asyncio.iscoroutine(response):
                response = await response
            
            if hasattr(response, '__aiter__'):
                async for chunk in response:
                    yield self._extract_response(chunk)
            else:
                yield self._extract_response(response)
                
        except Exception as e:
            logger.error(f"Error in {self.model_name} async stream chat: {str(e)}")
            raise

    @asynccontextmanager
    async def session(self):
        """Context manager để quản lý phiên làm việc với model"""
        try:
            yield self
        finally:
            # Cleanup code if needed
            pass