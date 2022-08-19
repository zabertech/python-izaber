FROM ubuntu:20.04

# Copy over the data files
COPY . /src

# Let's sit in the src directory by default
WORKDIR /src

ENV PATH /root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Install all deps
RUN apt update \
    && apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && add-apt-repository ppa:pypy/ppa \
    && apt install -y \
              build-essential \
              curl \
              git \
              libssl-dev \
              libxml2-dev \
              libxslt1-dev \
              pypy3 \
              pypy3-dev \
              python2.7 \
              python2.7-dev \
              python3-distutils \
              python3.6 \
              python3.6-dev \
              python3.6-distutils \
              python3.7 \
              python3.7-dev \
              python3.7-distutils \
              python3.8 \
              python3.8-dev \
              python3.8-distutils \
              python3.9 \
              python3.9-dev \
              python3.9-distutils \
              python3.10 \
              python3.10-dev \
              python3.10-distutils \
              python3.11 \
              python3.11-dev \
              python3.11-distutils \
              vim-nox \
    # Pip is handy to have around
    && curl https://bootstrap.pypa.io/get-pip.py -o /root/get-pip.py \
    && python3 /root/get-pip.py \
    # Poetry is used managing deps and such
    && curl -sSL https://install.python-poetry.org -o /root/install-poetry.py \
    && python3 /root/install-poetry.py \
    # We also use Nox
    && python3 -m pip install nox \
    # SETUP Environment
    && /src/docker/setup-env.sh \
    # Cleanup caches to reduce image size
    && pip cache purge \
    && apt clean \
    && rm -rf ~/.cache \
    && rm -rf /var/lib/apt/lists/* \
    ;

# Then this will execute the test command
CMD /src/docker/run-test.sh

