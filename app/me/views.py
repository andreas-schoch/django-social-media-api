from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
from helpers.permissions import IsOwner
from users.serializer import PrivateUserSerializer


User = get_user_model()


# api/me/
class GetOrUpdateUserData(RetrieveUpdateAPIView):

    serializer_class = PrivateUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsOwner,)  # not really needed as the user is hardcoded to the requesting user

    def get_queryset(self):
        self.kwargs['pk'] = self.request.user.id  # the view expects a lookup field in the url e.g. api/me/<pk>
        return self.queryset

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)
