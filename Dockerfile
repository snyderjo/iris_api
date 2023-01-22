FROM python:3.10

WORKDIR /app

COPY requirements2.txt requirements2.txt
RUN pip3 install -r requirements2.txt

COPY . .

EXPOSE 5001

CMD ["gunicorn", "-b", "0.0.0.0:5001","app:app"]
