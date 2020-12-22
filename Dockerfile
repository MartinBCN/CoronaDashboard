FROM python:3.8

COPY requirements.txt .

RUN pip install -r /requirements.txt

RUN pip install gunicorn

COPY . .

EXPOSE 8050

CMD ["python", "app.py"]