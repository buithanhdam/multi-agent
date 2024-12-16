import asyncio
from src.agents.llm import GeminiLLM
from llama_index.core.llms import ChatMessage

def test_gemini_sync():
    try:
        llm = GeminiLLM()
        response = llm.chat("Xin chào!")
        print("=== Chat đơn giản ===")
        print(f"Response: {response}")
        
        history = [
            ChatMessage(role="user", content="Bạn là ai?"),
            ChatMessage(role="assistant", content="Tôi là trợ lý AI.")
        ]
        response = llm.chat("Rất vui được gặp bạn!", chat_history=history)
        print("\n=== Chat với history ===")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

async def test_gemini_async():
    try:
        llm = GeminiLLM()
        
        response = await llm.achat("Xin chào!")
        print("\n=== Async chat ===")
        print(f"Response: {response}")
        
        print("\n=== Async stream chat ===")
        try:
            async for chunk in llm.astream_chat("Kể cho tôi một câu chuyện ngắn"):
                print(chunk, end="", flush=True)
            print()  # New line after story
        except Exception as e:
            print(f"\nError in stream: {str(e)}")
            
    except Exception as e:
        print(f"Error in async test: {str(e)}")
        raise

if __name__ == "__main__":
    # test_gemini_sync()
    asyncio.run(test_gemini_async())