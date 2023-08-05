from django.http import HttpResponse
# Create your views here.


def test(request):
    return HttpResponse("app_test/test 接口被访问成功")

