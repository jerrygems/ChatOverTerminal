FROM python:3

WORKDIR /COT

COPY COT-Server.py /COT/
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "/COT/COT-Server.py" ]
