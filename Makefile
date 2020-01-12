
build:
    docker build -t kbsbot_compose_engine . -f docker/Dockerfile

run:
    docker run --rm  --name=compose-engine -p 5000:8001 -it kbsbot_compose_engine




