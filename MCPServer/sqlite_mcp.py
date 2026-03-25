import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_ollama import ChatOllama


# Initialize model and server parameters
model = ChatOllama(model="mistral", temperature=0.4)
server_params = StdioServerParameters(
    command="uv",
    args=[
        "--directory", 
        "D:\HopeAI\Assignments/22.MCPServer\servers-archived-main\src\sqlite",
        "run", 
        "mcp-server-sqlite",
        "--db-path",
        "D:\HopeAI\Assignments/22.MCPServer\mcp-sqlite-langchain\sqlite_mcp_langchain\database.db",
    ],
)

async def process_query(agent, query):
    response = await agent.ainvoke({"messages": query})
    return response["messages"][-1].content

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_agent(model, tools)
            
            print("SQLite Database Assistant (type 'exit' to quit)")
            
            while True:
                query = input("\nEnter your query: ").strip()
                if query.lower() == 'exit':
                    break
                if not query:
                    continue
                    
                print("\nProcessing...\n")
                response = await process_query(agent, query)
                print(f"\nAnswer: {response}")

if __name__ == "__main__":
    asyncio.run(main())