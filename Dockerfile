FROM python:2.7

EXPOSE 8080

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "server.py"]