import asyncio
from src.agents.llm import UnifiedLLM
from llama_index.core.llms import ChatMessage

async def test_gemini_achat():
    try:
        llm = UnifiedLLM(model_name="gemini")
        response = llm.chat("Xin chào!")
        print("=== Chat đơn giản ===")
        print(f"Response: {response}")
        
        history = [
            ChatMessage(role="user", content="Bạn là ai?"),
            ChatMessage(role="assistant", content="Tôi là trợ lý AI.")
        ]
        response = await llm.achat("Rất vui được gặp bạn!", chat_history=history)
        print("\n=== Chat với history ===")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

async def test_gemini_async():
    try:
        llm = UnifiedLLM(
            model_name="gemini",
            system_prompt=
                """<think>

                1. **Understand the Question**: Begin by carefully reading and interpreting the question to clarify what is being asked.
                2. **Identify Key Components**: Break down the question into its essential elements. What are the main concepts or variables involved?
                3. **Outline Relevant Information**: Consider any formulas, definitions, or prior knowledge that may apply to this problem. What information do I need to solve it?
                4. **Step-by-Step Reasoning**:
                    - Clearly articulate each step of your reasoning process.
                    - Apply logical reasoning to derive conclusions from the information provided.
                    - If applicable, perform necessary calculations or analyses in a systematic manner.
                5. **Summarize Key Points**: After completing your reasoning, summarize the main points that are relevant to the question.
                6. **Final Answer**: Provide a concise answer that directly addresses the question.
                </think>
                <answer>{{final_answer}}</answer>
                """
            )
        
        # response = await llm.achat("Xin chào!")
        # print("\n=== Async chat ===")
        # print(f"Response: {response}")
        
        print("\n=== Async stream chat ===")
        try:
            async for chunk in llm.astream_chat("Phân tích nhiễm sắc thể con người, sự khác nhau giống nhau?"):
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