""" Read DHT22 sensors """
import os
from pathlib import Path
from influxdb_wrapper import influxdb_factory
from log_mgr import Logger
from config_yml import Config


class Sensors():
    """Read inputs from DHT22 sensors (temperature & humidity) and write it to influx database"""

    def __init__(self, template_config_path: str = None, dry_run: bool = False):
        self.logger = Logger(self.get_class_name(), 'sensors')

        if dry_run:
            dry_run_abs_path = ""
        else:
            dry_run_abs_path = None

        if not template_config_path:
            template_config_path = os.path.join(Path(__file__).parent.resolve(), './config-template.yml')

        self.config = Config(package_name=self.get_class_name(),
                             template_path=template_config_path,
                             config_file_name="config.yml",
                             dry_run=True,
                             dry_run_abs_path=dry_run_abs_path)

        influx_conn_type = self.config['influxdbconn'].get('type', 'influx')
        self.conn = influxdb_factory(influx_conn_type)
        self.conn.open_conn(self.config['influxdbconn'])

    @classmethod
    def get_class_name(cls):
        """ Class name """
        return "sensors"

    def sensor_read(self):
        """
        Read sensors information
        """
        have_readings = False

        try:
            import adafruit_dht  # pylint: disable=import-outside-toplevel

            dht_sensor = adafruit_dht.DHT22(self.config["pin"])
            humidity = dht_sensor.humidity
            temp_c = dht_sensor.temperature
            have_readings = True
        except (ModuleNotFoundError, NameError):
            self.logger.warning("No adafruit supported: returning default values.")
            humidity = 50
            temp_c = 25
            have_readings = True
        except RuntimeError as ex:
            self.logger.error(f"Error reading sensor DHT22: {ex}")

        if have_readings:
            try:
                points = [
                    {
                        "tags": {"sensorid": self.config["id"]},
                        "fields": {"temp": float(temp_c), "humidity": float(humidity)},
                    }
                ]
                self.conn.insert("DHT22", points)

                self.logger.info(f"Temp: {temp_c} | Humid: {humidity}")

            except RuntimeError as ex:
                self.logger.error(f"RuntimeError: {ex}")
                self.logger.error(f"influxDB conn={self.config['influxdbconn']}")


if __name__ == "__main__":
    sensors_instance = Sensors()
    sensors_instance.sensor_read()
