FROM python:3.8

WORKDIR /code


COPY requirements.txt .


RUN pip install -r requirements.txt


COPY qaf/ .

# command to run on container start
CMD [ "python", "run.py" ]