FROM alpine
ENV WORK=/dugout-crawler
RUN mkdir $WORK && cd $WORK
WORKDIR $WORK

RUN apk update && apk upgrade && apk add --no-cache python3 openssh python3-dev py3-pip
RUN pip3 install --upgrade pip

COPY ./id_rsa $WORK/id_rsa
RUN mkdir ~/.ssh && echo -e "Host $SSHSERVER\n\tStrictHostKeyChecking=no\n\tUser $SSHUSER\n\tIdentityFile $WORK/id_rsa\n" >> ~/.ssh/config

COPY . $WORK/
RUN python3 setup.py install

ENTRYPOINT ["./entrypoint.sh"]
