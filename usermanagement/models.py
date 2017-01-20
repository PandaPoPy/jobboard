from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager, User
from django.contrib.contenttypes.models import ContentType

from polymorphic.manager import PolymorphicManager


OFFER_TYPES = (
    ('cdi','CDI'),
    ('cdd', 'CDD'),
    ('interim', 'Interim'),
    ('freelance', 'Freelance'),
    ('internship', 'Internship'),
)


OFFER_STATUSES= (
    ('draft','Draft'),
    ('published', 'Published'),
    ('closed', 'Closed'),
)


APPLIANCE_STATUSES=(
    ('pending','Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)


# class PolyUserManager(PolymorphicManager, UserManager):
#     pass
#
#
# class User(PolymorphicManager, AbstractUser):
#     objects = PolyUserManager()
#
#     @property
#     def type(self):
#         ctype = ContentType.objects.get_for_id(self.polymorphic_ctype_id)
#         return ctype.model


class CandidateUser(User):
    file = models.FileField(upload_to='candidate_cv', verbose_name=_('CV File'))
    skill = models.CharField(max_length=100, blank=True, verbose_name=_('Candidate Skill'))

    def __str__(self):
        return str(self.user)  # on met str() pour renvoyer une chaîne de caractère et non un Objet

    class Meta:
        verbose_name = _('Candidate User')
        verbose_name_plural = _('Candidate Users')


class EnterpriseUser(User):
    enterprise = models.ForeignKey('Enterprise')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = _('Enterprise User')
        verbose_name_plural = _('Enterprise Users')


class Enterprise(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name=_('Name'))
    logo = models.ImageField(upload_to='enterprise_logo', blank=True, verbose_name=_('Logo'))
    #address = models.CharField(max_length=500)
    #postcode = models.CharField(max_length=10)
    #city = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('enterprise_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _('Enterprise')
        verbose_name_plural = _('Enterprises')


class Offer(models.Model):
    enterprise = models.ForeignKey(Enterprise, verbose_name=_('Enterprise'))
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(max_length=250, unique=True, verbose_name=_('Slug'))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    duration = models.DurationField(null=True, blank=True, verbose_name=_('Duration'))
    type = models.CharField(max_length=100, choices=OFFER_TYPES, verbose_name=_('Type'))
    description = models.TextField(blank=True, verbose_name='Description')
    city = models.CharField(max_length=250, verbose_name=_('City'))
    postcode = models.CharField(max_length=10, verbose_name=_('Postcode'))
    status = models.CharField(max_length=100, choices=OFFER_STATUSES, verbose_name=_('Status'))
    skill = models.CharField(max_length=100, blank=True, verbose_name=_('Researched Skill'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('offer_detail', kwargs={'slug': self.slug})

    #  to create automatically the slug when an object is created
    def save(self, *args, **kwargs):  # à voir ne fonctionne pas en shell
        if not self.slug:
            self.slug = slugify(self.title)
        super(Offer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Offer')
        verbose_name_plural = _('Offers')


class Appliance(models.Model):
    candidate_user = models.ForeignKey(CandidateUser, verbose_name=_('Candidate User'))
    offer = models.ForeignKey(Offer, verbose_name=_('Offer'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Appliance Date'))
    status = models.CharField(max_length=100, choices=APPLIANCE_STATUSES, verbose_name=_('Status'))
    motivational_text = models.TextField(blank=True, verbose_name='Motivationnal Text')

    def __str__(self):
        return "Candidature du Candidat : {} sur l'Offre : {}".format(self.candidate_user, self.offer)

    class Meta:
        verbose_name = _('Appliance')
        verbose_name_plural = _('Appliances')
