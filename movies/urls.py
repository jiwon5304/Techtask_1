from django.urls  import path
from movies.views import MovieListView, MovieDetailView, MovieCreateView, ReviewDetailView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView, RecommendCreateView, RecommendDeleteView

urlpatterns = [
    path('', MovieListView.as_view()),
    path('/<int:movie_id>', MovieDetailView.as_view()),
    path('/create', MovieCreateView.as_view()),
    path('/reviewdetail/<int:review_id>', ReviewDetailView.as_view()),
    path('/<int:movie_id>/reviewcreate', ReviewCreateView.as_view()),
    path('/reviewupdate/<int:review_id>', ReviewUpdateView.as_view()),
    path('/reviewdelete/<int:review_id>', ReviewDeleteView.as_view()),
    path('/recommendation/create/<int:review_id>', RecommendCreateView.as_view()),
    path('/recommendation/delete/<int:review_id>', RecommendDeleteView.as_view()),
]