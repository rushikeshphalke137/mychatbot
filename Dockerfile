# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:1.10.2

MAINTAINER "Rohit Kumar"

# Use subdirectory as working directory
WORKDIR /app

# Change back to root user to install dependencies
USER root

#Installing git and cloning the data from the gitHub
RUN apt-get update && apt-get upgrade -y &&  apt-get install -y git
RUN git clone https://rohit-persistent:GitHu3Passw0rd@github.com/NSSAC/chatbot.git

# Installing extra requirements for actions code
RUN pip install -U pip && pip install word2number && pip install dateparser
RUN pip3 install pandas

#Adding the codebase to our work directory
RUN cp -R ./chatbot/* ./

# By best practices, don't run the code with root user
USER 1001

CMD ["start", "--actions", "actions", "--debug"]
