"""
main.py — START THE SERVER

Mental model:
  This file does not define routes. It only tells uvicorn:
    "load the FastAPI app object named `app` from module app.app"

  app.app means: package `app`, file `app.py`, variable `app = FastAPI()`
"""

import uvicorn

if __name__ == "__main__":
    # reload=True restarts server when you save files (dev only)
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
