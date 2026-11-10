FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt
COPY app ./app
EXPOSE 8000
# Render indica el puerto en la variable PORT; en local se usa 8000
CMD uvicorn app.main:app --host 0.0.0.0 \
    --port ${PORT:-8000}
