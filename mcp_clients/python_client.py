from smolagents import ToolCollection, CodeAgent
from mcp.client.stdio import StdioServerParameters

server_params = StdioServerParameters(command="python", args=["../frontend/app.py"])

with ToolCollection.from_mcp(server_params, trust_remote_code=True) as tools:
  agent = CodeAgent(tools=[*tools])
  result = agent.run("What subjects is student 1 taking?")
  print(result)

