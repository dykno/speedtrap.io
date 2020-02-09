FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["EXPORT", "FLASK_APP=py-mongo-api.py"
CMD ["flask", "run", "--host=0.0.0.0"]
