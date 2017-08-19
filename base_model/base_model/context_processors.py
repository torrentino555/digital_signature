from .models import Person

class PersonMiddleware():
def process_request(self, request):
    def person(self, request):
        context = {}
        if hasattr(request, 'user') and request.user.is_authenticated:
            context['person'] = Person.objects.get(user=request.user)
        return context
