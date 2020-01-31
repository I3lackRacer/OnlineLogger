FROM python:3 as py
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4308

CMD [ "python", "./logger_server.py" ]