from pyowm import OWM
try:
    from dugoutdew import dewpoint
except ImportError:
    from dugoutweathercrawler.dugoutdew import dewpoint

class DugoutOWM():

    def __init__(self, api_key, location):
        self.api_key = api_key
        self.location = location
        self.owm = OWM(self.api_key)

    def sensitive_retriever(self, dict_, *kwargs, default=0):
        try:
            if len(kwargs) == 1:
                return dict_[kwargs[0]]
            else:
                key = kwargs[0]
                kwargs = kwargs[1:]
                return self.sensitive_retriever(dict_[key], *kwargs, default=default)
        except:
            return default

    def pull(self):
        mgr = self.owm.weather_manager()
        observation = mgr.weather_at_place(self.location)
        w = observation.weather
        temperature = float(self.sensitive_retriever(w.temperature(), 'temp',
            default=172.15)) - 272.15 # KELVIN!
        return {
    'timestamp': observation.reception_time('date').strftime('%Y-%m-%dT%H:%M:%SZ'),
    'temperature': temperature,
    'felt_temperature': self.sensitive_retriever(w.temperature(), 'feels_like', default=172.15) - 272.15, # KELVIN!
    'humidity': w.humidity,
    'dewpoint': dewpoint(temperature, w.humidity),
    'clouds': w.clouds,
    'pressure': self.sensitive_retriever(w.pressure, 'press', -1),
    'detailed_status': w.detailed_status,
    'status': w.status,
    'sunrise': w.sunrise_time('date').strftime('%H-%M-%S'),
    'sunset': w.sunset_time('date').strftime('%H-%M-%S'),
    'visibility': w.visibility_distance,
    'weather_code': w.weather_code,
    'wind_speed': self.sensitive_retriever(w.wind('km_hour'),'speed', default=-1),
    'wind_degree': self.sensitive_retriever(w.wind(),'deg', default=-1)
        }
