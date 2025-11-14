from typing import List
from pathlib import Path
from app.servers.mcp.server import app

# Resource for suggested Wikipedia topics, the file://suggested_titles as as the resource identifier
@app.resource("file://suggested_titles")
def suggested_titles() -> List[str]:
    """
    Read and return suggested Wikipedia topics from a local file.
    """
    try:
        path = Path("suggested_titles.txt")
        if not path.exists():
            return ["File not found"]
        return path.read_text(encoding="utf-8").strip().splitlines()
    except Exception as e:
        return [f"Error reading file: {str(e)}"]

