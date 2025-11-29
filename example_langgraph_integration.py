from ollama import Client

# Create a client connected to our Ollama container
client = Client(host='http://localhost:11434')

def query_model(model_name, prompt):
    """Function to query a specific model with a prompt"""
    response = client.generate(
        model=model_name,
        prompt=prompt
    )
    return response

# Example usage
if __name__ == "__main__":
    # Test with one of the Team A models
    model_name = "deepseek-r1:32b"
    prompt = "Solve this logic puzzle: If all Bloops are Razzies and some Razzies are Loppies, are all Bloops definitely Loppies?"
    
    print(f"Querying {model_name} with: {prompt}")
    
    response = query_model(model_name, prompt)
    
    print(f"Response: {response['response']}")