from django.urls import path

from . import views
from .views import get_zisan
from .views import display_posted_data

urlpatterns = [
    # path('postrequest_demo/', views.postrequest_demo, name='postrequest_demo'),
    path('list/',views.PlanList.as_view()),
    path('create/',views.PlanCreate.as_view()),
    path('display-posted-data/', display_posted_data, name='display_posted_data'),

    path('demo/', views.demo, name='demo'),  # Mapping '/demo' to demo view function
    path('delete/<int:pk>/', views.PlanDelete.as_view()),  # Endpoint for deletion
    #  path('hotel_offers', views.hotel_offers, name='hotel_offers'), # New endpoint
    # path('demo/hotels/', views.get_hotels, name='get_hotels'),  # New endpoint for GET response
    path('api/get_zisan/', get_zisan, name='get_zisan'),
    path('', views.demo, name='demo_form'),
    path('city_search/', views.city_search, name='city_search'),
    path('book_hotel/<str:offer_id>', views.book_hotel, name='book_hotel'),
    path('rooms_per_hotel/<str:hotel>/<str:departureDate>/<str:returnDate>', views.rooms_per_hotel, name='rooms_per_hotel')
]
