from django.conf.urls import url

from .views import OfferListView


urlpatterns = [
    url(r'^$', OfferListView.as_view(), name = 'home'),
]