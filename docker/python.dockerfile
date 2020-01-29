FROM python:3.7.0-stretch
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "src/main.py"]
