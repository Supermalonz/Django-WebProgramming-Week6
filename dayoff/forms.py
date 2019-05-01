from django import forms
from django.core.exceptions import ValidationError

from dayoff.models import Dayoff

import datetime


class DayOffForm(forms.ModelForm):
    class Meta:
        model = Dayoff
        exclude = ['approve_status', 'create_by']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'class': 'form-control'}),
        }

    error = None

    def clean(self):
        data = super().clean()

        start = data.get('date_start')
        end = data.get('date_end')

        try:
            if start > end:
                self.error = 'วันที่จบไม่สามารถมาก่อนวันที่เริ่มได้'
                raise ValidationError('วันที่จบไม่สามารถมาก่อนวันที่เริ่มได้')
            elif start < datetime.datetime.now().date():
                self.error = 'คุณกรอกวันที่ในอดีค'
                raise ValidationError('คุณกรอกวันที่ในอดีค')
        except:
            raise ValidationError('คุณกรอกวันที่ผิด')
