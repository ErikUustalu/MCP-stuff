FROM python:3.12-slim
WORKDIR /app
RUN pip install fastmcp requests paramiko
COPY server.py .
EXPOSE 8121
CMD ["python", "server.py"]