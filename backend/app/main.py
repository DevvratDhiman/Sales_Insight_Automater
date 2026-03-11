from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.ai_engine import parse_sales_file, generate_ai_summary
from app.email_service import send_summary_email
from app.security import validate_file, validate_email


app = FastAPI(title="Sales Insight Automator API")

# Restrict CORS (frontend will run on localhost:3000 later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Sales Insight Automator API running"}

@app.post("/analyze")
async def analyze_sales(
    file: UploadFile = File(...),
    email: str = Form(...)
):
    try:
        # Validate email & file
        validate_email(email)
        validate_file(file)

        # Reset file pointer before reading
        file.file.seek(0)

        # Parse dataset
        df = parse_sales_file(file)

        # Generate AI summary
        summary = generate_ai_summary(df)

        # Send email
        send_summary_email(email, summary)

        return {
            "filename": file.filename,
            "email": email,
            "ai_summary": summary
        }

    except Exception as e:
        return {"error": str(e)}