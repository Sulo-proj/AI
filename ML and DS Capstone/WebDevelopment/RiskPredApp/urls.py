# from django.conf.urls import url
from RiskPredApp import views
from django.urls import path

app_name = 'RiskPredApp'

urlpatterns = [
    path('', views.dataUploadView.as_view(), name = 'RiskPred'),

]