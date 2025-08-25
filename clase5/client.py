from mcp import ClientSession, StdioServerParameters,types
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="mcp",
    args=["run", "server.py"],
    env=None,
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            #Bloque para enlistar herrramientas y recursos del server(igual que en el inspector)
            resources = await session.list_resources()
            print("LISTING RESOURCES")
            for resource in resources:
                print("Resource: ",resource)
            print("END LISTING RESOURCES")
            
            tools = await session.list_tools()
            print("LISTING TOOLS")
            for tool in tools.tools:
                print("Tool: ",tool.name)
            print("END LISTING TOOLS")
            
            #Leer recursos
            print("Reading resource")
            resource = await session.read_resource("greeting://hello")
            print("Resource: ",resource)
            
            #Leer herramientas
            tool = await session.call_tool("add", arguments ={"a": 1, "b": 2})
            print("Tool: ",tool.content)
            
            #Ejecutar herramienta
       
if __name__ == "__main__":
    import asyncio
    asyncio.run(run())