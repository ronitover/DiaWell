import requests, json

try:
    from .. import config  # our local config file
except ImportError:
    config = None

def rewrite_tips_with_granite(actions: list[str], lang: str = "en") -> list[str] | None:
    url       = getattr(config, "IBM_WX_URL", None)
    api_key   = getattr(config, "IBM_WX_API_KEY", None)
    project_id = getattr(config, "IBM_WX_PROJECT_ID", None)
    model_id   = getattr(config, "IBM_WX_MODEL_ID", "ibm/granite-13b-instruct")

    if not (url and api_key and project_id):
        return None  # fallback if not configured

    sys_prompt = (
        "You are a health coach. Rewrite the given action tips to be empathetic and "
        "simple for a 15-year-old. Keep the same meaning, do not add new medical claims. "
        "If a language code is provided, translate. Return ONLY 3–5 bullet points, total ≤ 80 words."
    )
    user_prompt = f"Language: {lang}\nTips:\n- " + "\n- ".join(actions)

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model_id": model_id,
            "input": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "project_id": project_id,
            "parameters": {"decoding_method": "greedy", "max_new_tokens": 120}
        }
        r = requests.post(f"{url}/ml/v1/text/generation?version=2023-05-29",
                          headers=headers, data=json.dumps(payload), timeout=15)
        r.raise_for_status()
        text = r.json().get("results", [{}])[0].get("generated_text", "")
        out = [line.strip("-• ").strip() for line in text.splitlines() if line.strip()]
        return out[:5] or None
    except Exception as e:
        print("Granite error:", e)
        return None
