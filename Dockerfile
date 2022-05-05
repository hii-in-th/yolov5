FROM tiangolo/uvicorn-gunicorn:python3.9-slim
RUN mkdir /yolov5-fastapi-test
COPY . /yolov5-fastapi-test
RUN cd /yolov5-fastapi-test \
	&& apt-get update \
	&& apt-get install git -y \
	&& ls -al \
	&& git clone -b  v6.1 https://github.com/ultralytics/yolov5.git \
	&& ls -al \
	&& pwd \
	&& ls -al yolov5 \
	&& apt-get install gcc ffmpeg libsm6 libxext6 openssh-client -y \
	&& pip install --upgrade pip \
	&& pip install --no-cache-dir --upgrade -r /yolov5-fastapi-test/requirements.txt \
	&& apt-get remove git -y \
	&& apt-get autoremove -y \
	&& rm -rf /var/lib/apt/lists/*
WORKDIR /yolov5-fastapi-test
VOLUME /yolov5-fastapi-test/model
CMD uvicorn main:app  --host=0.0.0.0 --port=${PORT:-8000}