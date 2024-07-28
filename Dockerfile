FROM python:3.12-slim
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
CMD python app.py