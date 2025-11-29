/*
Example n8n workflow configuration for Ollama API integration

To use this in n8n:

1. Create an HTTP Request node
2. Set Method to POST
3. Set URL to: http://HOST_IP:11434/api/generate
4. Set Body Content Type to JSON
5. Use the following JSON structure in the body:

{
  "model": "qwen2.5-coder",
  "prompt": "buatkan kode go"
}

6. You can parameterize the model and prompt based on previous nodes
7. The response will contain the AI-generated content in the "response" field

Additional notes:
- Replace HOST_IP with the actual IP where your Ollama container is running
- In a Docker setup, this would typically be the host's IP address
- You can also use http://nexaforge-ollama:11434/api/generate if using Docker networking
*/

Example n8n node configuration (JSON format):

{
  "parameters": {
    "method": "POST",
    "url": "http://localhost:11434/api/generate",
    "body": {
      "model": "={{ $json.model }}",
      "prompt": "={{ $json.prompt }}"
    },
    "options": {
      "response": "fullResponse",
      "responseFormat": "json",
      "timeout": 60000
    }
  },
  "name": "Ollama Query",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "position": [
    750,
    400
  ]
}