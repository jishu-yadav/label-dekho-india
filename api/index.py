import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Force-load .env environment variables
load_dotenv()

from services.vision_agent import analyze_label_image
from services.audio_agent import generate_audio_base64

app = FastAPI(title="Label Dekho India API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "active", "project": "Label Dekho India"}
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "label-dekho-india-backend",
        "environment": "vercel-serverless"
    }
@app.post("/api/analyze")
async def analyze_label(
    file: UploadFile = File(...),
    user_profile: str = Form(default="{}"),
    lang: str = Form(default="hi")
):
    try:
        # Validate that the file is an image
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, 
                detail="Please upload a valid image file (JPG, PNG, WEBP)."
            )

        image_bytes = await file.read()
        mime_type = file.content_type or "image/jpeg"

        try:
            profile_data = json.loads(user_profile)
        except Exception:
            profile_data = {}

        # 1. Direct label & personalized analysis via Gemini
        analysis_data = analyze_label_image(image_bytes, mime_type, profile_data)

        # 2. Generate Hinglish audio summary
        audio_script = analysis_data.get("audio_script_hi", "Analysis complete.")
        audio_base64 = generate_audio_base64(audio_script, lang=lang)

        return JSONResponse(content={
            "status": "success",
            "data": analysis_data,
            "audio_base64": audio_base64
        })

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))