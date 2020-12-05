#!/bin/sh

tmpback=/tmp/index_backup.json
persistentback=/dugout-backup/data/index_backup.json
elasticdump \
  --input=$esurl/$esindex \
  --output=$tmpback \
  --type=data \
  --httpAuthFile=/dugout-backup/auth.ini

mv $tmpback $persistentback
