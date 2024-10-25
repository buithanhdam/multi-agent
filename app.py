import streamlit as st
import asyncio
from src.agents import (
    ReflectionAgent,
    create_function_tool,
    PlanningAgent,
    AgentOptions,
    ManagerAgent
)
from src.agents.llm import GeminiLLM
from typing import AsyncGenerator

def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get current weather for a location"""
    return {
        "temperature": 25,
        "weather_description": "Sunny",
        "humidity": 60,
        "wind_speed": 10
    }

class AgentChat:
    def __init__(self):
        self.llm = GeminiLLM()
        
        # Initialize agents
        self.reflection_agent = ReflectionAgent(
            self.llm,
            AgentOptions(
                name="Reflection Assistant",
                description="Helps with information base on LLM"
            )
        )
        
        # Create tools
        self.weather_tool = create_function_tool(
            get_weather,
            name="get_weather",
            description="Get current weather information for a location"
        )
        
        self.planning_agent = PlanningAgent(
            self.llm,
            AgentOptions(
                name="Planning Assistant",
                description="Assists with project planning, task breakdown, and a weather tool"
            ),
            tools=[self.weather_tool]
        )
        
        # Initialize manager agent
        self.manager = ManagerAgent(
            self.llm,
            AgentOptions(
                name="Manager",
                description="Routes requests to specialized agents"
            )
        )
        
        # Register agents with manager
        self.manager.register_agent(self.reflection_agent)
        self.manager.register_agent(self.planning_agent)

    async def get_response(self, user_input: str) -> str:
        response = await self.manager.run(
            query=user_input,
            verbose=True
        )
        return response

def initialize_session_state():
    if 'agent_chat' not in st.session_state:
        st.session_state.agent_chat = AgentChat()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def add_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})

def main():
    st.title("🤖 Multi-Agent Chat Interface")
    
    # Initialize session state
    initialize_session_state()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        add_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = asyncio.run(
                    st.session_state.agent_chat.get_response(prompt)
                )
                st.markdown(response)
                add_message("assistant", response)

    # Sidebar with agent information
    with st.sidebar:
        st.subheader("Available Agents")
        st.info("📝 Reflection Assistant\n\nHelps with information based on LLM")
        st.info("📋 Planning Assistant\n\nAssists with project planning, task breakdown, and weather information")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()