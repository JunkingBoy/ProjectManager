import uvicorn

from config import ProjectServer

if __name__ == "__main__":
    uvicorn.run(
        ProjectServer,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
