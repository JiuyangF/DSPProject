from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)

class DemandForm(forms.Form):
    GENDER_CHOICES = (
        ("1", 1),
        ("0", 0),
    )
    department = forms.CharField(max_length=50)
    priority = forms.CharField()
    channel_name = forms.CharField()
    data_type = forms.CharField()
    is_app = forms.ChoiceField(widget=forms.RadioSelect,choices=GENDER_CHOICES)
    start_url = forms.URLField()
    rate = forms.CharField()
    dem_com = forms.CharField()
    de_data = forms.CharField()
