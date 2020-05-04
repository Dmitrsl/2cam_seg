FROM  pytorch/pytorch
WORKDIR /home/project
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
         dialog apt-utils \
         apt-utils \
         build-essential \
         cmake \
         git \
         curl \
         ca-certificates \
         zlib1g-dev \
         libgtk2.0-0 \
         libjpeg62-dev \
         libglib2.0-dev \
         libsm6 \
         libxext6 \
         libxrender1 \
         libxrender-dev \
         libpng-dev &&\
     rm -rf /var/lib/apt/lists/*
ADD http://static.matrix-vision.com/mvIMPACT_Acquire/2.37.1/install_mvGenTL_Acquire.sh /home/project
ADD http://static.matrix-vision.com/mvIMPACT_Acquire/2.37.1/mvGenTL_Acquire-x86_64_ABI2-2.37.1.tgz /home/project

RUN chmod ugo+x install_mvGenTL_Acquire.sh
RUN ./install_mvGenTL_Acquire.sh
COPY . /home/project
COPY requirements.txt /home/project
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "stream.py"]
