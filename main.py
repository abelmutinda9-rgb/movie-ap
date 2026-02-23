import os, random, asyncio
from fastapi import FastAPI
from moviebox_api.cli import MovieAuto
from fastapi.middleware.cors import CORSMiddleware

# This uses your Cloudflare Shield to stay hidden
os.environ["MOVIEBOX_API_HOST"] = "abel.mutindaabel6.workers.dev" 

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/search")
async def search(q: str):
    try:
        # ANTI-BLOCK: Human Delay Jitter (1 to 3 seconds)
        await asyncio.sleep(random.uniform(1, 3))
        
        auto = MovieAuto()
        result = await auto.run(q)
        return {"title": q, "url": result.url if result else "None"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
  
