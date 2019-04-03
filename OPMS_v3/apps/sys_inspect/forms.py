from django import forms

######################################
# 修改设备表单
######################################
class EditDevForm(forms.Form):
    dev_name =forms.CharField(max_length=255, required=False)
    install_position=forms.CharField(max_length=255, required=False)
    # comment =forms.CharField(max_length=1000, required=False)


######################################
# 添加设备表单
######################################
class AddDevForm(forms.Form):
    dev_id =forms.CharField(max_length=255,required=True)
    dev_name = forms.CharField(max_length=255, required=True)
    install_position = forms.CharField(max_length=255, required=False)
    comment = forms.CharField(max_length=1000, required=False)
