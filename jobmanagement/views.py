from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test

from jobmanagement.models import Offer, Enterprise, EnterpriseUser, CandidateUser, Appliance
from jobmanagement.forms import EnterpriseUserCreationForm, CandidateUserCreationForm


class HomeView(generic.ListView):
    model=Offer
    #template_name='offer_list.html'


class OfferDetailView(generic.DetailView):
    model=Offer
    #template_name='offer_detail.html'


class OfferCreateView(generic.CreateView):
    model = Offer
    fields = ['title', 'start_date', 'duration', 'type', 'description','city', 'postcode', 'status', 'skill']

    def form_valid(self, form):
        offer=form.save(commit=False)
        offer.enterprise = self.request.user.enterprise
        offer.save()
        return super().form_valid(form)

    @classmethod
    def as_view(cls, *args, **kwargs):
        return user_passes_test(lambda u: u.type == 'enterpriseuser')(super().as_view(*args, **kwargs))


class EnterpriseListView(generic.ListView):
    model=Enterprise
    #template_name='enterprise_list.html'


class EnterpriseUserCreateView(generic.CreateView):
    model=EnterpriseUser
    form_class = EnterpriseUserCreationForm
    success_url = reverse_lazy('jobmanagement:home')


class CandidateUserCreateView(generic.CreateView):
    model=CandidateUser
    form_class = CandidateUserCreationForm
    success_url = reverse_lazy('jobmanagement:home')


class ApplianceView(generic.CreateView):
    model = Appliance
    fields = ['motivational_text']

    def get_object(self):
        import ipdb
        ipdb.set_trace()

        object=super().get_object()
        try:
            return object
        except Offer.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['offer'] = self.get_object()
        return context

    def form_valid(self, form):
        appliance=form.save(commit=False)
        appliance.offer = self.get_object()  # le get_object prévu ds le Mixin me récupère directement l'objat Offer
        appliance.candidate_user = self.request.user
        appliance.save()
        return super().form_valid(form)