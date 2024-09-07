
FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY . .

# Expose port 80
EXPOSE 80


CMD ["fastapi", "run", "app.py", "--port", "80"]