import os
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# --- Setup ---
# Set this as an environment variable, e.g.:
#   export GEMINI_API_KEY="your-key-here"        (local)
#   or add it in your host's dashboard             (deployed)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

app = FastAPI()

# --- Enable CORS so the grader's Cloudflare Worker can call this API ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow requests from any origin
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Shape of the incoming request body ---
class QARequest(BaseModel):
    image_base64: str
    question: str


@app.post("/answer-image")
def answer_image(req: QARequest):
    # Decode the base64 string back into raw image bytes
    image_bytes = base64.b64decode(req.image_base64)

    # Ask the model to look at the image and answer the question
    prompt = (
        "Look at this image carefully and answer the question. "
        "Respond with ONLY the raw answer value — no units, no currency "
        "symbols, no explanation, no extra words.\n\n"
        f"Question: {req.question}"
    )

    response = model.generate_content(
        [
            {"mime_type": "image/png", "data": image_bytes},
            prompt,
        ]
    )

    answer_text = response.text.strip()

    # Always return the answer as a string
    return {"answer": answer_text}


# Optional: simple health check, useful for confirming the deploy is live
@app.get("/")
def health():
    return {"status": "ok"}
