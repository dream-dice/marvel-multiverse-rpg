FROM python:3.11-slim

RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/web
RUN npm install
RUN npm run build

WORKDIR /app
CMD ["python", "app.py"]
