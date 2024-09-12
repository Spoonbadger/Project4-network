FROM python:3
COPY . /Users/craigmorley/Downloads/project4-4
WORKDIR /Users/craigmorley/Downloads/project4-4
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]