# Dugout

So what on earth is this?

We want to have information. If we dug out a cellar, we want to know its
temperature and humidity to keep above the dew point. We want to monitor
such parameters to increase the storage time of vegetables and prevent mold.

This project and all of its sub-projects constitute a pipeline between raw sensor data
available via Modbus RTU / RS-485 and an Elasticsearch instance.

For accessing sensor data, a Raspberry PI (any SoC would do) is utilized. It
is connected to a
[MAX485 chip](https://www.maximintegrated.com/en/products/interface/transceivers/MAX485.html)
that speaks RS-485. The [pymodbus](https://riptideio.github.io/pymodbus/) is
the ideal solution to this use case. However, we had to [fork
it](https://github.com/abzicht/pymodbus), since
Raspberry PI usage __without a
[shield](https://www.sparkfun.com/products/retired/13706)__ really does not
lay in its focus. What is the problem? Well, to send and receive data via
RS485, you need to enable or disable the transmit and receive drivers respectively.
Of course, this job can be done via GPIO. However, pymodbus did not have the
capability of toggling pins whenever data is to be sent or to be received.
Our fork does exactly that and now we can use a Raspberry Pi and a MAX485 to
speak to RS485 sensors.

The [sensors in question](https://www.banggood.com/Modbus-RS485-Temperature-and-Humidity-Transmitter-Sensor-High-Precision-Monitoring-p-1159961.html?cur_warehouse=CN)
have hilariously bad document. Multiple sources contradict each other,
forcing you to fallback to trial-and-error.

Hear are some observations made while exploring this kind of sensor:

* The register addresses named in most documentation is off by one: if the
  documentation states that temperature data is located in register 0x0001,
  use 0x0000 instead. The same is true for humidity.
* You want to change the device address? Good luck. Most documentation will
  tell you that the device's original address is 0x0001 and that you should
  therefore send the address-change-command to 0x0001. However, this is false.
  Send it to address 0x0000 and beware to only connect one sensor at a time.
  Otherwise, all devices on the line will update their address.

The great thing about these RS485 sensors is that you can use the bus to
connect countless devices that will all be controllable by the Raspberry.

Is your cellar burglarproof? No? How bad would it be, if a burglar had access
to your Elasticsearch instance? Or to your docker network? Bad, right? We want
to keep the Raspberry as dumb as possible. Assuming that our crawler that puts
sensor data of the Raspberry into Elasticsearch is located in a secure
environment, we take the following approach:

The Raspberry runs an ssh server the crawler connects to. On the Raspberry, a
__Dugout-Server__ is running on `127.0.0.1`. The crawler uses port forwarding
to mirror this server to an own port. This way, the Raspberry does not need to
know any secrets and only the crawler is able to retrieve sensor data.

The crawler's job is to periodically pull data and push it to Elasticsearch.

The above explains the operational functionality. Of course, we want to
configure sensors before production. Check out the configurator that, e.g.,
assigns addresses for each sensors.
