FROM python:latest AS gitlab-ci

# Install dependencies.
# copy manually requirements.txt from main forge directory or use ./build-image.sh script
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install bandit pycodestyle pylint semgrep
