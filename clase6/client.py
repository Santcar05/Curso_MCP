from mcp import ClientSession, StdioServerParameters,types
from mcp.client.stdio import stdio_client
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import json



server_params = StdioServerParameters(
    command="mcp",
    args=["run", "server.py"],
    env=None,
)


def convert_to_llm_tool(tool):
    tool_schema = {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema["properties"],
            },
        }
    }
    return tool_schema

    
def call_llm(prompt, functions):
    token = token_github_azure
    endpoint = "https://models.inference.ai.azure.com"
    
    model_name = "gpt-4o"

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(token))

    print("Calling llm")
    response = client.complete(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        tools=functions,
        temperature=1.,
        max_tokens=1000,
        top_p=1
    )

    tool_calls = []
    for choice in response.choices:
        if choice.message and choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                tool_calls.append({
                    "name": tc.function.name,
                    "args": json.loads(tc.function.arguments)
                })

    return tool_calls


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
            
            #Llamar herramienta
            tool = await session.call_tool("add", arguments ={"a": 1, "b": 2})
            print("Tool: ",tool.content)
            
            functions = []
            
            for tool in tools.tools:
                print("Tool: ",tool.name)
                print("Tool: ",tool.inputSchema["properties"])
                functions.append(convert_to_llm_tool(tool))
            
            prompt = "Add 2 to 20"
            #Ejecutar herramienta
            
            functions_to_call = call_llm(prompt, functions)
            for f in functions_to_call:
                result = await session.call_tool(f["name"], arguments = f["args"])
                print("TOOL Result: ",result.content)
       
if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
    
    
    
#Instalar modulo de azure
# pip install azure-ai-inference azure-core
