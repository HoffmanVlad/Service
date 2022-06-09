from rest_framework import routers

from products.views import ProductViewSet_Api

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet_Api)
urlpatterns = router.urls
