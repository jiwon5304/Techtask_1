import json 

from django.http    import JsonResponse
from django.views   import View

from core.decorator import login_decorator
from users.models   import User
from movies.models  import Movie, Recommend, Review

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
                genres    = data["year"],
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