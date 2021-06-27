"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
# from main.views import ProductListView, ProductDetailView

from main.views import *
from main.views import  ProductViewSet, RetrieveViewSet, OrderViewSet

router = SimpleRouter()
router.register('products', ProductViewSet)
router.register('reviews', RetrieveViewSet)
router.register('orders', OrderViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),

    # path('api/v1/products/', ProductViewSet.as_view(
    #     {'post':'create', 'get':'list'}
    # )),
    # path('api/v1/products/<int:pk>/', ProductViewSet.as_view(
    #     {'get':'retrieve',
    #      'put':'update',
    #      'patch':'partial_update',
    #      'delete':'destroy'}
    # )),
    # path('products/', ProductListView.as_view()),
    # path('products/<int:pk>/', ProductDetailView.as_view()),
    # path('api/v1/reviews/', CreateReview.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

