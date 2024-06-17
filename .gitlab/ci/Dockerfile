FROM python:latest AS gitlab-ci

# Install dependencies.
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install bandit pycodestyle pylint semgrep
