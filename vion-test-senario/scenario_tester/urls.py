from django.urls import path
from scenario_tester.views import *

urlpatterns = [
    path('sessions/<int:pk>/', SessionDetailView.as_view(), name='session-detail'),
    path('test-scenarios/', TestAllScenariosView.as_view(), name='test-all-scenarios'),
]
