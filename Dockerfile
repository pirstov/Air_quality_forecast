FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=8080
ENV FLASK_ENV=production

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
