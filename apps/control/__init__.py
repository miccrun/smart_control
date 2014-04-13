APPLIANCE = 1
SENSOR = 2
DEVICE_CHOICES = (
    (APPLIANCE, 'Appliance'),
    (SENSOR, 'Sensor'),
)

MODE_ON = "O"
MODE_OFF = "F"
MODE_AUTO = "A"
DEVICE_MODES = (
    (MODE_ON, 'On'),
    (MODE_OFF, 'Off'),
    (MODE_AUTO, 'Auto'),
)

LOCAL = 1
REMOTE = 2
OPERATION_SROUCE = (
    (LOCAL, 'Local'),
    (REMOTE, 'Remote'),
)

ON = "O"
OFF = "F"

True = "1"
False = "0"

OPERATION_FAIL = 0
OPERATION_SUCCESS = 1
OPERATION_RESULT = (
    (OPERATION_FAIL, 'Fail'),
    (OPERATION_SUCCESS, 'Success'),
)

EVENT_TIME = 1
EVENT_TRIGGER = 2
