FROM python:3.7.5-slim
WORKDIR /usr/src/app
COPY . .
RUN python -m pip install -r requirements.txt
CMD ["python", "src/main.py"]
