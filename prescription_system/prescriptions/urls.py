from rest_framework.routers import DefaultRouter
from prescriptions import views

router = DefaultRouter()
router.register(r'prescriptions', views.PrescriptionViewSet)