#server.py
from mcp.server.fastmcp import FastMCP

#Crear el servidor
mcp = FastMCP("Demo")

# Agregar una herramienta adicional
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

# agregar un recurso dinamico
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello {name}"


##PARA EJECUTAR UTILIZAR EL SIGUIENTE COMANDO
# npx.cmd @modelcontextprotocol/inspector mcp run server.py