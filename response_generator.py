from openai import AzureOpenAI

file_path = "api_key.txt"
key_endpoint = []

with open(file_path, "r") as file:
    for line in file:
        key_endpoint.append(line.strip())

def get_response(msg:str) -> str:
    client = AzureOpenAI(
        azure_endpoint = key_endpoint[1], 
        api_key = key_endpoint[0],  
        api_version = "2024-02-01"
    )
    response = client.chat.completions.create(
        model="Testbed", # model = "deployment_name".
        messages=[{"role": "user", "content": "as a robot, reply this message: "+msg}]
    )
    return response.choices[0].message.content