from canteenapp.models import UserProfile
from canteenapp.models import orderDetails, Food_item
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('Name', 'Admn_no', 'Batch')


class CountForm(forms.ModelForm):

    useradno = forms.CharField(max_length=10)
    itemname = forms.CharField(max_length=200, required=False)
    order_date = forms.DateField(required=False)

    class Meta:
        model = orderDetails
        fields = ('count', 'useradno', 'itemname', 'order_date')

    def __init__(self, *args, **kwargs):
        super(CountForm, self).__init__(*args, **kwargs)

        for useradno in self.fields:
            self.fields[useradno].required = False

        for itemid in self.fields:
            self.fields[itemid].required = False

        for order_date in self.fields:
            self.fields[order_date].required = False


class UserUpdateForm(forms.Form):

    useradno = forms.CharField(max_length=10)
    add_credit = forms.IntegerField()
    fields = ('udseradno', 'add_credit')


class add_number(forms.Form):

    number = forms.IntegerField()
    fields = ('number')


class itemUpdateForm(forms.ModelForm):

    pub_date = forms.DateField(required=False)

    class Meta:
        model = Food_item
        fields = ('itemName', 'cost', 'number')