FROM python:latest
RUN mkdir /usr/local/server
WORKDIR /usr/local/server
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5050
CMD [ "python3","backend/server.py" ]