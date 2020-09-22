# Extend the official Rasa SDK image
FROM ubuntu
FROM rasa/rasa-sdk:1.10.2

MAINTAINER "Rohit Kumar"

USER root

# Use subdirectory as working directory
WORKDIR /appp


RUN apt-get update && apt-get upgrade -y &&  apt-get install -y git
RUN git clone https://2b863d8ba6c117a331f107e08241d33a95c572a2:x-oauth-basic@github.com/NSSAC/chatbot.git .


# Copying the codebase to the containers 
#COPY . ./

# Change back to root user to install dependencies
#USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -U pip && pip install word2number && pip install dateparser
RUN pip3 install pandas

# By best practices, don't run the code with root user
USER 1001

CMD ["start", "--actions", "actions", "--debug"]
