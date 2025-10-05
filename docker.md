pre : docker login

fe

# 1. Build Docker image
docker build -t charlilyyyy/test-fe:latest -t charlilyyyy/test-fe:4 .

# 2. Push both tags
docker push charlilyyyy/test-fe:latest
docker push charlilyyyy/test-fe:4

docker build -t charlilyyyy/test-fe:latest -t charlilyyyy/test-fe:4 .
docker push charlilyyyy/test-fe:latest
docker push charlilyyyy/test-fe:4

be

# 1. Build Docker image
docker build -t charlilyyyy/test-be:latest -t charlilyyyy/test-be:4 .

# 2. Push both tags
docker push charlilyyyy/test-be:latest
docker push charlilyyyy/test-be:4

docker build -t charlilyyyy/test-be:latest -t charlilyyyy/test-be:4 .
docker push charlilyyyy/test-be:latest
docker push charlilyyyy/test-be:4


to do :
1. make dockerfile can copy from my merc laptop
2. push to docker 
3. add documentation ho to run service locally and try run the service
4. check if frontend can ommunicate with backend
5. if cannot please change the api endpoint and it is according in .env
    - done: get api when expose
    - done: need api connot open in browser
6. done :after settle , instead of .env please use secrets or configmap etc
7. watch webinar
8. instead of configmap , watch how odin do and use direct from keyvault ,and use azure id managed identity later
9. security implementation cicd