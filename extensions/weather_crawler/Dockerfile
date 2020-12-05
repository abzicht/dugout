FROM alpine
ENV WORK=/dugout-weather-crawler
RUN mkdir $WORK && cd $WORK
WORKDIR $WORK

RUN apk update && apk upgrade && apk add --no-cache python3 python3-dev py3-pip build-base
RUN pip3 install --upgrade pip

COPY . $WORK/
RUN python3 setup.py install

ENTRYPOINT ["./entrypoint.sh"]
