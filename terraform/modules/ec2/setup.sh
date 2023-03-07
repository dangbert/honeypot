#!/bin/bash
set -e

function main() {
  # if args:
  while getopts "r" arg; do
    case $arg in
    #h | --help)
    #    usage
    #    ;;
    r)
      redeploy
      exit
      ;;
    esac
  done

  sudo yum update -y
  sudo yum install -y git

  ensure_docker
  ensure_ssh_keys

  echo -e "\nsetup.sh complete!"

}

function ensure_docker {
  if [[ ! `command -v docker` || ! `command -v docker-compose` ]]; then
    sudo yum install -y docker
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
    sudo chmod a+x /usr/bin/docker-compose
    sudo systemctl enable docker && sudo systemctl start docker
  else
     echo "docker already installed ✅"
  fi
}

function ensure_ssh_keys {
 if [ `ls ~/.ssh/id* 2>/dev/null | wc -l` -eq 0 ]; then
   echo "creating ssh keys"
   #ssh-keygen -t ed25519 -C "$USER@$HOSTNAME"
   ssh-keygen -t ed25519 -C "$USER@$HOSTNAME" -f ~/.ssh/id_ed25519 -N ""
   echo -e "\npublic key is:"
   cat ~/.ssh/id_ed25519.pub
   echo "visit https://github.com/settings/ssh/new to add to github"
 else
   echo "ssh key already exists ✅"
 fi
}

function redeploy() {
  echo "deploying website..."
  cd ~/docker
  sudo docker load < image.tar
  mkdir -p ../flask # prevent docker-compose error
  sudo docker-compose up -d
}

main "$@"
