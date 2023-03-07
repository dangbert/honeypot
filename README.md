# Setup:

1. Launch EC2 instance with necessary dependencies:
````bash
cd terraform/instances/example
terraform init
terraform apply
````

2. Build docker image
````bash
cd docker && cp .env.sample .env

cd ../terraform
# build and export docker image to image.tar
# and copy docker folder to server
./deploy.py example --build --push
````

3. Start service on server:
````bash
# from terraform directory
cd example
terraform output

# now use ssh command outputted to enter server and (re)start website with:
./setup.py -r

#sudo docker run --rm -p 80:5000 --name honey honey_flask:latest python
````