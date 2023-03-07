## About
This project defines a **simple** website that tracks all visits to the site (storing user's IP, user agent, timestamp, visited link, and an optional token field that may be included in the URL).

Whenever someone visits the server's IP over http, the visit is logged to a json file in `~/data` (by default) on the server. All the logged data can be seen as json by visiting `http:SERVER_IP/report?pass=PASSWORD`.
  * Note: `PASSWORD` is defined implicitly by `flask/app/blueprints/tracker/__init__.py:PW_HASH`, but this should be moved to an ENV variable.
  * Only visits to the site at paths `/` and `/link` are logged.  These can all be seen on the `/report?pass=PASSWORD` page, and you can optionally filter these results with `/report?pass=PASSWORD&path=/link` and you can add `&t=TOKEN` to filter by some token, `t`, in the url the user visited (e.g. `/link?t=hello`).
  * Note that open connecting to the site, user's are redirected to the `REDIRECT_URL` set in the `docker/.env` file.

The site is implemented in Flask and can be easily/rapidly deployed to an EC2 instance with the commands below.

## Setup:


1. Launch EC2 instance with necessary dependencies:
````bash
cd terraform/instances/example
terraform init
terraform apply
````

2. Build docker image
````bash
# in terraform/ directory:
# build and export docker image to image.tar (and copy docker folder to server)
./deploy.py example --build --push
````

3. Start service on server:
````bash
# in terraform/ directory:
cd example
terraform output

# now use ssh command outputted to enter server and (re)start website with:
./setup.py -r
````
