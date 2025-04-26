FROM docker:dind-rootless

USER root
RUN apk add --no-cache python3 py3-pip


WORKDIR /app
COPY . .
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "main.py"]
