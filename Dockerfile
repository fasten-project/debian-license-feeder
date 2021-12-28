FROM ubuntu:focal-20201106
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip python-dev libpq-dev git curl npm nodejs
RUN npm install -g newman
RUN git clone https://github.com/fasten-project/debian-license-feeder.git
WORKDIR "/debian-license-feeder"
RUN chmod +x entrypoint.sh
RUN make
EXPOSE 3251
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
