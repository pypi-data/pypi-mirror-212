from django import forms
from django.core.exceptions import ValidationError

from huscy.project_consents.forms import TokenForm
from huscy.project_consents.views import CreateTokenView
from mpi_cbs.huscy.subjects_wrapper.models import WrappedSubject


class WrappedTokenForm(TokenForm):
    subject = forms.CharField()

    def clean_subject(self):
        subject_id = self.cleaned_data['subject']
        try:
            wrapped_subject = WrappedSubject.objects.get(pseudonym=subject_id)
        except WrappedSubject.DoesNotExist:
            raise ValidationError('subject does not exist')
        return wrapped_subject.subject


class WrappedCreateTokenView(CreateTokenView):
    form_class = WrappedTokenForm
