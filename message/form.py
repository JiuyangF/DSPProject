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
    rate = forms.FloatField()
    dem_com = forms.CharField()
    de_data = forms.CharField()
    proposer = forms.CharField()
    # forms.formset_factory()
    # de_data = forms.CharField()

class DemandSelect(forms.Form):
    create_time = forms.DateField()
    channel_name = forms.CharField()

class SuperDemand(forms.Form):
    GENDER_CHOICES = (
        (1, "是"),
        (0, "否"),
    )
    department = forms.CharField(max_length=50,label='部门名称')
    priority = forms.CharField(label='优先级')
    channel_name = forms.CharField(label='渠道名称')
    data_type = forms.CharField(label='数据类型')
    is_app = forms.ChoiceField(widget=forms.RadioSelect,choices=GENDER_CHOICES,label='是否为APP')
    start_url = forms.URLField(label='起始URL')
    rate = forms.FloatField(label='采集频率')
    dem_com = forms.CharField(label='备注')
    de_data = forms.CharField(label='需求字段')
    proposer = forms.CharField(label='提交人')