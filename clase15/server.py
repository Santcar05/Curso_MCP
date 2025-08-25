from fastapi import FastAPI, UploadFile, File
from mcp.server.fastmcp import FastMCP
from PIL import Image
import numpy as np

# Servidor web FastAPI
app = FastAPI()

# Servidor MCP
mcp = FastMCP("MultimodalServer")

# Herramientas MCP
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def get_greeting(name: str) -> str:
    return f"Hello {name}"

# Endpoint HTTP normal (FastAPI, no MCP)
@app.post("/mcp/image/brightness")
async def brightness(file: UploadFile = File(...)):
    image = Image.open(file.file)
    image = np.array(image)
    brightness = np.mean(image)
    return {"brightness": float(brightness), "message": "Image brightness calculated successfully"}

# Montar MCP dentro de FastAPI
app.mount("/mcp", mcp)


#comando para ejecutar 
# uvicorn server:app --host 0.0.0.0 --port 8000
#npx.cmd @modelcontextprotocol/inspector mcp run server.py
# curl -X POST "https://localhost:8000/mcp/image/brightness" -H "Content-Type: multipart/form-data" -F "file=@image.jpg"