from usermanagement.models import Offer
from usermanagement.generics import ListView, DetailView, UpdateView, DeleteView, CreateView


class OfferListView(ListView):
    model=Offer
    template_name='enterpriseuserviews/offer_list.html'
