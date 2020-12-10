FROM python:3.6-buster

COPY requirements.txt /var/tmp/requirements.txt

RUN pip install -r /var/tmp/requirements.txt
RUN useradd -r -u 16139 worker
WORKDIR /home/worker
copy . .
RUN chown -R worker:worker .

USER worker

CMD ./run.py 3000
