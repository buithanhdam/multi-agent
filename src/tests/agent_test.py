import asyncio
from src.agents import ReflectionAgent, create_function_tool, PlanningAgent
from src.agents.llm import GeminiLLM

async def test_reflection_async():
    async with ReflectionAgent(llm= GeminiLLM()) as agent:
        result = await agent.run(
            user_msg="leonel messi most successful achievement in his career",
            verbose=1
        )
        print("reflection agent commplete: ",result)
async def test_planning_async():
    def get_weather(location: str, unit: str = "celsius") -> dict:
        """Get current weather for a location
        
        Args:
            location: City name or coordinates
            unit: Temperature unit (celsius/fahrenheit)
        """
        # Implementation here
        return {
            "temperature": 25,
            "weather_description": "Sunny",
            "humidity": 60,
            "wind_speed": 10
        }

    # Create tools
    weather_tool = create_function_tool(
        get_weather,
        name="get_weather",
        description="Get current weather information for a location"
    )

    # Initialize agent
    async with PlanningAgent(llm= GeminiLLM(),tools=[weather_tool]) as agent:
        result = await agent.run(
            task="What's the weather in Hanoi?",
            verbose=True
        )
        print("Planning agent commplete: ",result)

if __name__ == "__main__":
    asyncio.run(test_reflection_async())