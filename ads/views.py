import csv
import json

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_str
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Advertisments, Categories


def show(self):

    ''' This function accesses the root path, and returns a Json object '''

    return JsonResponse({
        "status": "ok"
    },
    status=200
    )


def csv_to_json(request):

    ''' This function converts CSV files to Json, returns Json, and saves the commented out piece of code to the sqlite database '''

    with open('datasets/ads.csv', 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        data = list(data)

    response = HttpResponse(content_type='text/plain; charset=utf-8')
    for row in data:
        row = [smart_str(cell) for cell in row]
        response.write('\t'.join(row) + '\n')

    # with open('datasets/ads.csv', 'r', encoding='utf-8') as f:
    #     reader = csv.DictReader(f)
    #     for row in reader:
    #         obj1 = Advertisments(name=row['name'], author=row['author'], price=row['price'],
    #                              description=row['description'],
    #                              address=row['address'])
    #         obj1.save()

    return response


def csv_cat_to_json(request):

    ''' This function converts CSV files to Json, returns Json, and saves the commented out piece of code to the sqlite database '''

    data = []
    with open('datasets/categories.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

            # obj1 = Categories(name=row['name'])
            # obj1.save()

    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    return JsonResponse(json_data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdvertismentView(View):

    ''' This class contains POST and GET methods for advertise '''

    def get(self, request):

        ''' This GET method returns all data from the Ads table database in Json format '''

        advertisments = Advertisments.objects.all()
        response = []
        for advertisment in advertisments:
            response.append(
                {
                    "id": advertisment.id,
                    "name": advertisment.name,
                    "author": advertisment.author,
                    "price": advertisment.price,
                }
            )
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):

        ''' This POST method returns data that you send to the database Ads table in Json format '''

        ads_data = json.loads(request.body)

        ads = Advertisments()
        ads.name = ads_data["name"]
        ads.author = ads_data["author"]
        ads.price = ads_data["price"]
        ads.description = ads_data["description"]
        ads.address = ads_data["address"]

        ads.save()

        return JsonResponse({
                'id': ads.id,
                'name': ads.name,
                "author": ads.author,
                "price": ads.price,
                "description": ads.description,
                "address": ads.address
            })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):

    ''' This class contains POST and GET methods for advertise '''

    def get(self, request):

        ''' This GET method returns all data from the Categories table database in Json format '''

        categories = Categories.objects.all()
        response = []
        for category in categories:
            response.append(
                {
                    "id": category.id,
                    "name": category.name,
                }
            )
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):

        ''' This POST method returns data that you send to the database table Categories in Json format '''

        cat_data = json.loads(request.body)

        cat = Categories()
        cat.name = cat_data["name"]

        cat.save()

        return JsonResponse({
                'id': cat.id,
                'text': cat.name,
            })


class DetViewAds(DetailView):

    ''' This class uses the DetailView class method '''

    model = Advertisments

    def get(self, request, *args, **kwargs):

        '''This method takes a category from the database in the Category table by the primary key specified in the address bar'''

        try:
            ads = self.get_object()
            response = {
                    'id': ads.id,
                    'name': ads.name,
                    'author': ads.author,
                    'price': ads.price,
                    "description": ads.description,
                    "address": ads.address
                }
        except Categories.DoesNotExist:
            return JsonResponse({
                "error": "advertise not found"
            },
            status=404
            )
        return JsonResponse(response)


class DetViewCat(DetailView):

    ''' This class uses the DetailView class method '''

    model = Categories

    def get(self, request, *args, **kwargs):

        '''This method takes a category from the database in the Category table by the primary key specified in the address bar'''

        try:
            cat = self.get_object()
            response = {
                    'id': cat.id,
                    'name': cat.name,
                }
        except Categories.DoesNotExist:
            return JsonResponse({
                "error": "category not found"
            },
            status=404
            )
        return JsonResponse(response)

