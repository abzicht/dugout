FROM alpine

RUN apk update && apk upgrade && apk add --no-cache npm

RUN npm install elasticdump -g

RUN echo "user=$esuser\npassword=$espass" > /dugout-backup/auth.txt

ENTRYPOINT ["./entrypoint.sh"]
