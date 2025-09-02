# Nascar-Live-Dashboard

Displays a live Race Dashboard from the Nascar live feed.  Requires docker.

``` git clone https://github.com/VMI1994/Nascar-Live-Dashboard.git ```

``` cd Nascar-Live-Dashboard ```


On Linux:
``` sudo docker build -t webdash . ```

On Mac:
``` sudo docker buildx build -t webdash . ```

Run:
``` sudo docker run -it --rm --name webdash webdash ```

The dashboard can be found at http://localhost:8448

![1](https://github.com/VMI1994/Nascar-Live-Dashboard/blob/main/1.jpg)
