#!/bin/bash

#curl -sS http://127.0.0.1:5000/service/status

export IMAGE_TAG=hiilab/test_detec:a2
export SERVICE_NAME=hii-yolov5

docker service scale ${SERVICE_NAME}=0
docker service rm ${SERVICE_NAME}
docker service create --replicas 1 \
    --name ${SERVICE_NAME} \
    --publish published=8213,target=8000 \
    --mount type=bind,src=/home/thanachai/yolov5_model,dst=/yolov5-fastapi-test/model \
    ${IMAGE_TAG}
    
docker service scale ${SERVICE_NAME}=1