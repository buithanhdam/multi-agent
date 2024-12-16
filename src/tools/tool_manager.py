from typing import Callable, Optional
from llama_index.core.tools import FunctionTool

def create_function_tool(
    func: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None
) -> FunctionTool:
    """Helper function to create a FunctionTool with proper metadata"""
    return FunctionTool.from_defaults(
        fn=func,
        name=name or func.__name__,
        description=description or func.__doc__ or "No description provided"
    )
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Get current weather for a location"""
    return {
        "temperature": 25,
        "weather_description": "Sunny",
        "humidity": 60,
        "wind_speed": 10
    }
weather_tool = create_function_tool(
            get_weather,
            name="get_weather",
            description="Get current weather information for a location"
        )