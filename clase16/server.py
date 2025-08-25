from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Servidor MCP con contexto mutable")

root_context = {"message": "Hello world!", "user_data": {}}


@mcp.tool()
def update_context(user_id: str, new_message: str) ->dict:
    root_context["user_data"][user_id] = new_message
    return root_context


@mcp.tool()
def get_root_context() -> dict:
    return root_context


if __name__ == "__main__":
    mcp.run()