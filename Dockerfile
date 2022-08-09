FROM python:3.8-slim-buster

WORKDIR /arconverter

COPY src/requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=./src/app.py

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]