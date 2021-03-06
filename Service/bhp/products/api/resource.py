from datetime import timedelta

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import  IsAdminUser, AllowAny
from rest_framework.response import Response

from products.models import Product
from products.api.serializers import ProductSerializerView


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if created:
            token.created += timedelta(minutes=5)
            token.save()
        return Response({'token': token.key})


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        token: Token = request.auth
        token.delete()
        return Response()

class ProductSerializer(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerView
    http_method_names = ['post', ]
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny, )
        return super().get_permissions()

class ProductsListViewSet(ModelViewSet):
    queryset = Product.objects.filter()
    serializer_class = ProductSerializerView
    permission_classes = [IsAdminUser]

    @property
    def get_queryset(self):
        return Product.objects.filter(CustomUser=self.request.CustomUser).all

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = (AllowAny,)
        return super().get_permissions()