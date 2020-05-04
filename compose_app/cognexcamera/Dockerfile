FROM  jjanzic/docker-python3-opencv
WORKDIR /home/cognexcamera
ADD http://static.matrix-vision.com/mvIMPACT_Acquire/2.37.1/install_mvGenTL_Acquire.sh /home/cognexcamera
ADD http://static.matrix-vision.com/mvIMPACT_Acquire/2.37.1/mvGenTL_Acquire-x86_64_ABI2-2.37.1.tgz /home/cognexcamera

RUN chmod ugo+x install_mvGenTL_Acquire.sh
RUN ./install_mvGenTL_Acquire.sh
 
RUN apt-get update -y 
COPY /requirements.txt /home/cognexcamera
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "camera.py"]