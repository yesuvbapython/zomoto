from django.urls import path
from .views import registerUser,registerVendor,login,logout,cusDashboard,venDashboard,Account

urlpatterns = [
    path('registerUser/',registerUser,name="registerUser"),
    path('registerVendor/',registerVendor,name="registerVendor"),
    path('login/',login,name="login"),
    path('logout/',logout,name="logout"),
    path('cusDashboard/',cusDashboard,name="cusDashboard"),
    path('venDashboard/',venDashboard,name="venDashboard"),
    path('Account/',Account,name="Account"),
]
