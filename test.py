import httpx
import asyncio

GROQ_API_KEY = "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"

async def test_groq():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": "You are a historical chatbot."},
                    {"role": "user", "content": "Tell me about Indian Knowledge System"}
                ],
            },
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
        )
        print(response.json())  # Ensure response is valid JSON

asyncio.run(test_groq())
