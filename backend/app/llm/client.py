import httpx 
import json

async def extract_price_from_html(html: str) -> dict | None:
    html = html[:100000]  # Limit to first 100k chars for speed and context window sanity

    prompt = """
You are a precise HTML parser that extracts structured product data from e-commerce pages.

Your task:
1. Identify the **product name**.
2. Identify the **numeric price value** (no currency symbols).
3. Identify the **currency** (use ISO 4217, e.g., USD, CAD, EUR).
4. Extract the **current selling price** or **discounted price shown most prominently**,
   not the struck-through MSRP or “estimated value”.
5. Ignore text like “Save $”, “Discount”, “Est. value”.

Return **valid JSON only**, with these keys:
{
  "name": "<product name>",
  "price": <float: price>,
  "currency": "<currency code>"
}

Do not include explanations, markdown, or other text.
If no price is found, still return valid JSON with "price": 0.0.
HTML snippet:
""" + html

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False},
            timeout=120,
        )

    result = resp.json()["response"]

    try:
        # Extract only the JSON part
        start = result.find("{")
        end = result.rfind("}") + 1
        cleaned = result[start:end]
        data = json.loads(cleaned)
        return data
    except Exception as e:
        print(f"[ERROR] Llama parse failed: {e}\nRaw output:\n{result[:500]}")
        return None