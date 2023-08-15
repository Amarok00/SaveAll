from django.forms import ModelForm
from .models import Discussions


class DiscussionsCreateForm(ModelForm):

    class Meta:
        model = Discussions
        fields = ('title','content')
