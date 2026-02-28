from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from regguard_swarm import RegGuardSwarm
from pypdf import PdfReader
import io
import base64

app = FastAPI(title="RegGuard AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend HTML + assets
app.mount("/static", StaticFiles(directory="static"), name="static")

class TextQuery(BaseModel):
    description: str

rg = RegGuardSwarm()

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/classify")
def classify_text(query: TextQuery):
    return {"result": rg.run_full_swarm(query.description)}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        text = "".join(page.extract_text() or "" for page in reader.pages)
        description = f"Uploaded PDF '{file.filename}': {text[:3000]}..."
    else:
        base64_img = base64.b64encode(content).decode('utf-8')
        description = f"Uploaded image '{file.filename}' (base64): {base64_img[:500]}..."
    return {"result": rg.run_full_swarm(description)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)