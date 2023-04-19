FROM python:3.9.7
# This defines the current working directory
# this is where all the comands are run from
WORKDIR /usr/src/app
# We copy our req.txt file into the container
# We also have to specify the path ./
# Because we have a WORKDIR we can use ./ otherwise we need to use the full path
COPY requirements.txt ./
# comand for istalling all dependencies
RUN pip install --no-cache-dir -r requirements.txt
# This copies everything from our current directory in the container dir
# If we hadn't specified workdir it needs to be -> . /usr/src/app
COPY . . 
# Run the command to start the application
# Everytime there is a space in the command we have to split it up between quotation marks
# Docker specific syntax
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Next step is to create a Docker build
# In the CLI Terminal Execute
# docker build --help
# docker build -t AndYourPersonalNameOfTheBuild .
# example
# docker build -t fastapi .
# check the image in CLI ->
# docker image ls