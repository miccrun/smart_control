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
    id="A1",
    name="Air Conditioner",
    type=1,
    room=living_room,
)
ac1.save()
ac1_running_status = DeviceStatus(
    device=ac1,
    name="Running",
    codename="run",
    value="off",
)
ac1_running_status.save()
ac1_on_operation = DeviceOperation(
    device=ac1,
    name="Turn On",
    codename="on",
    command="http://192.168.42.1:8080/a.json",
)
ac1_on_operation.save()
ac1_off_operation = DeviceOperation(
    device=ac1,
    name="Turn Off",
    codename="off",
    command="http://192.168.42.1:8080/b.json",
)
ac1_off_operation.save()
ac1_check_operation = DeviceOperation(
    device=ac1,
    name="Check Status",
    codename="status",
    command="",
)
ac1_check_operation.save()

bed_light = Device(
    id="L1",
    name="Bed Room Light",
    type=1,
    room=bed_room,
)
bed_light.save()
bed_light_running_status = DeviceStatus(
    device=bed_light,
    name="Running",
    codename="run",
    value="off",
)
bed_light_running_status.save()
bed_light_on_operation = DeviceOperation(
    device=bed_light,
    name="Turn On",
    codename="on",
    command="",
)
bed_light_on_operation.save()
bed_light_off_operation = DeviceOperation(
    device=bed_light,
    name="Turn Off",
    codename="off",
    command="",
)
bed_light_off_operation.save()
bed_light_check_operation = DeviceOperation(
    device=bed_light,
    name="Check Status",
    codename="status",
    command="",
)
bed_light_check_operation.save()


temp_sensor1 = Device(
    id="S1",
    name="Living Room Temperature Sensor",
    type=2,
    room=living_room,
)
temp_sensor1.save()
temp_sensor1_temperature_status = DeviceStatus(
    device=temp_sensor1,
    name="Temperature",
    codename="temperature",
    value="75",
)
temp_sensor1_temperature_status.save()
temp_sensor1_humidity_status = DeviceStatus(
    device=temp_sensor1,
    name="Humidity",
    codename="humidity",
    value="35",
)
temp_sensor1_humidity_status.save()
temp_sensor1_check_operation = DeviceOperation(
    device=temp_sensor1,
    name="Check Status",
    codename="status",
    command="http://192.168.42.1:8080/c.json",
)
temp_sensor1_check_operation.save()
