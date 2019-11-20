from annoying.functions import get_object_or_None
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from .serializers import RegistrationSerializer, ValidationCodeSerializer, RegistrationValidationSerializer
from .models import VALIDATION_CODE_LENGTH, ValidationCode, CodeStatus
from helpers.my_mailer import Mailer

User = get_user_model()


class RegistrationView(GenericAPIView):
    permission_classes = []
    serializer_class = RegistrationSerializer

    def post(self, request):
        # create a new User (only email field specified)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save(email=serializer.validated_data['email'])

        # create a new ValidationCode for the user
        new_validation_code = get_random_string(length=VALIDATION_CODE_LENGTH)
        validation_serializer = ValidationCodeSerializer(data=request.data)
        validation_serializer.is_valid(raise_exception=True)
        validation_serializer.save(user=new_user, code=new_validation_code)

        # send the user the validation code via email
        Mailer.send_registration_validation_code(new_user.email, new_validation_code)

        return Response(self.get_serializer(new_user).data)


# api/registration/validation/
class RegistrationValidationView(UpdateAPIView):

    serializer_class = RegistrationValidationSerializer
    permission_classes = []
    queryset = User.objects.all()

    def get_queryset(self):
        # injecting right user id
        new_user = get_object_or_None(ValidationCode, code=self.request.data['code'])
        self.kwargs['pk'] = new_user.user.id
        return self.queryset

    def partial_update(self, request, *args, **kwargs):
        # compare validation code
        code = self.request.data.get('code')  # provided by user in body
        valid_code = get_object_or_None(ValidationCode, code=code)
        if not valid_code:
            raise PermissionError('invalid validation code')

        if valid_code.status == CodeStatus.validated:
            raise PermissionError('already validated')

        # set the status of the ValidationCode instance to validated
        valid_code.status = CodeStatus.validated
        valid_code.save()

        # prepare provided user data and store it
        data = self.request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid()
        return self.update(request, *args, **kwargs)


# class RegistrationValidationView(GenericAPIView):
#     permission_classes = []
#     serializer_class = RegistrationValidationSerializer
#
#
#     def put(self, request):
#         # remove "code" because this serializer doesn't need it
#         code = request.data.pop('code')
#         print(f"COOOOOOODDDEEEE: {code}")
#         print(request.data)
#         serializer = self.get_serializer(data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#
#         # compare stored validation code with the one the user just sent
#         # valid_code = get_object_or_None(ValidationCode, code=code)
#
#         # if not valid_code:
#         #     raise PermissionError('invalid validation code')
#
#         # save new user data if valid
#         user = serializer.save()
#
#         return Response(self.get_serializer(user).data)
