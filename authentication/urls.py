from django.conf.urls import include, url
import authentication.views as auth_view

urlpatterns = [
    url(r'^login/', auth_view.LoginUserView.as_view()),
    url(r'^register/', auth_view.RegisterUserView.as_view()),
    url(r'^logout/', auth_view.LogoutUserView.as_view()),
    url(r'^me/', auth_view.CurrentUserView.as_view())
]
