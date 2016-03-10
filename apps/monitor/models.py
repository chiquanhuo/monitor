#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from django.db import models
from django import forms


class Monitor(models.Model):
    class Meta:
        db_table = "debug_monitor_ad"

    connection_name = 'youmi_admin'

    id = models.AutoField(primary_key=True)
    product = models.IntegerField()
    params = models.CharField(max_length=200, default='')
    create_at = models.DateTimeField()


class MonitorForm(forms.Form):
    product = forms.IntegerField(initial=2)
    aid = forms.CharField(initial='')
    ei = forms.CharField(initial='')
    ifa = forms.CharField(initial='')
