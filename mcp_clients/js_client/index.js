import { Client } from "@huggingface/mcp-client";

const client = new Client();

async function main() {
  await client.connect({
    transport: {
      type: "sse",
      url: "http://localhost:7860/gradio_api/mcp/sse"
    }
  });

  const tools = await client.listTools();
  console.log("Available tools:", tools);

  const response = await client.callTool({
    tool: "get_student_subjects",
    input: { student_id: 1 }
  });

  console.log("Tool response:", response.output);
}

main().catch(console.error);
