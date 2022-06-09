from django.urls import path

from .api.resource import CustomAuthToken, LogoutView, ProductsListViewSet
from .views import ProductListView, UserCreateView, LoginingView, Logout, ProductDetailView, NewProductView, \
    ProfileUser, NewUserView, ProductDetailView, EditProductView
from products import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list_page'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', LoginingView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('products/id=<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', NewUserView.as_view(), name='newuserview'),
    path('products/new', NewProductView.as_view(), name='new_product'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    # path('profile/edit/<int:pk>', ProfileUserEdit.as_view(), name='profile_edit'),
    path('products/edit/<int:pk>', EditProductView.as_view(), name='edit_product'),
    path('api/auth', CustomAuthToken.as_view(), name='auth'),
    path('api/logout', LogoutView.as_view(), name='api_logout'),
    path('api/products/<int:pk>/', ProductsListViewSet.as_view({'get': 'list',
                                                                        'post': 'create',
                                                                        'put': 'update',}), name='show_products'),
    path('product/', views.snippet_list),
    path('product/<int:pk>/', views.snippet_detail),
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),

]
