FROM python:3.11-slim
WORKDIR /fastapi-microservice
COPY requirements.txt ./
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN pip install -r requirements.txt
ADD . ./
EXPOSE 5015
CMD /docker-entrypoint.sh
