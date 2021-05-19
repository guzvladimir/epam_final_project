FROM python:3.8.5-alpine
RUN pip install --upgrade pip
COPY . /
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "browser_executor/main.py"]