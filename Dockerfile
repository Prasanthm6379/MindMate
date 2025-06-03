FROM python:3.12

WORKDIR /code

RUN apt update -y && apt-get install -y libgl1-mesa-glx

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]