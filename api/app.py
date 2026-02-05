import json
import uuid
import threading
import time
import webbrowser
from pathlib import Path
from contextlib import asynccontextmanager

import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import HTTPException
from urllib.parse import quote

# ==================================================
# パス解決（通常 / PyInstaller 両対応）
# ==================================================
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

# ==================================================
# 設定ファイル読み込み
# ==================================================
CONFIG_PATH = BASE_DIR / "config.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

DATA_DIR = Path(config["data_dir"])
DATA_DIR.mkdir(parents=True, exist_ok=True)

FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR / "assets"

# ==================================================
# サーバ起動
# ==================================================
def start_server():
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_config=None,
        access_log=False
    )

# ==================================================
# FastAPI
# ==================================================
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# React build をマウント
app.mount("/assets", StaticFiles(directory=STATIC_DIR), name="assets")

@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")

# ==================================================
# API: ファイル作成
# ==================================================
@app.post("/api/files")
def create_file():
    filename = f"{uuid.uuid4().hex}.txt"
    path = DATA_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        f.write("Hello from FastAPI\n")

    return {"filename": filename}

# ==================================================
# API: ファイル一覧
# ==================================================
@app.get("/api/files")
def list_files():
    return {
        "files": [f.name for f in DATA_DIR.iterdir() if f.is_file()]
    }

# ==================================================
# API: ファイル取得
# ==================================================
@app.get("/api/files/{filename}")
def download_file(filename: str):
    file_path = DATA_DIR / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
        filename=filename,
        headers={
            # 日本語ファイル名対策（Windows + Chrome 安定）
            "Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"
        }
    )

# ==================================================
# ローカル起動用（python app.py）
# ==================================================
if __name__ == "__main__":
    # FastAPI サーバ起動
    server_thread = threading.Thread(
        target=start_server,
        daemon=True
    )
    server_thread.start()

    # サーバ起動待ち
    time.sleep(1.5)

    # ブラウザ起動
    webbrowser.open("http://127.0.0.1:8000")

    # プロセスを生かす（←これがないと exe 即終了）
    while True:
        time.sleep(1)