#Base image
FROM ubuntu

#Extend the official Rasa SDK image
FROM rasa/rasa-sdk:1.10.2

MAINTAINER "Rohit Kumar"

#Change back to root user to install dependencies
USER root

#Work Directory
WORKDIR /app

#Installing git and cloning the data from the gitHub
RUN apt-get update && apt-get upgrade -y &&  apt-get install -y git
RUN git clone https://github.com/NSSAC/chatbot.git

#Adding the codebase to our work directory
RUN cp -R ./chatbot/* ./

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -U pip && pip install word2number && pip install dateparser
RUN pip3 install pandas

# By best practices, don't run the code with root user
USER 1001

CMD ["start", "--actions", "actions", "--debug"]
