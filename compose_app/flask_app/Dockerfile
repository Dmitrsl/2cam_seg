FROM   jjanzic/docker-python3-opencv

WORKDIR /home/flask_app
RUN apt-get update -y 
 
COPY /requirements.txt /home/flask_app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "flask_server.py"]
