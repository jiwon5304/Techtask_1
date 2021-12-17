from django.urls  import path
from movies.views import MovieCreateView

urlpatterns = [
    path('/create', MovieCreateView.as_view()),
]