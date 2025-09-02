FROM python
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-full python3-pip
RUN pip install flask requests
COPY . .
COPY ./templates/index.html ./templates/index.html
CMD ["python3", "webdash.py"]
