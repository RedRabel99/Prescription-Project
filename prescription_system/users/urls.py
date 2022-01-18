from rest_framework.routers import DefaultRouter
from users import views

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet)
router.register(r'pharmacists', views.PharmacistViewSet)
router.register(r'patient', views.PatientViewSet)
