#### target for building flask backend container: ####
#  https://registry.hub.docker.com/_/python/
FROM python:3.8.12-slim AS flask_common
# need a c compiler to build uwsgi pip package:
RUN apt-get update && apt-get install -y gcc build-essential python-dev
RUN apt install -y libpq-dev
WORKDIR /app
# for better caching, install requirements.txt first:
COPY requirements.txt .
RUN pip3 install -r requirements.txt 

# copy whole flask folder:
COPY ./ .

FROM flask_common as flask_prod
RUN apt remove -y gcc build-essential python-dev && apt autoremove -y
CMD uwsgi --ini app.ini

FROM flask_common as flask_dev
# run flask on container's IP rather than localhost:
#   https://stackoverflow.com/a/56438755
#CMD flask run -h $(hostname -i)
