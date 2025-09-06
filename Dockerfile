FROM python
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-full python3-pip
RUN pip install --upgrade pip
RUN pip install flask requests
RUN mkdir templates
COPY . .
RUN cp index.html ./templates/
CMD ["bash", "start.sh"]
