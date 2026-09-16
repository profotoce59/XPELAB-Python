"""Application entry point.

Run it with:
    uvicorn src.main:app --reload --port 3000
or simply:
    python -m src.main
"""

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.routes import create_router


def create_app() -> FastAPI:
    load_dotenv()
    app = FastAPI(title="XPELAB Python API")
    app.include_router(create_router())
    return app


# uvicorn imports this module and looks for this variable.
app = create_app()


# `__name__` is "__main__" only when the file is executed directly, and the
# module name when it is imported. This is the Python idiom for "this is an
# executable script": without the guard, the server would also start when
# another module imports this one.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    print(f"Starting XPELAB Python API on http://0.0.0.0:{port}")
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
