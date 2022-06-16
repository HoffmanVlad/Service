from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .api.permissions import IsOwnerOrReadOnly
from .api.resource import ProductSerializer
from .api.serializers import SnippetSerializer
from .models import Product, CustomUser, Custom, Auto
from .forms import NewProductForm, EditProductForm, CustomUserForm, UserCompanyForm, EditUsersForm, UserAutoForm
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import generics


class LoginingView(LoginView):
    success_url = reverse_lazy('product_list_page')
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        # self.request.session['last_request'] = str(timezone.now())
        return super().form_valid(form=form)
    
@classmethod
class ProductListView(ListView ,PermissionRequiredMixin):
    model = Product
    template_name = 'products_list.html'
    queryset = Product.objects.all()

class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product
    

class ProfileUser(LoginRequiredMixin,ListView):
    template_name = 'profile.html'
    queryset = CustomUser.objects.all()

class ProfileUserCompany(LoginRequiredMixin,ListView):
    template_name = 'users_list.html'
    model = Custom

class AutoCompany(LoginRequiredMixin,ListView):
    template_name = 'auto.html'
    model = Auto
    
class NewProductView(LoginRequiredMixin,CreateView):
    template_name = 'product_form.html'
    model = Product
    form_class = NewProductForm
    success_url = reverse_lazy('product_list_page')


class NewUserView(LoginRequiredMixin,CreateView):
    template_name = 'productuser.html'
    model = Custom
    form_class = UserCompanyForm
    success_url = reverse_lazy('newuser')   

    def get_absolute_url(self):
        return reverse("newuser", kwargs={"id": self.id})

class NewAutoView(LoginRequiredMixin,CreateView):
    template_name = 'auto_form.html'
    model = Auto
    form_class = UserAutoForm
    success_url = reverse_lazy('newautoview')   


class EditProductView(LoginRequiredMixin,UpdateView):
    template_name = 'product_form.html'
    model = Product
    form_class = EditProductForm
    success_url = reverse_lazy('product_list_page')

class ProfileUserEdit(LoginRequiredMixin,UpdateView):
    template_name = 'product_form.html'
    model = Custom
    form_class = EditUsersForm
    success_url = reverse_lazy('newuser')

    def get_absolute_url(self):
        return reverse("newuser", kwargs={"id": self.id})


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    success_url = '/login/'
    template_name = 'register_page.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(self.object.password)
        self.object.save()
        return super().form_valid(form)


class Logout(LogoutView):
    next_page = '/'


class ProductViewSet_Api(APIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    @classmethod
    def get_extra_actions(cls):
        return []


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        Prod = Product.objects.all()
        serializer = SnippetSerializer(Prod, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        Prod = Product.objects.get(pk=pk)
    except Prod.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(Prod)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(Prod, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        Prod.delete()
        return HttpResponse(status=204)

class SnippetList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
