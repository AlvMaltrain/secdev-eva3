FROM jenkins/jenkins:lts-jdk17
USER root

#Docker CLI y git dentro de Jenkins
RUN apt-get update && apt-get install -y docker.io git && rm -rf /var/lib/apt/lists/*