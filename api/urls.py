from django.urls import path
from removebg.views import index, person, remove_background

urlpatterns = [
    path('index/', index),
    path('person/',person),
    path('remove-background/', remove_background, name='remove-background'),
]
