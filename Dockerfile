FROM ubuntu:20.04

# Add the python repo
RUN apt update ; apt install -y software-properties-common ; add-apt-repository ppa:deadsnakes/ppa

# Install all deps
RUN apt install -y python2.7 python2.7-dev python3.6 python3.7 python3.8 python3.9 libxml2-dev libxslt1-dev build-essential pypy3-dev python3.6-dev python3.7-dev python3.8-dev python3.9-dev libssl-dev curl python3-distutils ; curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

# Copy over the data files
COPY . /python-izaber

# SETUP Environment
RUN /python-izaber/docker/setup-env.sh

# Then this will execute the test command
CMD /python-izaber/docker/run-test.sh

