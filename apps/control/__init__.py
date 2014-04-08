APPLIANCE = 1
SENSOR = 2
DEVICE_CHOICES = (
    (APPLIANCE, 'Appliance'),
    (SENSOR, 'Sensor'),
)

LOCAL = 1
REMOTE = 2
OPERATION_SROUCE = (
    (LOCAL, 'Local'),
    (REMOTE, 'Remote'),
)

OPERATION_FAIL = 0
OPERATION_SUCCESS = 1
OPERATION_RESULT = (
    (OPERATION_FAIL, 'Fail'),
    (OPERATION_SUCCESS, 'Success'),
)

EVENT_TIME = 1
EVENT_TRIGGER = 2

API_PATH = "http://central.micbase.com/central.php"
