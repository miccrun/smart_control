from apps.control.models import (
    Room,
    Device,
    DeviceStatus,
    DeviceOperation,
)

# *** Rooms ***
living_room = Room(name="Living Room")
living_room.save()

bed_room = Room(name="Bed Room")
bed_room.save()


# *** Devices ***
ac1 = Device(
    id="AC01",
    name="Air Conditioner",
    type=1,
    format='^(?:\w{5})(?P<run>\w{1})$',
    room=living_room,
)
ac1.save()
ac1_running_status = DeviceStatus(
    device=ac1,
    name="Running",
    codename="run",
    value="F",
)
ac1_running_status.save()
ac1_on_operation = DeviceOperation(
    device=ac1,
    name="Turn On",
    codename="on",
    command="O",
)
ac1_on_operation.save()
ac1_off_operation = DeviceOperation(
    device=ac1,
    name="Turn Off",
    codename="off",
    command="F",
)
ac1_off_operation.save()
ac1_check_operation = DeviceOperation(
    device=ac1,
    name="Check Status",
    codename="status",
    command="S",
)
ac1_check_operation.save()

bed_light = Device(
    id="LT01",
    name="Light",
    type=1,
    format='^(?:\w{5})(?P<run>\w{1})$',
    room=bed_room,
)
bed_light.save()
bed_light_running_status = DeviceStatus(
    device=bed_light,
    name="Running",
    codename="run",
    value="F",
)
bed_light_running_status.save()
bed_light_on_operation = DeviceOperation(
    device=bed_light,
    name="Turn On",
    codename="on",
    command="O",
)
bed_light_on_operation.save()
bed_light_off_operation = DeviceOperation(
    device=bed_light,
    name="Turn Off",
    codename="off",
    command="F",
)
bed_light_off_operation.save()
bed_light_check_operation = DeviceOperation(
    device=bed_light,
    name="Check Status",
    codename="status",
    command="S",
)
bed_light_check_operation.save()


living_light = Device(
    id="LT02",
    name="Light",
    type=1,
    format='^(?:\w{5})(?P<run>\w{1})$',
    room=living_room,
)
living_light.save()
living_light_running_status = DeviceStatus(
    device=living_light,
    name="Running",
    codename="run",
    value="F",
)
living_light_running_status.save()
living_light_on_operation = DeviceOperation(
    device=living_light,
    name="Turn On",
    codename="on",
    command="O",
)
living_light_on_operation.save()
living_light_off_operation = DeviceOperation(
    device=living_light,
    name="Turn Off",
    codename="off",
    command="F",
)
living_light_off_operation.save()
living_light_check_operation = DeviceOperation(
    device=living_light,
    name="Check Status",
    codename="status",
    command="S",
)
living_light_check_operation.save()


living_temp_sensor = Device(
    id="TS01",
    name="Temperature Sensor",
    type=2,
    format='^(?:\w{5})(?P<temperature>\d{2}),(?P<humidity>\d{2})$',
    room=living_room,
)
living_temp_sensor.save()
living_temp_sensor_temperature_status = DeviceStatus(
    device=living_temp_sensor,
    name="Temperature",
    codename="temperature",
    value="20",
)
living_temp_sensor_temperature_status.save()
living_temp_sensor_humidity_status = DeviceStatus(
    device=living_temp_sensor,
    name="Humidity",
    codename="humidity",
    value="35",
)
living_temp_sensor_humidity_status.save()
living_temp_sensor_check_operation = DeviceOperation(
    device=living_temp_sensor,
    name="Check Status",
    codename="status",
    command="S",
)
living_temp_sensor_check_operation.save()


bed_temp_sensor = Device(
    id="TS02",
    name="Temperature Sensor",
    type=2,
    format='^(?:\w{5})(?P<temperature>\d{2}),(?P<humidity>\d{2})$',
    room=bed_room,
)
bed_temp_sensor.save()
bed_temp_sensor_temperature_status = DeviceStatus(
    device=bed_temp_sensor,
    name="Temperature",
    codename="temperature",
    value="20",
)
bed_temp_sensor_temperature_status.save()
bed_temp_sensor_humidity_status = DeviceStatus(
    device=bed_temp_sensor,
    name="Humidity",
    codename="humidity",
    value="35",
)
bed_temp_sensor_humidity_status.save()
bed_temp_sensor_check_operation = DeviceOperation(
    device=bed_temp_sensor,
    name="Check Status",
    codename="status",
    command="S",
)
bed_temp_sensor_check_operation.save()


living_motion_sensor = Device(
    id="MS01",
    name="Motion Sensor",
    type=2,
    format='^(?:\w{5})(?P<present>\w{1})$',
    room=living_room,
)
living_motion_sensor.save()
living_motion_sensor_present_status = DeviceStatus(
    device=living_motion_sensor,
    name="Present",
    codename="temperature",
    value="F",
)


bed_motion_sensor = Device(
    id="MS02",
    name="Motion Sensor",
    type=2,
    format='^(?:\w{5})(?P<present>\w{1})$',
    room=bed_room,
)
bed_motion_sensor.save()
bed_motion_sensor_present_status = DeviceStatus(
    device=bed_motion_sensor,
    name="Present",
    codename="temperature",
    value="F",
)
