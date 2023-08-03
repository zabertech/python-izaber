FROM ubuntu:20.04

ARG CONTAINER_UID=1000
ARG CONTAINER_GID=1000
ENV CONTAINER_UID $CONTAINER_UID
ENV CONTAINER_GID $CONTAINER_GID

ENV PATH /home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

ENV TZ America/Vancouver

# Install all deps
RUN apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -y software-properties-common \
    && DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:deadsnakes/ppa \
    && DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:pypy/ppa \
    && DEBIAN_FRONTEND=noninteractive apt install -y \
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
              python3-pip \
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
              python3.12 \
              python3.12-dev \
              python3.12-distutils \
              vim-nox \
    # Manually install virtualenv version so that we can use it across python3.6 and up
    # the most recent stuff breaks undef py 3.6
    && python3.6 -m pip install virtualenv \
    # We also use Nox
    && python3.6 -m pip install nox \
    # Cleanup caches to reduce image size
    && apt clean \
    && rm -rf ~/.cache \
    && rm -rf /var/lib/apt/lists/* \
    # Create the new user
    && groupadd -f -g $CONTAINER_GID ubuntu \
    && useradd -ms /bin/bash -d /home/ubuntu -G sudo ubuntu -u $CONTAINER_UID -g $CONTAINER_GID \
    && mkdir /app \
    && chown -R $CONTAINER_UID:$CONTAINER_GID /app \
    ;

# Switch to the ubuntu user
USER ubuntu

# Copy over the data files
COPY --chown=ubuntu:ubuntu . /src

# Let's sit in the src directory by default
WORKDIR /src

# Install all the required files
RUN cd /src \
    # Poetry is used managing deps and such
    && curl -sSL https://install.python-poetry.org -o /tmp/install-poetry.py \
    && python3.8 /tmp/install-poetry.py \
    && poetry install \
    && ls -l /src \
    # SETUP Environment
    && /src/docker/setup-env.sh \
    && :


# Then this will execute the test command
CMD /src/docker/run-test.sh

