FROM ubuntu:20.04
LABEL MAINTAINER monandkey <satoru070505@gmail.com>

RUN apt update && apt-get install -y \
    make \
    g++ \
    libsctp-dev \
    lksctp-tools \
    iproute2 \
    libssl-dev \
    nano \
    wget \
    iputils-ping \
    net-tools

WORKDIR /
RUN wget https://github.com/Kitware/CMake/releases/download/v3.19.4/cmake-3.19.4.tar.gz && \
    tar -zxvf cmake-3.19.4.tar.gz && \
    rm cmake-3.19.4.tar.gz

WORKDIR /cmake-3.19.4
RUN ./bootstrap
RUN make && \
    make install

ENV UERANSIM_VERSION=v3.1.9
WORKDIR /
RUN wget https://github.com/aligungr/UERANSIM/archive/${UERANSIM_VERSION}.tar.gz && \
    mkdir UERANSIM && \
    tar -zxvf ${UERANSIM_VERSION}.tar.gz -C UERANSIM --strip-components 1 && \
    rm ${UERANSIM_VERSION}.tar.gz

WORKDIR /UERANSIM
RUN make

VOLUME [ "/UERANSIM/build/config" ]
ENTRYPOINT [ "/UERANSIM/build" ]
