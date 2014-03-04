
from django.db import models

import apps.control as control_constants


class Room(models.Model):
    name = models.CharField(
        max_length=30,
        default='',
        blank=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'Rooms'


class Device(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=30,
        default='',
        blank=False,
    )
    name = models.CharField(
        max_length=30,
        default='',
        blank=False,
    )
    room = models.ForeignKey(Room)
    type = models.PositiveSmallIntegerField(
        choices=control_constants.DEVICE_CHOICES,
    )
    icon = models.CharField(
        max_length=100,
        default='',
    )
    response_format = models.CharField(
        max_length=50,
        default='',
    )
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'Devices'


class DeviceStatus(models.Model):
    device = models.ForeignKey(Device)
    name = models.CharField(
        max_length=30,
        default='',
        blank=False,
    )
    code = models.CharField(
        max_length=30,
        default='',
        blank=False,
    )
    value = models.CharField(
        max_length=30,
        default='',
        blank=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'DeviceStatus'


class DeviceOperation(models.Model):
    device = models.ForeignKey(Device)
    name = models.CharField(
        max_length=30,
        default='',
        blank=False,
    )
    command = models.CharField(
        max_length=100,
        default='',
        blank=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'DeviceOperations'


class OperationLog(models.Model):
    device = models.ForeignKey(Device)
    operation = models.ForeignKey(DeviceOperation)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.operation.name

    class Meta:
        db_table = 'OperationLogs'


class StatusLog(models.Model):
    device = models.ForeignKey(Device)
    operation = models.ForeignKey(DeviceOperation)
    operation_log = models.ForeignKey(OperationLog)
    status = models.ForeignKey(DeviceStatus)
    value = models.CharField(
        max_length=30,
        default='',
        blank=False,
    )
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.status.name

    class Meta:
        db_table = 'StatusLogs'
