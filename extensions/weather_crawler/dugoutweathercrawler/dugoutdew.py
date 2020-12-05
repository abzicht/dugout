from meteocalc import Temp, dew_point
import logging

def dewpoint(temperature, humidity):
    if temperature <= 0:
        return -1
    t = Temp(temperature , 'c')
    dp = dew_point(temperature=t, humidity=humidity)
    logging.debug('Computing dew point for temperature {} and humidity {}: {}'.format(temperature, humidity, dp.c))
    return dp.c
