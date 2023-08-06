from django.urls import path

from mpi_cbs.huscy.mpicbs_project_consents.views import WrappedCreateTokenView


urlpatterns = [
    path('create/token/', WrappedCreateTokenView.as_view(), name='wrapped-create-project-consent-token'),
]
