# Setup:

````bash
cd terraform
terraform init
terraform apply
````


````bash
cd docker
cp .env.sample .env
sudo docker-compose build

# export image
sudo docker image save honey_flask -o image.tar
sudo chmod 664 image.tar

scp -i ../terraform/honey-key.pem -r `pwd`  ec2-user@<EC2_IP>
````

On ec2 instance:

(note this could be a setup.sh script that terraform runs on the instance)
````bash
sudo yum update && sudo yum install -y docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
sudo chmod a+x /usr/bin/docker-compose
sudo systemctl enable docker && sudo systemctl start docker

# enter folder that was copied through scp:
cd docker/
sudo docker load < image.tar
mkdir ../flask # prevent docker-compose error

sudo docker-compose up

#sudo docker run --rm -p 80:5000 --name honey honey_flask:latest python
````