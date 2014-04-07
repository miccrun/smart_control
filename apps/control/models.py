
import json
import re
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
    format = models.CharField(
        max_length=200,
        default='',
    )
    icon = models.CharField(
        max_length=100,
        default='',
    )
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def operate(self, operation_codename):
        try:
            operation = DeviceOperation.objects.get(
                device=self,
                codename=operation_codename,
            )
        except DeviceOperation.DoesNotExist:
            return (False, "Device operation does not exist")

        operation_log = OperationLog(
            device=self,
            operation=operation,
            source=control_constants.LOCAL,
        )
        operation_log.save()

        try:
            urllib2.urlopen(operation.command).read()
        except urllib2.HTTPError, e:
            return (False, 'HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            return (False, 'URLError = ' + str(e.reason))

        return (True, "OK")

    def save_operation_log(self, operation_log_id, data):
        try:
            json_data = json.loads(data)
        except ValueError:
            return (False, "JSON Decoding Error, bad response format")

        if operation_log_id == 0:
            try:
                operation = DeviceOperation.objects.get(
                    device=self,
                    codename=json_data.get("operation", "")
                )
            except DeviceOperation.DoesNotExist:
                return (False, "Device operation does not exist")

            operation_log = OperationLog(
                device=self,
                operation=operation,
                source=control_constants.REMOTE,
                success=json_data.get("result", 1),
                trial=json_data.get("trial", 0),
                rtt=json_data.get("rtt", 0),
            )
            operation_log.save()
        else:
            try:
                operation_log = OperationLog.objects.get(pk=operation_log_id)
            except OperationLog.DoesNotExist:
                return (False, "Operation log does not exist")

            operation_log.success = json_data.get("result", 1)
            operation_log.trial = json_data.get("trial", 0)
            operation_log.rtt = json_data.get("rtt", 0)
            operation_log.save()

        return self.save_status_log(json_data.get("message", ""))

    def save_status_log(self, data):
        group = re.match(self.format, data)
        if group:
            for status, value in group.groupdict().iteritems():
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
                        status=device_status,
                        value=value,
                    )
                    status_log.save()
        else:
            return (False, "Bad response format")

        return (True, "OK")

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
    success = models.PositiveSmallIntegerField(
        choices=control_constants.OPERATION_RESULT,
        default=control_constants.OPERATION_FAIL,
    )
    trial = models.PositiveSmallIntegerField(default=0)
    rtt = models.PositiveSmallIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.operation.name

    class Meta:
        db_table = 'OperationLogs'


class StatusLog(models.Model):
    device = models.ForeignKey(Device)
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


class Config(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=30,
        default='',
        blank=False,
    )
    value = models.CharField(
        max_length=100,
        default='',
        blank=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id

    class Meta:
        db_table = 'Config'
