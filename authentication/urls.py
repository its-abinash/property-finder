from django.conf.urls import include, url
from .views import (LoginUserView, LogoutUserView, RegisterUserView,
                    CurrentUserView)

urlpatterns = [
    url(r'^login/', LogoutUserView.as_view()),
    url(r'^register/', RegisterUserView.as_view()),
    url(r'^logout/', LogoutUserView.as_view()),
    url(r'^me/', CurrentUserView.as_view())
]
