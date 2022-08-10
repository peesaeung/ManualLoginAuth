from django import forms


class HNArray(forms.Form):
    HN = forms.CharField(label='HN', required=True, widget=forms.TextInput(attrs={'id': 'hn', 'placeholder': 'HN'}))


class HNTextField(forms.Form):
    HN = forms.CharField(
        label='HN', required=True,
        widget=forms.Textarea(
            attrs={'id':'hnbox', 'placeholder': 'Up to 10 HNs, separated by space bar', 'cols':'30', 'rows': '5'}
        )
    )


class PatientData(HNArray):
    # register = forms.BooleanField(
    #     label='Register', required=False,
    #     widget=forms.CheckboxInput(attrs={'id': 'regis', 'value': 'register', 'checked': 'True'})
    birthDate = forms.DateField(
        label='Date of Birth', required=False, widget=forms.DateInput(attrs={'id': 'birthdate', 'type': 'date'})
    )
    gender = forms.ChoiceField(
        label='Gender', required=False, choices=[(True, 'Male'), (False, 'Female')],
        widget=forms.Select(attrs={'id': 'gender'})
    )
    name = forms.CharField(
        label='Full Name', required=False,
        widget=forms.TextInput(attrs={'id': 'name', 'placeholder': 'Firstname Surname'})
    )


class SecretData(HNArray):
    title = forms.ChoiceField(
        label='Title', required=False, choices=[('', ''), ('Mr', 'Mr.'), ('Ms', 'Ms.'), ('Mrs', 'Mrs.')],
        widget=forms.Select(attrs={'id': 'title'})
    )
    firstname = forms.CharField(
        label='First Name', required=True,
        widget=forms.TextInput(attrs={'id': 'firstname', 'placeholder': 'Firstname'})
    )
    middlename = forms.CharField(
        label='Middle Name', required=False,
        widget=forms.TextInput(attrs={'id': 'middlename', 'placeholder': 'Middlename'})
    )
    lastname = forms.CharField(
        label='Last Name', required=True,
        widget=forms.TextInput(attrs={'id': 'Lastname', 'placeholder': 'Lastname'})
    )


class VisitData(HNArray):
    TXN = forms.CharField(label='TXN', required=True, widget=forms.TextInput(attrs={'id': 'txn', 'placeholder': 'TXN'}))
    type = forms.ChoiceField(
        label='Type', required=True, choices=[(True, 'IPD'), (False, 'OPD')], widget=forms.Select(attrs={'id': 'type'}))
    visittime = forms.DateTimeField(
        label='Visit Datetime', required=True,
        widget=forms.DateTimeInput(attrs={'id': 'visittime', 'type': 'datetime'})
    )
