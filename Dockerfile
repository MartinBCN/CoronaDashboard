FROM python:3.8

ENV DATA_DIR=/data

COPY requirements.txt .

RUN pip install -r /requirements.txt

COPY . .

COPY /corona .

EXPOSE 8050

CMD ["python", "app.py"]