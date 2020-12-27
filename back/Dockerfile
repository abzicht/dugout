FROM alpine

RUN apk update && apk upgrade && apk add --no-cache npm

RUN npm install elasticdump -g

RUN mkdir /dugout-backup
RUN mkdir /dugout-backup/data
WORKDIR /dugout-backup
COPY backup.sh /dugout-backup/backup.sh
#COPY scheduler.txt /dugout-backup/scheduler.txt
#RUN echo SHELL=/bin/sh\n* * * * * /dugout-backup/backup.sh\n > /dugout-backup/scheduler.txt
#RUN echo "SHELL=/bin/sh\n* * * * 0 /dugout-backup/backup.sh\n" > /dugout-backup/scheduler.txt

ENTRYPOINT crontab /dugout-backup/scheduler.txt && crond -f
#ENTRYPOINT /dugout-backup/backup.sh
