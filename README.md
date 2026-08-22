# 🇮🇳 Label Dekho India
> **AI-Powered Visual Food Label Decoder & Multilingual Audio Assistant**  
> *Built for the Food Pharmer Challenge*

---

## 📌 Overview
**Label Dekho India** transforms dense, fine-print food labels into instant visual metrics and regional audio summaries. By translating raw numerical data (e.g., "18g sugar per 100g") into real-world visual indicators (like physical teaspoons of sugar and palm oil volume), it bridges the literacy and language gap for Indian grocery shoppers.

---

## ✨ Key Features
* 🍬 **"Spoon & Cup" Visual Metrics:** Converts hidden sugar and fats into visual teaspoon/ml equivalents.
* ⚔️ **Marketing vs. Reality Split:** Exposes front-of-pack claims (e.g., *"Made with Real Atta"*) against back-of-pack truths (*"Contains 68% Maida"*).
* 🔊 **"Sahi Bhasha" Audio Summaries:** Generates 15-second native voice readouts in regional Indian languages (Hindi, Tamil, Telugu, Marathi, etc.).
* 🛑 **FSSAI De-shrouder:** Unmasks hidden sugars (Maltodextrin, Invert Sugar, Liquid Glucose) and INS additives.
* 🚦 **NOVA Processing Scale:** Assigns a clear visual processing rating from Level 1 (Whole Food) to Level 4 (Ultra-Processed Food).

---

## 🏗️ Architecture & Tech Stack

```text
  ┌─────────────────────────────────────────────────────────┐
  │                 FRONTEND: Next.js 14                    │
  │     (Tailwind CSS + Framer Motion / HTML5 Camera)       │
  └────────────────────────────┬────────────────────────────┘
                               │
                       HTTP REST API (JSON)
                               │
  ┌────────────────────────────▼────────────────────────────┐
  │                 API: Python FastAPI                 │
  │     (Hosted on Render - OpenAI GPT-4o + gTTS Engine)    │
  └─────────────────────────────────────────────────────────┘