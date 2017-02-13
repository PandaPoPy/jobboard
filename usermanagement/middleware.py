from django.conf import settings


class CustomURLMiddleware():
    # attention nouveau code pour Django1.10
    def __init__(self, get_response):
        self.get_reponse=get_response

    # attention nouveau code pour Django1.10
    def __call__(self, request):
        self.process_request(request)  # ici appel à la méthode écrite spécialement ci-dessous
        response=self.get_reponse(request)
        return response

    def process_request(self, request):
        # import ipdb
        # ipdb.set_trace()
        if request.user.is_authenticated():
            if request.user.type != 'user':
                request.urlconf = settings.ROOT_URLCONF.replace('.urls','.{}_urls'.format(request.user.type))
            else:
                request.urlconf = settings.ROOT_URLCONF.replace('.urls','.{}_urls'.format('anonymous'))
        else:
            request.urlconf = settings.ROOT_URLCONF.replace('.urls','.{}_urls'.format('anonymous'))

        print('-'*80)
        print(request.user, getattr(request.user, 'type', '-'))
        print(request)
        print(request.urlconf)
        print('-'*80)
