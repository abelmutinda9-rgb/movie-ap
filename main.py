import os
import traceback
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Change the import to the base Client instead of the CLI
from moviebox_api.client import MovieBoxClient 

# --- STEP 2 MODIFIED: THE BRAIN ---
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
        # Using the Client directly is safer than the CLI 'MovieAuto'
        client = MovieBoxClient()
        
        # Search for the movie/series
        search_results = await client.search(q)
        
        if not search_results or len(search_results) == 0:
            return {"title": q, "url": None, "message": "No results found"}

        # Get the first result's detail to get the download/stream link
        first_item = search_results[0]
        item_id = first_item.get('id')
        
        # Fetch the download/stream info
        detail = await client.get_details(item_id)
        
        return {
            "title": first_item.get('name'),
            "url": detail.get('download_url') or detail.get('stream_url'),
            "status": "success"
        }
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
    
