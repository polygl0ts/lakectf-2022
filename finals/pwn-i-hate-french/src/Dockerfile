# syntax=docker/dockerfile:latest
ARG UBUNTU_VERSION=18.04

################################################################################
# Binary builder -- such build, much wow                                       #
################################################################################
FROM --platform=linux/amd64 ubuntu:$UBUNTU_VERSION as builder

# Enable APT package caching
RUN rm -f /etc/apt/apt.conf.d/docker-clean && \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

# Install prerequisites
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        make

# Build the file
RUN --mount=type=bind,source=src,target=/src,readwrite \
    cd /src && \
    make all && \
    cp /src/sections /sections


