from django.urls  import path
from movies.views import MovieCreateView, ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('/create', MovieCreateView.as_view()),
    path('/reviewdetail/<int:review_id>', ReviewDetailView.as_view()),
    path('/<int:movie_id>/reviewcreate', ReviewCreateView.as_view()),
    path('/reviewupdate/<int:review_id>', ReviewUpdateView.as_view()),
    path('/reviewdelete/<int:review_id>', ReviewDeleteView.as_view()),
]