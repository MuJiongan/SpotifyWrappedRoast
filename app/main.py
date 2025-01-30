from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from app.spotify import search_tracks, get_track_features
from app.analyzer import analyze_personality
from pydantic import BaseModel
from typing import List, Optional
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the data models
class Song(BaseModel):
    id: str
    name: str
    artist: str
    album: str
    albumImage: Optional[str] = None  # Make albumImage optional
    previewUrl: Optional[str] = None  # Make previewUrl optional

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/search")
async def search(q: str):
    try:
        tracks = search_tracks(q)
        return JSONResponse(tracks)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/analyze")
async def analyze(songs: List[Song]):
    try:
        logger.debug(f"Received songs for analysis: {songs}")
        songs_with_features = []
        for song in songs:
            logger.debug(f"Processing song: {song.name} by {song.artist}")
            songs_with_features.append({
                **song.dict(),
            })
        
        logger.debug("Getting personality analysis...")
        analysis = analyze_personality(songs_with_features)
        return JSONResponse({"analysis": analysis})
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}", exc_info=True)
        return JSONResponse({"error": str(e)}, status_code=500) 