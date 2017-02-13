from django.views import generic

from .view_mixins import PermissionMixin


class ListView(PermissionMixin, generic.ListView):
    permission_prefix = 'view'


class DetailView(PermissionMixin, generic.DetailView):
    permission_prefix = 'view'  # liste et detail, c'est la même permission car si on a la liste, on devrait pouvoir voir les details


class UpdateView(PermissionMixin, generic.UpdateView):
    permission_prefix = 'change'


class DeleteView(PermissionMixin, generic.DeleteView):
    permission_prefix = 'delete'


class CreateView(PermissionMixin, generic.CreateView):
    permission_prefix = 'create'