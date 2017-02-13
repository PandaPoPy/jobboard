from django.conf.urls import url

from .views import OfferListView, EnterpriseListView


urlpatterns = [
    url(r'^$', OfferListView.as_view(), name = 'offer_list'),  # notre page publique par défaut
    url(r'^enterprise/$', EnterpriseListView.as_view(), name = 'enterprise_list'),
]