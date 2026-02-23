import os
import traceback
from fastapi import FastAPI
from moviebox_api.cli import MovieAuto
from fastapi.middleware.cors import CORSMiddleware

# --- STEP 2 MODIFIED: THE BRAIN ---
# Ensure this matches your Cloudflare Worker URL EXACTLY (without https://)
OS_HOST = "movie-shield.names.workers.dev" 
os.environ["MOVIEBOX_API_HOST"] = OS_HOST

app = FastAPI()

# Allow Lovable/WebIntoApp to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "API is Live", "proxy_host": OS_HOST}

@app.get("/search")
async def search(q: str):
    try:
        # Initialize the MovieBox engine
        auto = MovieAuto()
        
        # Search for the movie
        result = await auto.run(q)
        
        if result and hasattr(result, 'url'):
            return {
                "title": q,
                "url": result.url,
                "status": "success"
            }
        else:
            return {
                "title": q,
                "url": None,
                "message": "Movie found but no streaming URL available.",
                "status": "not_found"
            }
            
    except Exception as e:
        # This prints the REAL error to your Render dashboard logs
        print(f"ERROR OCCURRED: {str(e)}")
        print(traceback.format_exc())
        
        return {
            "error": str(e),
            "hint": "Check Render Logs for the full Traceback",
            "status": "failed"
        }

if __name__ == "__main__":
    import uvicorn
    # Render uses port 10000 by default
    uvicorn.run(app, host="0.0.0.0", port=10000)
    
