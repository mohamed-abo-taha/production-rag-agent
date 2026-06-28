"""Start the FastAPI server.

Usage:
    python -m scripts.run_api          # then open http://localhost:8000/docs
"""

from __future__ import annotations

import uvicorn


def main() -> None:
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
