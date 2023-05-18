# Use the official Python base image
FROM python:3.9-slim-buster

RUN groupadd -g 999 python \
    && useradd -r -u 999 -g python python \
    && mkdir -p /usr/app \
    && python -m venv /usr/app/.venv \
    && chown -R python:python /usr/app 

ENV PATH="/usr/app/.venv/bin:$PATH"
ENV PIP_NO_CACHE_DIR=off
WORKDIR /usr/app
#Todo lo que viene ejecutado despues de WORKDIR /usr/app se ejecuta acá dentro

USER 999
#Se ejecutan las instrucciones de abajo con este USER

COPY --chown=python:python requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code
COPY songs.py songs.py

# Expose the application port
EXPOSE 8080

# Run the Flask application
CMD ["python", "songs.py"]
