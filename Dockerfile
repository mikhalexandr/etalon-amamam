FROM python:3.11

WORKDIR /main

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

COPY . /main
WORKDIR /main

EXPOSE 5252

CMD ["python3", "main.py"]
