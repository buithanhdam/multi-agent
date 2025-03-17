from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Generator, List, Optional
from llama_index.core.llms import ChatMessage
# from llama_index.llms.anthropic import Anthropic
from llama_index.llms.gemini import Gemini
# from llama_index.llms.openai import OpenAI
from src.config import Config
from src.logger import get_formatted_logger


logger = get_formatted_logger(__file__)

class BaseLLM(ABC):
    def __init__(
        self, 
        api_key: str, 
        model_name: str, 
        model_id: str, 
        temperature: float, 
        max_tokens: int, 
        system_prompt: str
    ):
        """
        Khởi tạo base LLM class.

        Args:
            api_key (str): API key cho model
            model_name (str): Tên của model
            model_id (str): ID của model
            temperature (float): Nhiệt độ cho việc sinh text
            max_tokens (int): Số tokens tối đa cho mỗi response
            system_prompt (str): System prompt mặc định
        """
        self.api_key = api_key
        self.model_name = model_name
        self.model_id = model_id
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt

    def _initialize_model(self) -> None:
        try:
            global_settings = Config()
            if self.model_name.lower() == "gemini":
                self.model = Gemini(
                    api_key=self.api_key if self.api_key else global_settings.GEMINI_CONFIG.api_key,
                    model=self.model_id if self.model_id else global_settings.GEMINI_CONFIG.model_id,
                    temperature=self.temperature if self.temperature else global_settings.GEMINI_CONFIG.temperature,
                    max_tokens=self.max_tokens if self.max_tokens else global_settings.GEMINI_CONFIG.max_tokens,
                    additional_kwargs={
                        'generation_config': {
                            'temperature': self.temperature if self.temperature else global_settings.GEMINI_CONFIG.temperature,
                            'top_p': 0.8,
                            'top_k': 40,
                        }
                    },
                )
            # elif self.model_name == "claude":
            #     self.model = Anthropic(
            #         api_key=self.api_key,
            #         model=self.model_id,
            #         temperature=self.temperature,
            #         max_tokens=self.max_tokens
            #     )
            # elif self.model_name == "openai":
            #     self.model = OpenAI(
            #         api_key=self.api_key,
            #         model=self.model_id,
            #         temperature=self.temperature,
            #         max_tokens=self.max_tokens
            #     )
            else:
                raise ValueError(f"Unsupported model type: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize {self.model_name} model: {str(e)}")
            raise

    @abstractmethod
    def _prepare_messages(
        self, 
        query: str, 
        chat_history: Optional[List[ChatMessage]] = None
    ) -> List[ChatMessage]:
        pass
    
    def _extract_response(self, response: Any):
        """
        Extract content from various response formats.
        
        Args:
            response: The response object from the LLM
            
        Returns:
            str: The extracted content
        """
        try:
            if hasattr(response, 'content'):
                return response.content
            elif hasattr(response, 'message') and hasattr(response.message, 'content'):
                return response.message.content
            elif isinstance(response, dict) and 'content' in response:
                return response['content']
            elif isinstance(response, str):
                return response
            else:
                # Try best effort to get string representation
                return str(response)
        except Exception as e:
            logger.error(f"Error extracting response from {self.model_name}: {str(e)}")
            return response.message.content
        
    @abstractmethod
    def chat(
        self, 
        query: str, 
        chat_history: Optional[List[ChatMessage]] = None
    ) -> str:
        pass

    @abstractmethod
    async def achat(
        self, 
        query: str, 
        chat_history: Optional[List[ChatMessage]] = None
    ) -> str:
        pass

    @abstractmethod
    def stream_chat(
        self, 
        query: str, 
        chat_history: Optional[List[ChatMessage]] = None
    ) -> Generator[str, None, None]:
        pass

    @abstractmethod
    async def astream_chat(
        self, 
        query: str, 
        chat_history: Optional[List[ChatMessage]] = None
    ) -> AsyncGenerator[str, None]:
        pass
    
    def get_model_name(self) -> str:
        return self.model_name

    def get_model_config(self) -> dict:
        return {
            "model_name": self.model_name,
            "model_id": self.model_id,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "system_prompt": self.system_prompt
        }
    @asynccontextmanager
    async def session(self):
        try:
            yield self
        finally:
            # Cleanup code if needed
            pass