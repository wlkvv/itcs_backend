from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from django.utils.dateparse import parse_datetime
from .jwt_helper import get_access_token, create_access_token, get_jwt_payload
from .permissions import IsAuthenticated, IsModerator
from .serializers import *


@api_view(["GET"])
def search_services(request):
    query = request.GET.get("query", "")

    services = Service.objects.filter(status=1).filter(name__icontains=query)

    serializer = ServiceSerializer(services, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_service_by_id(request, service_id):
    if not Service.objects.filter(pk=service_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Service.objects.get(pk=service_id)
    serializer = ServiceSerializer(service, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_service(request, service_id):
    if not Service.objects.filter(pk=service_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Service.objects.get(pk=service_id)
    serializer = ServiceSerializer(service, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_service(request):
    Service.objects.create()

    services = Service.objects.all()
    serializer = ServiceSerializer(services, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_service(request, service_id):
    user = request.user
    if not Service.objects.filter(pk=service_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Service.objects.get(pk=service_id)
    service.status = 2
    service.save()

    services = Service.objects.filter(status=1)
    serializer = ServiceSerializer(services, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_service_to_order(request, service_id):
    access_token = get_access_token(request)
    payload = get_jwt_payload(access_token)
    user_id = payload["user_id"]

    if not Service.objects.filter(pk=service_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Service.objects.get(pk=service_id)

    order = Order.objects.filter(status=1).filter(user_id=user_id).last()

    if order is None:
        order = Order.objects.create()
        order.date_created = datetime.now()
        order.status = 1

    order.services.add(service)
    order.user = CustomUser.objects.get(pk=user_id)
    order.save()

    serializer = ServiceSerializer(order.services, many=True)

    user_data = {
        "user_id": user_id,
        "current_cart": order.id if order else -1,
    }

    return Response({"services": serializer.data, "user_data": user_data})



@api_view(["GET"])
def get_service_image(request, service_id):
    if not Service.objects.filter(pk=service_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Service.objects.get(pk=service_id)

    return HttpResponse(service.image, content_type="image/png")

 
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_service_image(request, service_id):
    if not Service.objects.filter(pk=service_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Service.objects.get(pk=service_id)
    serializer = ServiceSerializer(service, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_orders(request):
    access_token = get_access_token(request)
    payload = get_jwt_payload(access_token)
    user_id = payload["user_id"]

    if user_id is None:
        return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.get(pk=user_id)
    if  user_id is not None:
        if user.is_moderator:
            print(user.is_moderator)
            start_day = request.GET.get('start_day')
            end_day = request.GET.get('end_day')
            category = request.GET.get('category', '')
            start_day = start_day.split(' ')[0:-5]
            end_day = end_day.split(' ')[0:-5]
            start_day = ' '.join(start_day)
            end_day = ' '.join(end_day)
            start_day = datetime.strptime(start_day, '%a %b %d %Y %H:%M:%S')
            end_day = datetime.strptime(end_day, '%a %b %d %Y %H:%M:%S')    
            applications = Order.objects.filter(date_created__range=(start_day, end_day)).exclude(status=5)
            if category and category != '0':
                applications = applications.filter(status=category).exclude(status=5)
        else:
            applications = Order.objects.filter(user_id=user_id).exclude(status=5)
        serializer = OrderSerializer(applications, many=True)
        return Response(serializer.data)
    else:
        return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)


    #     if start_day and end_day:
    #         # Преобразование строковых параметров в объекты datetime
    #         start_day = parse_datetime(start_day)
    #         end_day = parse_datetime(end_day)
    #     print (start_day )
    #     orders = Order.objects.all()

    #     if start_day and end_day:
    #         orders = orders.filter(created_at__range=(start_day, end_day))

    #     if category and category != '0':
    #         orders = orders.filter(status=category)

    #     orders = orders.exclude(status=5).exclude(status=1)
    # else:
    #     orders = Order.objects.filter(customer_id=user_id).exclude(status=5)

    # serializer = OrderSerializer(orders, many=True)
    # return Response(serializer.data)
    # print(request)
    # token = get_access_token(request)
    # payload = get_jwt_payload(token)
    # user_id = payload["user_id"]
    # orders = Order.objects.filter(user_id=user_id).exclude(status=5)
    # user = CustomUser.objects.get(pk=user_id)
    # if user.is_moderator:
    #     orders = Order.objects.all().exclude(status=5)

    # serializer = OrderSerializer(orders, many=True)

    # return Response(serializer.data)

# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def get_orders(request):
#     print(request)
#     token = get_access_token(request)
#     payload = get_jwt_payload(token)
#     user_id = payload["user_id"]
#     orders = Order.objects.filter(user_id=user_id).exclude(status=5)
#     user = CustomUser.objects.get(pk=user_id)
#     if user.is_moderator:
#         orders = Order.objects.all().exclude(status=5)

#     serializer = OrderSerializer(orders, many=True)

#     return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    order.status = 1
    order.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status  in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=order_id)
    lesson_status = order.status

    if lesson_status == 5:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = request_status
    if request_status  != 5:
        order.date_of_formation = datetime.now(tz=timezone.utc)
    if request_status  == 5:
        order.date_complete = datetime.now(tz=timezone.utc)
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=order_id)

    lesson_status = order.status

    if lesson_status in [3, 4, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = request_status
    if request_status  in [3, 5]:
        order.date_complete = datetime.now(tz=timezone.utc)
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    order.status = 5
    order.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_service_from_order(request, order_id, service_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Service.objects.filter(pk=service_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    order.services.remove(Service.objects.get(pk=service_id))
    order.save()

    serializer = ServiceSerializer(order.services, many=True)
    return Response(serializer.data)


access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()


@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token,
    }
    cache.set(access_token, user_data, access_token_lifetime)

    response = Response(user_data, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=True, expires=access_token_lifetime)

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    cache.set(access_token, user_data, access_token_lifetime)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

    return response


@api_view(["POST"])
def check(request):
    access_token = get_access_token(request)

    if access_token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if not cache.has_key(access_token):
        message = {"message": "Token is not valid"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    user_data = cache.get(access_token)

    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if cache.has_key(access_token):
        cache.delete(access_token)

    message = {"message": "Вы успешно вышли из аккаунта!"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie('access_token')

    return response

@api_view(['GET'])
def handle_async_task(request, order_id):
    token = "SomeToken123456"
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    print(order_id)
    second_service_url = "http://localhost:8088/async_task"
    data = {
        'order_id': order_id,
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(second_service_url, data=data)
    exp = Order.objects.get(pk=order_id)
    
    # Обработка ответа от второго сервиса
    if response.status_code == 200:
        print(response)
        exp.deadline = "На оценке..."
        exp.save()
        serializer = OrderSerializer(exp)
        return Response(serializer.data)
    else:
        return Response(data={'error': 'Запрос завершился с кодом: {}'.format(response.status_code)},
                        status=response.status_code)

@api_view(['PUT'])
def put_async(request, format=None):
    """
    Обновляет данные 
    """
    print("вызвалось")
    # Проверка метода запроса (должен быть PUT)
    if request.method != 'PUT':
        return Response({'error': 'Метод не разрешен'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    exp_id = request.data.get('order_id')
    result = request.data.get('fact_time')
    token = request.data.get('token')
    exp_token = 'SomeToken123456'
    

    if token != exp_token :
        return Response({'error': 'Отсутствуют необходимые данные'}, status=status.HTTP_400_BAD_REQUEST)


    # Проверка наличия всех необходимых параметров
    if not exp_id or not result :
        return Response({'error': 'Отсутствуют необходимые данные'}, status=status.HTTP_400_BAD_REQUEST)

  

    try:
        exp = Order.objects.get(id=exp_id)
    except Order.DoesNotExist:
        return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

    exp.deadline = str(result) + " Дней"
    exp.save()
    serializer = OrderSerializer(exp)
    print(serializer.data)
    return Response(serializer.data)
