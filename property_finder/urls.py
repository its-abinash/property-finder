from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/auth/', include(("authentication.urls", "auth_urls"), namespace="auth_urls")),
    url(r'^api/listings/', include(("listings.urls", "listing_related_urls"), namespace="listing_related_urls")),
    # url(r'^api/bookings/', include(("bookings.urls", "booking_urls"), namespace="booking_urls")),
    # url(r'^api/reviews/', include(("reviews.urls", "reviews_and_rating_related_urls"), namespace="reviews_and_rating_related_urls")),
    # url(r'^api/notifications/', include(("notifications.urls", "notifications_urls"), namespace="notifications_urls")),
]
