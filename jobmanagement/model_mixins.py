from django.shortcuts import reverse


class GetAbsoluteMixin:

    def get_absolute_url(self):
        return reverse('jobmanagement:{}_detail'.format(self.__class__.__name__.lower()), kwargs={'slug': self.slug})
