# encoding: utf-8

'''
Free as freedom will be 25/9/2016

@author: luisza
'''

from __future__ import unicode_literals
from django import forms
from .models import EmailNotification
from .widgets import EmailLookup
#from ajax_select.fields import AutoCompleteSelectMultipleField


class NotificationForm(forms.ModelForm):
    recipient = EmailLookup('emails')

    class Meta:
        model = EmailNotification
        fields = ("subject", "enqueued", "sended", "problems",
                  "message", "recipient",
                  "file")
