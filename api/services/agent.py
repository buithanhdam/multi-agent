import logging
from typing import Optional, List

from src.agents import (
    ReflectionAgent,
    PlanningAgent,
    AgentOptions,
    ManagerAgent,
    FallbackAgent
)
from src.tools.tool_manager import weather_tool
from src.agents.llm import GeminiLLM
from llama_index.core.llms import ChatMessage

class AgentChat:
    def __init__(self):
        # Initialize LLM
        self.llm = GeminiLLM()
        
        # Logging setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Create a default agent for fallback
        # In AgentChat __init__
        self.default_agent = FallbackAgent(
            self.llm,
            AgentOptions(
                id="default",
                name="Default Assistant",
                description="Provides general conversational assistance"
            )
        )
        
        # Initialize specialized agents
        self.reflection_agent = ReflectionAgent(
            self.llm,
            AgentOptions(
                id="reflection",
                name="Reflection Assistant",
                description="Helps with information generation and refinement about football"
            )
        )
        
        self.planning_agent = PlanningAgent(
            self.llm,
            AgentOptions(
                id="planning",
                name="Planning Assistant",
                description="Assists with project planning, task breakdown, and using weather tool"
            ),
            tools=[weather_tool]
        )
        
        # Initialize manager agent
        self.manager = ManagerAgent(
            self.llm,
            AgentOptions(
                id="manager",
                name="Manager",
                description="Routes requests to specialized agents"
            )
        )
        
        # Register agents with manager (including default agent)
        self.manager.register_agent(self.default_agent)
        self.manager.register_agent(self.reflection_agent)
        self.manager.register_agent(self.planning_agent)
        
        # Chat history to provide context
        self.chat_history: List[ChatMessage] = []
    
    async def get_response(self, user_input: str, verbose: bool = True) -> str:
        """
        Process user input by routing to appropriate agent
        
        Args:
            user_input (str): User's query
            verbose (bool): Whether to log detailed information
        
        Returns:
            str: Agent's response
        """
        try:
            # Process the input and get a response
            response = await self.manager.run(
                query=user_input,
                chat_history=self.chat_history,
                verbose=verbose
            )
            
            # Update chat history
            self.chat_history.append(ChatMessage(role="user", content=user_input))
            self.chat_history.append(ChatMessage(role="assistant", content=response))
            
            # Trim chat history to last 5 messages to prevent context overflow
            self.chat_history = self.chat_history[-10:]
            
            return response
        
        except Exception as e:
            self.logger.error(f"Error in get_response: {e}")
            return "I'm sorry, I encountered an error processing your request."
    
    def reset_chat(self):
        """Reset the chat history"""
        self.chat_history = []
