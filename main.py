import uvicorn

from config import ProjectServer

if __name__ == "__main__":
    uvicorn.run(
        ProjectServer,
        host="127.0.0.1",
        port=8000,
        reload=False
    )
