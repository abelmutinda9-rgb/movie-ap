import os
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Correct Import according to official documentation
from moviebox_api import MovieAuto 

# --- STEP 2: THE BRAIN ---
# Your Cloudflare Worker URL (ensure it matches exactly)
OS_HOST = "movie-shield.names.workers.dev" 
os.environ["MOVIEBOX_API_HOST"] = OS_HOST

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "API is Live", "proxy": OS_HOST}

@app.get("/search")
async def search(q: str):
    try:
        # MovieAuto is the main class for searching and getting links
        auto = MovieAuto()
        
        # This function searches and returns the best matching movie object
        # Note: Depending on library version, this might be 'await auto.run(q)' 
        # or just 'auto.run(q)'. We'll use the async version from docs.
        result = await auto.run(q)
        
        if result and hasattr(result, 'movie_file'):
            return {
                "title": q,
                "url": result.movie_file.url if hasattr(result.movie_file, 'url') else "Link hidden",
                "status": "success"
            }
        else:
            return {"title": q, "url": None, "message": "Search completed, but no direct link found."}
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
    
