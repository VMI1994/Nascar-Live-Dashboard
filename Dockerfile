FROM python
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-full python3-pip
RUN pip install --upgrade pip
RUN pip install flask requests
COPY . .
CMD ["python3", "RaceDash.py"]
