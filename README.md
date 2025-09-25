# Nascar-Live-Dashboard

Displays a live Race Dashboard from the Nascar live feed.  Requires docker.

QUICK RUN:
``` sudo docker run -it --name webdash -p8448:8448 vmi1994/webdash:latest ```

MANUAL INSTALL:
``` git clone https://github.com/VMI1994/Nascar-Live-Dashboard.git ```

``` cd Nascar-Live-Dashboard ```

``` sudo docker build -t webdash . ```

Run:
``` sudo docker run -it --name webdash -p8448:8448 webdash ```

The dashboard can be found at http://localhost:8448

![1](https://github.com/VMI1994/Nascar-Live-Dashboard/blob/main/1.jpg)
