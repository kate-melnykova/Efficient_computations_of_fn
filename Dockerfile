FROM python:3.7.4

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    dos2unix && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app
RUN echo $PYTHONPATH

WORKDIR /app

COPY calcs/ .

RUN pip install --upgrade pip
RUN pip install -U -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"
RUN echo $PYTHONPATH

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN dos2unix /usr/local/bin/entrypoint.sh && \
    chmod a+x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]