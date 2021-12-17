import json 

from django.http    import JsonResponse
from django.views   import View

from core.decorator import login_decorator
from users.models   import User
from movies.models  import Movie, Recommend, Review

class MovieCreateView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            if request.user.is_admin == False:
                return JsonResponse({"MESSAGE": "Only administrators can access"}, status=401)
                
            if data["title"] == '' or data["year"] == '' or data["genres"] == ''or data["summary"] == '':
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
