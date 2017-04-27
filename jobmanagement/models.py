from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager, User
from django.contrib.contenttypes.models import ContentType
from polymorphic.manager import PolymorphicManager
from polymorphic.models import PolymorphicModel

from .model_mixins import GetAbsoluteMixin


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


class PolyUserManager(PolymorphicManager, UserManager):
    pass


class User(PolymorphicModel, AbstractUser):
    objects = PolyUserManager()

    @property
    def type(self):
        ctype = ContentType.objects.get_for_id(self.polymorphic_ctype_id)
        return ctype.model


class CandidateUser(GetAbsoluteMixin, User):
    file = models.FileField(upload_to='candidate_cv', null=True, blank=True, verbose_name=_('CV File'))
    skill = models.CharField(max_length=100, blank=True, verbose_name=_('Candidate Skill'))

    class Meta:
        verbose_name = _('Candidate User')
        verbose_name_plural = _('Candidate Users')


class EnterpriseUser(User):
    enterprise = models.ForeignKey('Enterprise')

    class Meta:
        verbose_name = _('Enterprise User')
        verbose_name_plural = _('Enterprise Users')


class EnterpriseManager(models.Manager):

    def get_by_natural_key(self, slug):
        queryset=self.get(slug=slug)
        return queryset


class Enterprise(GetAbsoluteMixin, models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name=_('Name'))
    logo = models.ImageField(upload_to='enterprise_logo', blank=True, verbose_name=_('Logo'))
    slug = models.SlugField(max_length=250, primary_key=True, verbose_name=_('Slug'))

    def __str__(self):
        return self.name

    #  to create automatically the slug when an object is created
    def save(self, *args, **kwargs):  # à voir ne fonctionne pas en shell
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)  #  en python3 : plus besoin de répéter la classe et le self

    def natural_key(self):
        return [self.slug]

    class Meta:
        verbose_name = _('Enterprise')
        verbose_name_plural = _('Enterprises')
        #permissions = (('view_enterprise', _('Can view an enterprise')),)


class OfferManager(models.Manager):

    def get_by_natural_key(self, slug):
        queryset=self.get(slug=slug)
        return queryset


class Offer(GetAbsoluteMixin, models.Model):
    enterprise = models.ForeignKey(Enterprise, verbose_name=_('Enterprise'))
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(max_length=250, null=True, verbose_name=_('Slug'))
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
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

    def natural_key(self):
        return [self.slug]

    #  to create automatically the slug when an object is created
    def save(self, *args, **kwargs):  # à voir ne fonctionne pas en shell
        if self.id:
            self.slug = slugify('{}_{}'.format(self.id, self.title))
            super().save(*args, **kwargs)  # en python3 : plus besoin de répéter la classe et le self
        else:
            super().save(*args, **kwargs)
            self.slug = slugify('{}_{}'.format(self.id, self.title))
            super().save(*args, **kwargs)

    def get_request_queryset(self, request):
        # import ipdb
        # ipdb.set_trace()
        if request.user.type == 'enterpriseuser':
            queryset = request.user.enterpriseuser.enterprise.offer_set.all()
        elif request.user.type == 'candidateuser':
            queryset = Offer.objects.all()  # TODO: provisoirement
        else:
            queryset = Offer.objects.none()
        return queryset

    class Meta:
        verbose_name = _('Offer')
        verbose_name_plural = _('Offers')
        #permissions = (('view_offer', _('Can view an offer')),)


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
        #permissions = (('view_appliance', _('Can view an appliance')),)
