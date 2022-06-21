# User the python 3.9.13 image on DockerHub
FROM python:3.9.13

# cd to /usr/src/app
WORKDIR /usr/src/app

# No explination needed:
COPY requirements.txt ./

# No explination needed:
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code from the current dir to the WORKDIR:
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]