FROM python:3.11.3

RUN mkdir /src
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
ENV PYTHONPATH /src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
