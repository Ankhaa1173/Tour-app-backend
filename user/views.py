import json
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import CompanySerializer, ConstantsSerializer, OperatorSerializer, UserSerializer
from .models import Company, Constants, Operator, User
import jwt, datetime

     
def checkExistAndNotNone(key, body):
    return key in body and body[key] is not None

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        print("login orsn bn")
        search = request.data['username']
        print(search)
        password = request.data['password']

        user = User.objects.filter(email=search).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        # response.set_cookie(key='jwt',value=token, expires=datetime.datetime.now() + datetime.timedelta(minutes=60), httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def post(self, request):
        token = request.data['jwt']
        if not token:
            raise AuthenticationFailed('Unauthenticated! token obso')

        try:
            payload = getPayloadJwt(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated! expired')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
def getPayloadJwt(token):
    return jwt.decode(token, 'secret', algorithms=['HS256'])

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
class UserUpdateView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        user = User.objects.get(pk = data['id'])
        res = Response()
        if checkExistAndNotNone('first_name', data):
            user.first_name = data['first_name']
        if checkExistAndNotNone('last_name', data):
            user.last_name = data['last_name']
        if checkExistAndNotNone('email', data):
            user.email = data['email']
        if checkExistAndNotNone('phone_no', data):
            user.phone_no = data['phone_no']
        if checkExistAndNotNone('password', data):
            user.set_password(data['password'])
            payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.timezone.utc)
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            res.data = {
            'jwt': token
            }
        user.save()
        if not res.data:
            res.data = {'status':'success'}
        return res

class OperatorListView(APIView):
    def get(self, request):
        operators = Operator.objects.all()
        serializer = OperatorSerializer(operators, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        operators = Operator.objects.all()
        body = request.data
        
        if checkExistAndNotNone('id', body):
            operators = operators.filter(id=body['id'])
        if checkExistAndNotNone('company_id', body):
            operators = operators.filter(company_id=body['company_id'])

        serializer = OperatorSerializer(operators, many=True)
        return JsonResponse(serializer.data, safe=False)

class OperatorDetailView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        operator = Operator.objects.get(pk=body.get('id'))
        serializer = OperatorSerializer(operator, many=False)
        return JsonResponse(serializer.data, safe=False)

class OperatorInsertView(APIView):
    def post(self, request):
        serializer = OperatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(pk = request.data['id'])
        user.user_level = 2
        user.save()
        return Response(serializer.data)

class OperatorUpdateView(APIView):
    def post(self, request):
        data = request.data
        operator = Operator.objects.get(pk=data['id'])
        if 'company_id' in data:
            operator.company_id = data['company_id']
        operator.save()
        return Response({'status': 'success'})

class OperatorDeleteView(APIView):
    def post(self, request):
        data = request.data
        operator = Operator.objects.get(pk=data['id'])
        operator.delete()
        return Response({'status': 'success'})

# Constants Views
class ConstantsListView(APIView):
    def get(self, request):
        constants = Constants.objects.all()
        serializer = ConstantsSerializer(constants, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        constants = Constants.objects.all()
        body = request.data
        if checkExistAndNotNone('id', body):
            constants = constants.filter(id=body['id'])
        if checkExistAndNotNone('group_name', body):
            constants = constants.filter(group_name=body['group_name'])
        if checkExistAndNotNone('name', body):
            constants = constants.filter(name=body['name'])
        if checkExistAndNotNone('data_type', body):
            constants = constants.filter(data_type=body['data_type'])
        if checkExistAndNotNone('value', body):
            constants = constants.filter(value=body['value'])

        serializer = ConstantsSerializer(constants, many=True)
        return JsonResponse(serializer.data, safe=False)

class ConstantsDetailView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        constant = Constants.objects.get(pk=body.get('id'))
        serializer = ConstantsSerializer(constant, many=False)
        return JsonResponse(serializer.data, safe=False)

class ConstantsInsertView(APIView):
    def post(self, request):
        serializer = ConstantsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ConstantsUpdateView(APIView):
    def post(self, request):
        data = request.data
        constant = Constants.objects.get(pk=data['id'])
        if 'group_name' in data:
            constant.group_name = data['group_name']
        if 'name' in data:
            constant.name = data['name']
        if 'data_type' in data:
            constant.data_type = data['data_type']
        if 'value' in data:
            constant.value = data['value']
        constant.save()
        return Response({'status': 'success'})

class ConstantsDeleteView(APIView):
    def post(self, request):
        data = request.data
        constant = Constants.objects.get(pk=data['id'])
        constant.delete()
        return Response({'status': 'success'})

class CompanyListView(APIView):
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        companies = Company.objects.all()
        body = request.data
        
        if checkExistAndNotNone('id', body):
            companies = companies.filter(id=body['id'])
        if checkExistAndNotNone('name', body):
            companies = companies.filter(name=body['name'])
        if checkExistAndNotNone('website', body):
            companies = companies.filter(website=body['website'])
        if checkExistAndNotNone('bankaccountno', body):
            companies = companies.filter(bankaccountno=body['bankaccountno'])

        serializer = CompanySerializer(companies, many=True)
        return JsonResponse(serializer.data, safe=False)

class CompanyDetailView(APIView):
    def post(self, request):
        body = json.loads(request.body)
        company = Company.objects.get(pk=body.get('id'))
        serializer = CompanySerializer(company, many=False)
        return JsonResponse(serializer.data, safe=False)

class CompanyInsertView(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CompanyUpdateView(APIView):
    def post(self, request):
        data = request.data
        company = Company.objects.get(pk=data['id'])
        if 'name' in data:
            company.name = data['name']
        if 'website' in data:
            company.website = data['website']
        if 'bankaccountno' in data:
            company.bankaccountno = data['bankaccountno']
        company.save()
        return Response({'status': 'success'})

class CompanyDeleteView(APIView):
    def post(self, request):
        data = request.data
        company = Company.objects.get(pk=data['id'])
        company.delete()
        return Response({'status': 'success'})
