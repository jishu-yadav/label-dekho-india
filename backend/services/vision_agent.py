import os
import json
from google import genai
from google.genai import types

SYSTEM_PROMPT = """
You are an educational food label analyst and ingredient de-shrouder for "Label Dekho India".
Analyze the food label image provided in context with the user's optional profile indicators.

OUTPUT SCHEMA (Strict JSON):
{
  "product_name": "String (Detected product name)",
  "nova_group": Integer (1 to 4: 1=Unprocessed, 2=Processed culinary, 3=Processed, 4=Ultra-Processed),
  "nova_label": "String (e.g., Ultra-Processed Food)",
  "personalized_verdict": {
    "is_suitable": Boolean,
    "verdict_tag": "String (e.g., 'General Caution', 'Moderate Choice', 'Suitable Option')",
    "personalized_warning": "String (Educational note comparing label macros/additives against profile preferences like low sugar, high sodium, etc.)"
  },
  "marketing_vs_reality": {
    "claim": "String (Front of pack marketing claims)",
    "truth": "String (Back of pack ingredient reality contrast)"
  },
  "visual_metrics": {
    "sugar_g_per_100g": Float,
    "sugar_teaspoons": Float,
    "fat_g_per_100g": Float,
    "palm_oil_ml": Float,
    "paratha_fat_equivalent": Float
  },
  "deshrouded_additives": [
    {
      "code_or_name": "String (e.g., INS 150d or Maltodextrin)",
      "simple_explanation": "String (Plain English/Hinglish explanation)"
    }
  ],
  "audio_script_hi": "String (A short 15-20 second audio summary in simple Hinglish highlighting product ingredients and educational warnings)",
  "disclaimer": "AI-generated educational information only. Not medical advice or diagnosis. Consult a qualified healthcare professional for dietary needs."
}

MANDATORY LEGAL RULES:
1. Do NOT diagnose, prevent, or treat any medical condition. Frame all findings as general nutritional education.
2. If severe allergen warnings apply, remind users to seek immediate medical attention if experiencing an emergency.
3. Always convert sugar (g) to teaspoons by dividing by 4.
4. Return ONLY valid JSON.
"""

def analyze_label_image(image_bytes: bytes, mime_type: str = "image/jpeg", user_profile: dict = None) -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    
    profile_prompt = f"User Profile Context (Educational/Synthetic): {json.dumps(user_profile if user_profile else {})}"
    user_message = f"{profile_prompt}\n\nAnalyze this food label image and return strict JSON according to the system instructions."

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[image_part, user_message],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)