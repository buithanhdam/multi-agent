from typing import List
from llama_index.core.llms import ChatMessage
from src.agents.llm import BaseLLM
import logging
from colorama import Fore
from src.agents.utils import ChatHistory
from src.prompt import BASE_GENERATION_SYSTEM_PROMPT, BASE_REFLECTION_SYSTEM_PROMPT
logger = logging.getLogger(__name__)

class ReflectionAgent:
    def __init__(self, llm:BaseLLM):
        self.llm = llm
        
    def _create_system_message(self, prompt: str) -> ChatMessage:
        return ChatMessage(role="system", content=prompt)
        
    async def _generate_response(
        self,
        chat_history: List[ChatMessage],
        verbose: int = 0,
        log_title: str = "COMPLETION",
        log_color: str = ""
    ) -> str:
        try:
            response = await self.llm.achat(
                query=chat_history[-1].content,
                chat_history=chat_history[:-1]
            )
            
            if verbose > 0:
                print(log_color, f"\n\n{log_title}\n\n", response)
                
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    async def generate(
        self,
        generation_history: ChatHistory,
        verbose: int = 0
    ) -> str:
        return await self._generate_response(
            generation_history.get_messages(),
            verbose,
            log_title="GENERATION",
            log_color=Fore.BLUE
        )

    async def reflect(
        self,
        reflection_history: ChatHistory,
        verbose: int = 0
    ) -> str:
        return await self._generate_response(
            reflection_history.get_messages(),
            verbose,
            log_title="REFLECTION", 
            log_color=Fore.GREEN
        )

    async def run(
        self,
        user_msg: str,
        generation_system_prompt: str = "",
        reflection_system_prompt: str = "",
        n_steps: int = 3,
        verbose: int = 0,
    ) -> str:
        # Initialize system prompts
        full_gen_prompt = generation_system_prompt + BASE_GENERATION_SYSTEM_PROMPT
        full_ref_prompt = reflection_system_prompt + BASE_REFLECTION_SYSTEM_PROMPT

        # Initialize chat histories
        generation_history = ChatHistory(
            initial_messages=[
                self._create_system_message(full_gen_prompt),
                ChatMessage(role="user", content=user_msg)
            ],
            max_length=3
        )

        reflection_history = ChatHistory(
            initial_messages=[self._create_system_message(full_ref_prompt)],
            max_length=3
        )

        for step in range(n_steps):
            if verbose > 0:
                print(f"\nStep {step + 1}/{n_steps}")

            # Generate content
            generation = await self.generate(generation_history, verbose=verbose)
            generation_history.add("assistant", generation)
            reflection_history.add("user", generation)

            # Reflect on the generation
            critique = await self.reflect(reflection_history, verbose=verbose)
            
            if "<OK>" in critique:
                if verbose > 0:
                    print(Fore.RED, "\n\nReflection complete - content is satisfactory\n\n")
                break

            generation_history.add("user", critique)
            reflection_history.add("assistant", critique)

        return generation

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cleanup code if needed
        pass