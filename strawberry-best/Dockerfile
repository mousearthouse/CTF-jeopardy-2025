FROM python:3.11-alpine

WORKDIR /app
COPY . .
COPY shared ./shared
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]