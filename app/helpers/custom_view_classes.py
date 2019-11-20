from rest_framework import mixins
from rest_framework.generics import GenericAPIView


# not used anymore. just use an existing API view and add the required mixin to add functionality
class CreateOrDestroyView(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericAPIView):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

