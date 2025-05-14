from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os, uuid, json, re
import qrcode
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "data")
QR_DIR = os.getenv("QR_DIR", "qrcodes")
METADATA_FILE = os.getenv("METADATA_FILE", "metadata.json")


# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(QR_DIR, exist_ok=True)

def sanitize_filename(filename):
    # Replace whitespace with underscores and remove problematic characters
    return re.sub(r'\s+', '_', filename)
router = APIRouter()

def load_metadata():
    try:
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

@router.get("/data/{code}")
async def get_file(code: str):
    metadata = load_metadata()  # Load metadata only once here
    file_path = metadata.get(code)
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)

@router.get("/qr/{code}.png")
async def get_qr_code(code: str):
    qr_path = os.path.join(QR_DIR, f"{code}.png")
    if not os.path.exists(qr_path):
        raise HTTPException(status_code=404, detail="QR code not found")
    return FileResponse(qr_path, media_type="image/png")

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    code = uuid.uuid4().hex[:6]
    safe_filename = sanitize_filename(file.filename)
    file_path = os.path.join(DATA_DIR, f"{code}_{safe_filename}")

    # Save the file to disk
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Update the metadata with the new file
    metadata = load_metadata()  # Load metadata only once here
    metadata[code] = file_path
    print(f"Updated metadata: {metadata}")  # Debugging print to check metadata

    # Write the updated metadata back to the file
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f)

    # Generate QR code URL
    download_url = f"http://localhost:8000/data/{code}"
    qr_img = qrcode.make(download_url)
    qr_path = os.path.join(QR_DIR, f"{code}.png")
    qr_img.save(qr_path)

    return JSONResponse(content={
        "id": code,
        "file_url": download_url,
        "qr_url": f"http://localhost:8000/qr/{code}.png"
    })

