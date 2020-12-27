#!/bin/sh

tmpback=/tmp/index_backup.json
persistentbacksensors=/dugout-backup/data/dugout_sensors_backup.json
persistentbackweather=/dugout-backup/data/dugout_weather_backup.json
elasticdump \
  --input=http://elasticsearch:9200/dugout-sensors \
  --output=$tmpback \
  --type=data \
  --httpAuthFile=/dugout-backup/auth.txt

mv $tmpback $persistentbacksensors

# ----

elasticdump \
  --input=http://elasticsearch:9200/dugout-weather \
  --output=$tmpback \
  --type=data \
  --httpAuthFile=/dugout-backup/auth.txt

mv $tmpback $persistentbackweather
