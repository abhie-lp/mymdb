from .models import Vote, MovieImage
from django import forms


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = "__all__"
        labels = {None}

    def __init__(self, **kwargs):
        super(VoteForm, self).__init__(**kwargs)

        self.fields["user"].widget = forms.HiddenInput()
        self.fields["user"].disabled = True

        self.fields["movie"].widget = forms.HiddenInput()
        self.fields["movie"].disabled = True

        self.fields["value"].label = "Vote"
        self.fields["value"].widget = forms.RadioSelect()
        self.fields["value"].choices = Vote.VALUE_CHOICES


class MovieImageForm(forms.ModelForm):

    class Meta:
        model = MovieImage
        fields = "__all__"
        widgets = {"movie": forms.HiddenInput(),
                   "user": forms.HiddenInput()}

    def __init__(self, **kwargs):
        super(MovieImageForm, self).__init__(**kwargs)
        self.fields["user"].disabled = True
        self.fields["movie"].disabled = True
