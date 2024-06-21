from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pytube import YouTube
import re

app = FastAPI(openapi_url="/api/ytdownloader.openapi.json")

class VideoURL(BaseModel):
    url: str

def download_video(url, resolution):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
        if stream:
            stream.download()
            return True, None
        else:
            return False, "Video with the specified resolution not found."
    except Exception as e:
        return False, str(e)

def get_video_info(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.first()
        video_info = {
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "views": yt.views,
            "description": yt.description,
            "publish_date": yt.publish_date,
        }
        return video_info, None
    except Exception as e:
        return None, str(e)

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?$"
    return re.match(pattern, url) is not None

@app.post("/download/{resolution}")
async def download_by_resolution(resolution: str, video_url: VideoURL):
    url = video_url.url
    
    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL.")
    
    success, error_message = download_video(url, resolution)
    
    if success:
        return {"message": f"Video with resolution {resolution} downloaded successfully."}
    else:
        raise HTTPException(status_code=500, detail=error_message)

@app.post("/video_info")
async def video_info(video_url: VideoURL):
    url = video_url.url
    
    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL.")
    
    video_info, error_message = get_video_info(url)
    
    if video_info:
        return video_info
    else:
        raise HTTPException(status_code=500, detail=error_message)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
