from django.conf.urls import url
import listings.views as listing_view

urlpatterns = [
    url(r'^(?P<property_id>[0-9]+)/$', listing_view.PropertyListingView.as_view()),
    url(r'^', listing_view.PropertyListingsView.as_view()),
]
