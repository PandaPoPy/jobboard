from django.conf.urls import url

from .views import HomeView, EnterpriseListView, OfferDetailView, EnterpriseUserCreateView, CandidateUserCreateView, OfferCreateView, ApplianceView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name = 'home'),  # notre page publique par défaut
    url(r'^offer/(?P<slug>[-\w]+)$', OfferDetailView.as_view(), name='offer_detail'),
    url(r'^enterprise/$', EnterpriseListView.as_view(), name = 'enterprise_list'),
    url(r'^register/$', CandidateUserCreateView.as_view(), name='register'),
    url(r'^recruiter/register/$', EnterpriseUserCreateView.as_view(), name='register_recruiter'),
    url(r'^recruiter/offer/create/$', OfferCreateView.as_view(), name='offer_create_recruiter'),
    url(r'^offer/appliance/(?P<slug>[-\w]+)$', ApplianceView.as_view(), name='appliance'),
]