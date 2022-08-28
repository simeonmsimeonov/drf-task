from api.views import OrderViewSet, ProductViewSet, StatsViewSet
from django.urls import path



from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('product', ProductViewSet, basename='product')
router.register('stats', StatsViewSet, basename='stats')

urlpatterns = router.urls