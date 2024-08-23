from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from function.screenshot import screenshot
from function.webTracker import track_usage
from database.db import get_detail
from model.model import (TimerState,ScreenShotTime)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get('/')
async def get_root():
    res = await get_detail()
    return res

@app.post('/screenshot')
async def read_screenshot(state: ScreenShotTime):
    import asyncio
    asyncio.create_task(screenshot(state.time))
    return {"message": "Screenshot taken", "time": state.time}

@app.post('/timer')
async def update_timer_state(state: TimerState):
    print(state.timerRunning)
    if state.timerRunning:
        # Run track_usage in the background
        import asyncio
        asyncio.create_task(track_usage())
    else: print("stop")
    return {"status": "success"}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
