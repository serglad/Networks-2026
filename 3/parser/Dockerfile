FROM selenium/standalone-firefox:latest


ENV MOZ_HEADLESS=1


USER root

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY parser.py .
COPY .env .


EXPOSE 7777


USER seluser


CMD ["uvicorn", "parser:app", "--host", "0.0.0.0", "--port", "7777"]