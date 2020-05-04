FROM  jjanzic/docker-python3-opencv
WORKDIR /home/webcamera
RUN apt-get update -y 
RUN pip install flask gunicorn
ENTRYPOINT ["python", "camera.py"]