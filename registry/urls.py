from django.urls import path

from . import views

urlpatterns = [
    path("facilities/", views.list_facilities),
    path("facilities/<uuid:pk>/", views.get_facility),
    path("workers/new/", views.register_health_worker),
    path("workers/<uuid:pk>/", views.get_health_worker),
    path("workers/tenures/new/", views.register_tenure),
    path("records/new/", views.create_record),
    path("records/ratings/new/", views.create_rating),
    path("records/<uuid:pk>/", views.get_record),
]
