FROM python:3.11-alpine

WORKDIR /app
COPY tgbot.py .
RUN pip install pyTelegramBotAPI

CMD ["python", "tgbot.py"]