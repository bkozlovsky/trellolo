from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
from .views import IndexListView, SignUpView, CardCreateView, CardUpdateView, CardDeleteView, CardViewSet, CardList
from .forms import UserLoginForm

router = DefaultRouter()
router.register(r'cards', CardViewSet)

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name="registration/login.html",
            authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('create/', CardCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', CardDeleteView.as_view(), name='card_delete'),
    path('update/<int:pk>/', CardUpdateView.as_view(), name='card_update'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('(?P<status>.+)/$', CardList.as_view()),
    path('api-v1/', include(router.urls)),
]