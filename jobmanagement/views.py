from django.shortcuts import render

from jobmanagement.models import Offer, Enterprise
from jobmanagement.generics import ListView, DetailView, UpdateView, DeleteView, CreateView


class OfferListView(ListView):
    model=Offer
    template_name='candidateuserviews/offer_list.html'


class EnterpriseListView(ListView):
    model=Enterprise
    template_name='candidateuserviews/offer_list.html'
