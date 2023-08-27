from django import forms
from .models import Profile


class ChangeImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'multiple': False,
                'class': 'edit-image-btn'
            }),
        }


class EditProfileInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                'bio', 'date_of_birth']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
        }