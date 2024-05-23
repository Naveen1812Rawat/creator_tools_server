from fastapi.responses import FileResponse
import subprocess
import os

class RequestVideo:
    def __init__(self, url, output_dir, YOUTUBE_DL_PATH):
        self.video_url = url
        self.save_path = output_dir
        self.YOUTUBE_DL_PATH = YOUTUBE_DL_PATH

    def download_video(self):
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # Generate a temporary file name
        print(self.save_path)
        output_template = os.path.join(self.save_path, '%(title)s.%(ext)s')

        # Use yt-dlp to download the video
        result = subprocess.run(
            [self.YOUTUBE_DL_PATH, "-o", output_template, self.video_url],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"yt-dlp error: {result.stderr}")
            raise HTTPException(status_code=400, detail=result.stderr)

        # Find the downloaded file
        downloaded_files = os.listdir(self.save_path)
        if not downloaded_files:
            print("No files found in the download directory.")
            raise HTTPException(status_code=404, detail="Video not found")

        # Assuming we download only one video at a time
        downloaded_file = downloaded_files[0]
        file_path = os.path.join(self.save_path, downloaded_file)

        if not os.path.exists(file_path):
            print(f"Downloaded file does not exist: {file_path}")
            raise HTTPException(status_code=404, detail="Video file not found")
        FileResponse(path=file_path, filename=downloaded_file)


