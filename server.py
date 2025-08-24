#server.py
from mcp.server.fastmcp import FastMCP

#Crear el servidor
mcp = FastMCP("Demo")

# Agregar una herramienta adicional
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

# Herramienta para restar
@mcp.tool()
def subtract(a: int, b: int) -> int:
    return a - b

# Herramienta para multiplicar
@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a * b

# Herramienta para dividir
@mcp.tool()
def divide(a: int, b: int) -> int:
    return a / b

# agregar un recurso dinamico
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello {name}"

# Otro recurso para despedirse
@mcp.resource("goodbye://{name}")
def get_goodbye(name: str) -> str:
    return f"Goodbye {name}"


##PARA EJECUTAR UTILIZAR EL SIGUIENTE COMANDO
# npx.cmd @modelcontextprotocol/inspector mcp run server.py