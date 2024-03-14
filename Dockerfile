# 
FROM python:3.11-alpine
 
WORKDIR /app

COPY ./requirements.txt requirements.txt 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app 

EXPOSE 6102

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6102"]