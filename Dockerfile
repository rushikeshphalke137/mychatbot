FROM ubuntu

# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:1.10.2

MAINTAINER "Rohit Kumar"

# Change back to root user to install dependencies
USER root

#Work Directory
WORKDIR /app

#install git and cloning data
RUN apt-get update && apt-get upgrade -y &&  apt-get install -y git
RUN git clone  https://2b863d8ba6c117a331f107e08241d33a95c572a2:x-oauth-basic@github.com/NSSAC/chatbot.git

RUN ls
# Copying the cloned data to the work directory
#COPY . ./

RUN cp -R ./chatbot/* ./

RUN ls

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -U pip && pip install word2number && pip install dateparser
RUN pip3 install pandas

# By best practices, don't run the code with root user
USER 1001

CMD ["start", "--actions", "actions", "--debug"]
