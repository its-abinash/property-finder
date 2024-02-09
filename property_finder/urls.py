from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/auth/', include("authentication.urls", namespace="auth_urls")),
    url(r'^api/listings/', include("listings.urls", namespace="listing_related_urls")),
    url(r'^api/users/', include("user_profile.urls", namespace="user_profile_related_urls")),
    url(r'^api/bookings/', include("bookings.urls", namespace="booking_urls")),
    url(r'^api/reviews/', include("reviews.urls", namespace="reviews_and_rating_related_urls")),
    url(r'^api/notifications/', include("notifications.urls", namespace="notifications_urls")),
]
