FROM python:3-slim
WORKDIR /programas/api-images
RUN pip3 install fastapi
RUN pip3 install pydantic
RUN pip3 install mysql-connector-python
COPY . .
CMD ["fastapi", "run", "./api-imagenes.py", "--port", "8000"]
