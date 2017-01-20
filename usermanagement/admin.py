from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin

from .models import CandidateUser, EnterpriseUser, Offer, Enterprise, Appliance


admin.site.register(CandidateUser)
admin.site.register(EnterpriseUser)
admin.site.register(Offer)
admin.site.register(Enterprise)
admin.site.register(Appliance)

