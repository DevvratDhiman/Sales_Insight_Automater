from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file(file: UploadFile):
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Only CSV or XLSX allowed")
    file.file.seek(0, 2)  # move pointer to end
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

def validate_email(email: str):
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email")