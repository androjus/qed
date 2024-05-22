FROM python:3.12.3

WORKDIR /app

COPY ./requirements/base.txt /tmp/base.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/base.txt

COPY . /app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]