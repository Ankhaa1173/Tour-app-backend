import datetime
import json
import django
from django.shortcuts import render
from tourList.models import Order, Review, SavedPlace, TourItem, TourList
from tourList.serializers import OrderSerializer, ReviewSerializer, SavedPlaceSerializer, TourItemSerializer, tourListSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q, Avg
import qrcode
from io import BytesIO
from user.models import Company

# Create your views here.

def checkExistAndNotNone(key, body):
	if key in body and body[key] is not None:
		return True
	else:
		return False

class tourListView(APIView):
    def get(self, request):
        print("prson bn")
        data = TourList.objects.all()
        serializer = tourListSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = TourList.objects.all()
        body = request.data
        print(body)
        
        if checkExistAndNotNone('company', body):
            data = data.filter(company=body['company'])
        if checkExistAndNotNone('name', body):
            data = data.filter(name=body['name'])
        if checkExistAndNotNone('id', body):
            data = data.filter(id__in=body['id'])
        if checkExistAndNotNone('priceMax', body):
            data = data.filter(price__lte=body['priceMax'])
        if checkExistAndNotNone('priceMin', body):
            data = data.filter(price__gte=body['priceMin'])
        if checkExistAndNotNone('personMax', body):
            data = data.filter(recommended_people_no__lte=body['personMax'])
        if checkExistAndNotNone('personMin', body):
            data = data.filter(recommended_people_no__gte=body['personMin'])
        if checkExistAndNotNone('type', body):
            data = data.filter(type=body['type'])
        if checkExistAndNotNone('rating', body):
            average_ratings = Review.objects.values('tour_id').annotate(avg_rating=Avg('rating')).filter(avg_rating__gte=body['rating'])
            tour_ids = [rating['tour_id'] for rating in average_ratings]
            data = data.filter(id__in=tour_ids)
        if checkExistAndNotNone('tag', body):
            tag_value = body['tag']
            data = data.filter(
                Q(tag1=tag_value) | Q(tag2=tag_value) | Q(tag3=tag_value)
            )
        if checkExistAndNotNone('limit', body):
            print("body has limit")
            data = data[:body['limit']]
        
        serializer = tourListSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)

class tourDetailView(APIView):
    def post(self, request):
        data = TourList.objects.all()
        body = json.loads(request.body)
        tour_id = body.get('id')
        try:
            data = data.get(pk=tour_id)
        except TourList.DoesNotExist:
            return JsonResponse({'error': 'Tour not found'}, status=404)
        
        reviews = Review.objects.filter(tour_id=tour_id)
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        
        serializer = tourListSerializer(data, many=False)
        tour_data = serializer.data
        tour_data['average_rating'] = average_rating
        
        return JsonResponse(tour_data, safe=False)


class tourInsert(APIView):
	def post(self, request):
		ser = tourListSerializer(data=request.data)
		print(request.data)
		ser.is_valid(raise_exception=True)
		ser.save()
		return Response(ser.data)
	
class tourUpdate(APIView):
	def post(self, request):
		data = request.data
		tour = TourList.objects.get(pk = data['id'])
		tour.name = data['name']
		tour.duration = data['duration']
		tour.company = data['company']
		tour.price = data['price']
		tour.level = data['level']
		tour.modifiedDate = datetime.datetime.now(datetime.timezone.utc)
		tour.save()
		res = Response()
		res.data = {'status':'success'}
		return res
class tourDelete(APIView):
	def post(self, request):
		data = request.data
		tour = TourList.objects.get(pk = data['id'])
		tour.delete()
		res = Response()
		res.data = {'status':'success'}
		return res
	
class tourItemList(APIView):
	def post(self, request):
		filter  = request.data['tourId']
		data = TourItem.objects.filter(tour_id = filter)
		serializer = TourItemSerializer(data, many=True)
		return JsonResponse(serializer.data, safe=False)
class tourItemInsert(APIView):
	def post(self, request):
		ser = TourItemSerializer(data = request.data)
		ser.is_valid(raise_exception=True)
		ser.save()
		return Response(ser.data)
class tourItemUpdate(APIView):
	def post(self, request):
		data = request.data
		tourItem = TourItem.objects.get(pk = data['id'])
		if data['img_path']:
			tourItem.img_path = data['img_path']
		if data['duration']:
			tourItem.duration = data['duration']
		if data['price']:
			tourItem.price = data['price']
		if data['level']:
			tourItem.level = data['level']
		tourItem.modified_date = django.utils.timezone.now
		tourItem.save()
		res = Response()
		res.data = {'status':'success'}
		return res
class tourItemDelete(APIView):
	def post(self, request):
		filter  = request.data['tourId']
		data = TourItem.objects.filter(tour_id = filter)
		serializer = TourItemSerializer(data, many=True)
		return JsonResponse(serializer.data, safe=False)	
	
class tourReviewList(APIView):
    def post(self, request):
        body = request.data
        data = Review.objects.all()
        
        if checkExistAndNotNone('tourId', body):
            data = data.filter(tour_id=body['tourId'])
        if checkExistAndNotNone('userId', body):
            data = data.filter(user_id=body['userId'])
            
        serializer = ReviewSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
      
class tourReviewInsert(APIView):
	def post(self, request):
		ser = ReviewSerializer(data = request.data)
		ser.is_valid(raise_exception=True)
		ser.save()
		return Response(ser.data)

class tourReviewUpdate(APIView):
	def post(self, request):
		data = request.data
		review = Review.objects.get(pk = data['id'])
		if data['review']:
			review.review = data['review']
		if data['rating']:
			review.rating = data['rating']
		review.save()
		res = Response()
		res.data = {'status':'success'}
		return res

class tourReviewDetail(APIView):
	def post(self, request):
		data = request.data
		review = Review.objects.get(pk = data['id'])
		res = ReviewSerializer(review)
		return Response(res.data)

class SavedPlaceListView(APIView):
    def get(self, request):
        saved_places = SavedPlace.objects.all()
        serializer = SavedPlaceSerializer(saved_places, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        saved_places = SavedPlace.objects.all()
        body = request.data
        
        if checkExistAndNotNone('user_id', body):
            saved_places = saved_places.filter(user_id=body['user_id'])
        if checkExistAndNotNone('tour_id', body):
            saved_places = saved_places.filter(tour_id=body['tour_id'])

        serializer = SavedPlaceSerializer(saved_places, many=True)
        return JsonResponse(serializer.data, safe=False)

class SavedPlaceDetailView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        saved_place = SavedPlace.objects.get(pk=body.get('id'))
        serializer = SavedPlaceSerializer(saved_place, many=False)
        return JsonResponse(serializer.data, safe=False)
    
class SavedPlaceInsertView(APIView):
    def post(self, request):
        data = request.data
        if checkExistAndNotNone('tourIdList', data):
            tour_id_list = data.get('tourIdList')
            user_id = data.get('user_id')
            saved_places = []
            for tour_id in tour_id_list:
                saved_place_data = {'user_id': user_id, 'tour_id': tour_id}
                serializer = SavedPlaceSerializer(data=saved_place_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                saved_places.append(serializer.data)
            return Response(saved_places)
        else:
            serializer = SavedPlaceSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class SavedPlaceUpdateView(APIView):
    def post(self, request):
        data = request.data
        saved_place = SavedPlace.objects.get(pk=data['id'])
        if 'user_id' in data:
            saved_place.user_id = data['user_id']
        if 'tour_id' in data:
            saved_place.tour_id = data['tour_id']
        saved_place.save()
        return Response({'status': 'success'})

class SavedPlaceDeleteView(APIView):
    def post(self, request):
        data = request.data
        saved_place = SavedPlace.objects.get(pk=data['id'])
        saved_place.delete()
        return Response({'status': 'success'})

# Order Views
class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        orders = Order.objects.all()
        body = request.data
        
        if checkExistAndNotNone('user_id', body):
            orders = orders.filter(user_id=body['user_id'])
        if checkExistAndNotNone('tour_id', body):
            orders = orders.filter(tour_id=body['tour_id'])
        if checkExistAndNotNone('tour_date', body):
            orders = orders.filter(tour_date=body['tour_date'])
        if checkExistAndNotNone('order_date', body):
            orders = orders.filter(order_date=body['order_date'])
        if checkExistAndNotNone('status', body):
            orders = orders.filter(status=body['status'])
        if checkExistAndNotNone('is_confirmed', body):
            orders = orders.filter(is_confirmed=body['is_confirmed'])

        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

class OrderDetailView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        order = Order.objects.get(pk=body.get('id'))
        serializer = OrderSerializer(order, many=False)
        return JsonResponse(serializer.data, safe=False)

class OrderInsertView(APIView):
    def post(self, request):
        company = Company.objects.get(pk = request.data['company'])
        print(company)
        data = request.data
        data['bank_account_no'] =  company.bankaccountno
        print(data)
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = generate_qr_code(request, company.bankaccountno)
        return response
class OrderUpdateView(APIView):
    def post(self, request):
        data = request.data
        order = Order.objects.get(pk=data['id'])
        if 'tour_date' in data:
            order.tour_date = data['tour_date']
        if 'order_date' in data:
            order.order_date = data['order_date']
        if 'pay_amount' in data:
            order.pay_amount = data['pay_amount']
        if 'paid_amount' in data:
            order.paid_amount = data['paid_amount']
        if 'is_confirmed' in data:
            order.is_confirmed = data['is_confirmed']
        if 'company' in data:
            order.company = data['company']
        if 'bank_account_no' in data:
            order.bank_account_no = data['bank_account_no']
        if 'status' in data:
            order.status = data['status']
        order.save()
        return Response({'status': 'success'})

class OrderDeleteView(APIView):
    def post(self, request):
        data = request.data
        order = Order.objects.get(pk=data['id'])
        order.delete()
        return Response({'status': 'success'})
    
def generate_qr_code(request, data):
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add bank account number data to QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create PIL image from QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Create BytesIO object to hold image data
    buffer = BytesIO()

    # Save image to BytesIO object as PNG
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return image in HTTP response
    response = HttpResponse(buffer.getvalue(), content_type="image/png")
    return response
