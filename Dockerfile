# start by pulling the python image
FROM python:3.9-alpine3.18

# copy every content from the local file to the image
COPY . /app

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

EXPOSE $PORT

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]