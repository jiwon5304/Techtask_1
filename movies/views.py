import json

from django.http        import JsonResponse
from django.views       import View 
from django.db.models   import Q

from core.decorator     import login_decorator
from movies.models      import Movie, Recommend, Review


# 1. 영화 리스트조회 API
class MovieListView(View):
    @login_decorator
    def get(self, request):
        try:
            limit  = int(request.GET.get("limit","10"))
            offset = int(request.GET.get("offset","0"))

            genres         = request.GET.get("genres", None)
            year           = request.GET.get("year", None)
            search_keyword = request.GET.get("keyword", None)
            rating         = request.GET.get("rating", None)

            q = Q()

            if genres:
                q &= Q(genres__icontains=genres)

            if year:
                q &= Q(year=year)

            if search_keyword:
                q &= Q(title__icontains=search_keyword)
            
            all_movies = Movie.objects.filter(q)
            
            if rating == "up":
                all_movies = all_movies.order_by('rating')

            if rating == "down":
                all_movies = all_movies.order_by('-rating')

            offset  = offset*limit
            movies  = all_movies[offset:offset+limit]

            movies_list = [{
                "id"      : movie.id,
                "title"   : movie.title,
                "year"    : movie.year,
                "rating"  : movie.rating,
                "genres"  : movie.genres,
                "summary" : movie.summary,
            }for movie in movies]

            result = {
                "count": len(movies_list),
                "data" : movies_list
            }
            return JsonResponse({"results": result}, status=200)

        except Movie.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST_MOVIE"}, status=404)


# 2. 영화 상세조회 API
class MovieDetailView(View):
    @login_decorator
    def get(self, request, movie_id):
        try:
            reviews     = Review.objects.filter(movie_id=movie_id)
            review_list = [review.text for review in reviews]

            movie = Movie.objects.get(id=movie_id)

            result = {
                "id"      : movie.id,
                "title"   : movie.title,
                "rating"  : movie.rating,
                "genres"  : movie.genres,
                "summary" : movie.summary,
                "review"  : review_list
            }
            return JsonResponse({"results": result}, status=200)

        except Movie.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST_MOVIE"}, status=404)

# 3. 영화 생성 API
class MovieCreateView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            # 관리자만 영화 생성이 가능함
            if request.user.is_admin == False:
                return JsonResponse({"MESSAGE": "Only administrators can access"}, status=403)
            
            if data["title"] == '' or data["year"] == '' or data["genres"] == '' or data["summary"] == '' :
                return JsonResponse({"MESSAGE": "INPUT_ERROR"}, status=400)
            
            Movie.objects.create(
                title     = data["title"],
                year      = data["year"],
                rating    = 0.0,
                genres    = data["genres"],
                summary   = data["summary"]
                )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

# 4. 리뷰 상세조회 API
class ReviewDetailView(View):
    @login_decorator
    def get(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)

            # 리뷰가 수정되었다면 수정된 시간을 반환하도록 함.
            result = {
                "id"         : review.id,
                "text"       : review.text,
                "rating"     : review.rating,
                "created_at" : review.updated_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return JsonResponse({"results": result}, status=200)

        except Review.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST_REVIEW"}, status=404)

# 5. 리뷰 생성 API
class ReviewCreateView(View):
    @login_decorator
    def post(self, request, movie_id):
        try:
            data = json.loads(request.body)
            movie = Movie.objects.get(id=movie_id)

            # 한 유저당 동일한 영화에 1개의 리뷰 작성만 가능
            if Review.objects.filter(user_id=request.user.id, movie_id=movie.id).exists():
                return JsonResponse({"MESSAGE": "Only one review per movie"}, status=403)

            if movie_id == '' or data["text"] == '' or data["rating"] == '' :
                return JsonResponse({"MESSAGE": "INPUT_ERROR"}, status=400)
            
            Review.objects.create(
                user   = request.user,
                movie  = movie,
                text   = data["text"],
                rating = data["rating"]
                )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


# 6. 리뷰 수정 API
class ReviewUpdateView(View):
    @login_decorator
    def post(self, request, review_id):
        try:
            data = json.loads(request.body)
            review = Review.objects.get(id=review_id)
            
            # 본인의 리뷰만 수정 가능
            if not review.user == request.user:
                return JsonResponse({"MESSAGE": "You can only update your own review"}, status=403)

            if data["text"] == '' or data["rating"] == '' :
                    return JsonResponse({"MESSAGE": "INPUT_ERROR"}, status=400)

            review.text   = data["text"]
            review.rating = data["rating"]
            review.save()
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except Review.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST_REVIEW"}, status=404)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


# 7. 리뷰 삭제 API
class ReviewDeleteView(View):
    @login_decorator
    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)

            # 본인의 리뷰만 삭제 가능
            if not review.user == request.user:
                return JsonResponse({"MESSAGE": "You can only delete your own review"}, status=403)
            
            Review.objects.filter(id=review.id).delete()

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except Review.DoesNotExist:
            return JsonResponse({"MESSAGE": "DOES_NOT_EXIST_REVIEW"}, status=404)

# 8. 리뷰추천 생성 API
class RecommendCreateView(View):
    @login_decorator
    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            
            # 같은 댓글은 한번만 추천 가능
            if Recommend.objects.filter(user=request.user, review=review).exists():
                return JsonResponse({"MESSAGE": "already recommended"}, status=400)

            Recommend.objects.create(
                user   = request.user,
                review = review
                )
            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

# 9. 리뷰추천 삭제 API
class RecommendDeleteView(View):
    @login_decorator
    def post(self, request, review_id):
        try:
            if not Recommend.objects.filter(user_id=request.user.id, review_id=review_id).exists():
                return JsonResponse({"MESSAGE": "already un-recommended"}, status=400)

            Recommend.objects.filter(user_id=request.user.id, review_id=review_id).delete()

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)