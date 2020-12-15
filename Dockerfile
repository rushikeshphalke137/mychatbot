# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:1.10.2

MAINTAINER "Rohit Kumar"

# Use subdirectory as working directory
WORKDIR /app

# Copying the codebase to the containers 
COPY . ./

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -U pip && pip install word2number && pip install dateparser
RUN pip3 install pandas

# By best practices, don't run the code with root user
USER 1001

CMD ["start", "--actions", "actions", "--debug"]
