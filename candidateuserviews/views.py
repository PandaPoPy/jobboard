from usermanagement.models import Offer, Enterprise
from usermanagement.generics import ListView, DetailView, UpdateView, DeleteView, CreateView


class OfferListView(ListView):
    model=Offer
    template_name='candidateuserviews/offer_list.html'
