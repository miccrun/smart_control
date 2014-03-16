
import json
import urllib2

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
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def operate(self, operation):
        try:
            response = urllib2.urlopen(operation.command).read()
        except urllib2.HTTPError, e:
            return (False, 'HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            return (False, 'URLError = ' + str(e.reason))

        return self.save_log(operation, control_constants.LOCAL, response)

    def save_log(self, operation, source, log):
        operation_log = OperationLog(
            device=self,
            operation=operation,
            source=source,
        )
        operation_log.save()

        try:
            json_data = json.loads(log)
        except ValueError:
            return (False, "JSON Decoding Error, bad response format")

        for status, value in json_data.iteritems():
            try:
                device_status = DeviceStatus.objects.get(
                    device=self,
                    codename=status,
                )
            except DeviceStatus.DoesNotExist:
                continue

            if device_status:
                device_status.value = value
                device_status.save()
                status_log = StatusLog(
                    device=self,
                    operation=operation,
                    operation_log=operation_log,
                    status=device_status,
                    value=value,
                )
                status_log.save()

        return (True, "")

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
    codename = models.CharField(
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
    codename = models.CharField(
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
    source = models.PositiveSmallIntegerField(
        choices=control_constants.OPERATION_SROUCE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

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
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.status.name

    class Meta:
        db_table = 'StatusLogs'
