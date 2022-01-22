from rest_framework.routers import DefaultRouter
from drugs import views

router = DefaultRouter()
router.register(r'drugs', views.DrugViewSet, basename='drugs')
