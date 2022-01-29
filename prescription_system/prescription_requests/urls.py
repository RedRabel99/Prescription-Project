from rest_framework.routers import DefaultRouter
from prescription_requests import views

router = DefaultRouter()
router.register(r'prescription-requests', views.PrescriptionRequestsViewSet)
