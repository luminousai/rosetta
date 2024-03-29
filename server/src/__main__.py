import uvicorn

from .app import app


def main():
    uvicorn.run(app, host="0.0.0.0", port=8081, reload=False)


if __name__ == "__main__":
    main()
