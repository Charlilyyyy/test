pre : docker login

fe

# 1. Build Docker image
docker build -t charlilyyyy/test-fe:latest -t charlilyyyy/test-fe:3 .

# 2. Push both tags
docker push charlilyyyy/test-fe:latest
docker push charlilyyyy/test-fe:3

docker build -t charlilyyyy/test-fe:latest -t charlilyyyy/test-fe:3 .
docker push charlilyyyy/test-fe:latest
docker push charlilyyyy/test-fe:3

be

# 1. Build Docker image
docker build -t charlilyyyy/test-be:latest -t charlilyyyy/test-be:3 .

# 2. Push both tags
docker push charlilyyyy/test-be:latest
docker push charlilyyyy/test-be:3

docker build -t charlilyyyy/test-be:latest -t charlilyyyy/test-be:3 .
docker push charlilyyyy/test-be:latest
docker push charlilyyyy/test-be:3


to do :
1. make dockerfile can copy from my merc laptop
2. push to docker 
3. add documentation ho to run service locally and try run the service
4. check if frontend can ommunicate with backend
5. if cannot please change the api endpoint and it is according in .env
6. after settle , instead of .env please use secrets or configmap etc
7. watch webinar