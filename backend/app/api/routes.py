from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os, uuid, json
import qrcode

router = APIRouter()


DATA_DIR = "data"
QR_DIR = "qrcodes"
METADATA_FILE = "metadata.json"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(QR_DIR, exist_ok=True)

# Load metadata or create empty
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)
else:
    metadata = {}

@router.get("/data/{id}")
async def get_data_by_id(id: str):
    file_path = f"data/{id}_file.txt"

    if os.path.exists(file_path):
        return FileResponse(file_path)

    raise HTTPException(status_code=404, detail="File not found")

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    code = uuid.uuid4().hex[:6]
    file_path = os.path.join(DATA_DIR, f"{code}_{file.filename}")

    try:
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)
    except json.JSONDecodeError:
        metadata = {}

    with open(file_path, "wb") as f:
        f.write(await file.read())

    metadata[code] = file_path
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f)

    download_url = f"http://localhost:8000/data/{code}"
    qr_img = qrcode.make(download_url)
    qr_path = os.path.join(QR_DIR, f"{code}.png")
    qr_img.save(qr_path)

    return FileResponse(qr_path, media_type="image/png")

