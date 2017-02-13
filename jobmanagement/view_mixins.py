from django.contrib.auth.decorators import login_required, permission_required


class LoginRequiredMixin:

    @classmethod  # car on surcharge une méthode de Classe et donc on a en arguments notamment la Classe cls
    def as_view(cls, *args, **kwargs):
        return login_required(super(LoginRequiredMixin, cls).as_view(*args, **kwargs))  # le super() permet de faire appel à la Classe Mère


class PermissionMixin():

    @classmethod  #  car on surcharge une méthode de Classe et donc on a en arguments notamment la Classe cls
    def as_view(cls, *args, **kwargs):
        if hasattr(cls, 'permission_prefix') and cls.permission_prefix is not None :
            permission_name='{}.{}_{}'.format(cls.model._meta.app_label, cls.permission_prefix, cls.model.__name__.lower())
            return permission_required(permission_name)\
                (super(PermissionMixin, cls).as_view(*args, **kwargs)) # c'est un générateur de décorateur et ici le super() n'a pas besoin du SELF car déjà passé automatiquement et permet de faire appel à l'as_view() parent
        else:
            return login_required(super(PermissionMixin, cls).as_view(*args, **kwargs))  # cela permet d'avoir un cas de figure qui countcircuite l'ajout de permission

    def get_queryset(self):  # self fait référence ici à une View
        if not hasattr(self.model.objects, 'get_request_queryset'):  # get_request_queryset est une méthode du Manager et donc faire appel au Manager self.model.objects
            return  self.model.objects.all()
        return self.model.objects.get_request_queryset(self.request)