FROM python:3.8

COPY requirements.txt .

RUN pip install -r /requirements.txt

ADD corona /app/
ADD data /app/data


WORKDIR /app

EXPOSE 8050

CMD ["python", "app.py"]