# Overview
This is how to build docker image for pabot.

# Pabot?
A parallel executor for Robot Framework tests.
https://pabot.org/

# How to build
docker build command options
* -t: set tag robopabot:1.0 : change version as needed

```
cd (Dockerfile directory)

docker build \
--no-cache=true \
-t robopabot:1.0 .
```
