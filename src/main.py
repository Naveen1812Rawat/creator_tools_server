from fastapi import FastAPI, HTTPException
from services.video_service import RequestVideo
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Path to yt-dlp executable (assuming it is installed via pip)
YOUTUBE_DL_PATH = "yt-dlp"  # yt-dlp should be in PATH if installed via pip

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/download/")
async def download_video(url: str):
    try:
        # Ensure output directory exists
        obj = RequestVideo(url, "downloads", YOUTUBE_DL_PATH)
        res = obj.download_video()
        return f"your video is downloaded at {str(res)}"

    except Exception as e:
        print(f"Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=35444)
