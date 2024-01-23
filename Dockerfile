# start by pulling the python image
FROM python:3.10-bookworm

# copy every content from the local file to the image
COPY . /app

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# EXPOSE 5000
EXPOSE $PORT
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app
# # configure the container to run in an executed manner
# ENTRYPOINT [ "python" ]

# CMD ["app.py" ]