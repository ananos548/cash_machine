from django.urls import path

from .views import CashMachineAPIView, QRCodeApiView

urlpatterns = [
    path("cash_machine/", CashMachineAPIView.as_view(), name="cash_machine"),
    path("media/<str:filename>/", QRCodeApiView.as_view(), name="qrcode"),

]
