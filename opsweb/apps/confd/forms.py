from django import forms
from confd.models import ProjectConfd, VhostsConfd


class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectConfd
        fields = "__all__"


class VhostForm(forms.ModelForm):
    class Meta:
        model = VhostsConfd
        fields = ['project_name','vhosts_key','vhosts_value']