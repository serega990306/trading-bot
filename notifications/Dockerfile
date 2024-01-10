FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN apt update
RUN apt install sqlite3

RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

COPY src .

EXPOSE 8000/tcp

CMD ["/usr/local/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "120", "-k", "uvicorn.workers.UvicornWorker", "main:app"]