from fastapi import FastAPI, HTTPException, Depends, Response
from openai import OpenAI
from pydantic import BaseModel
import requests
import os
import io
import zipfile


TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")
client = OpenAI(api_key=TOGETHER_API_KEY,
                base_url='https://api.together.xyz',
                )



app = FastAPI()

@app.get("/")
def test_source():
    return "working"

class CodeGenerationRequest(BaseModel):
    model: str
    prompt: str
    system_prompt: str
    max_tokens: int
    frequency_penalty: float
    presence_penalty: float
    top_p: float
    temperature : float

@app.post("/generate-code/")
def get_code_completion(request_data: CodeGenerationRequest = Depends()):
    message = [
      {
            "role": "system",
            "content": 
            """
            You are an expert python selenium programmer. Write the code with the below constraints.
            Do not include explanations, question or other text content in the response. 
            Keep all the code inside two code blocks and name it as main.py or config.py.
            Code blocks should be grouped as scripts like main.py and config.py.
            Mention the script Names inside the codeblock.
            Code blocks should be grouped by script names like main.py and config.py.
            Code blocks should start with a [```] tag and end with a [```] tag.
            Keep the configurations and Main code in the seperate code blocks.
            If any of the constraints failed, it will not be considered as a valid response
            """
      },
      {
            "role": "user",
            "content":request_data.prompt 
           
      },
      ]
    chat_completion = client.chat.completions.create(
        messages=message,
        model="codellama/CodeLlama-70b-Instruct-hf",
        max_tokens=1000,
        frequency_penalty=0.7,
        presence_penalty=0.7,
        top_p=0.7,
        temperature=0.7,
        )
    response_content = chat_completion.choices[0].message.content
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('main.py', response_content)  # Writing main.py content
        
    
    # Seek to the beginning of the buffer
    zip_buffer.seek(0)

    # Create a response with the zip file
    response = Response(content=zip_buffer.getvalue(), media_type="application/octet-stream")
    response.headers["Content-Disposition"] = "attachment; filename=generated_code.zip"
    return response
    
