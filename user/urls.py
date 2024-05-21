from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('update', UserUpdateView.as_view()),
    path('companyList', CompanyListView.as_view()),
    path('companyListDetail', CompanyDetailView.as_view()),
    path('companyListInsert', CompanyInsertView.as_view()),
    path('companyListUpdate', CompanyUpdateView.as_view()),
    path('companyListDelete', CompanyDeleteView.as_view()),
    path('operatorList', OperatorListView.as_view()),
    path('operatorListDetail', OperatorDetailView.as_view()),
    path('operatorListInsert', OperatorInsertView.as_view()),
    path('operatorListUpdate', OperatorUpdateView.as_view()),
    path('operatorListDelete', OperatorDeleteView.as_view()),
    path('constantsList', ConstantsListView.as_view()),
    path('constantsListDetail', ConstantsDetailView.as_view()),
    path('constantsListInsert', ConstantsInsertView.as_view()),
    path('constantsListUpdate', ConstantsUpdateView.as_view()),
    path('constantsListDelete', ConstantsDeleteView.as_view()),
 
]