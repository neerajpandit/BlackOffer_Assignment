# dashboard_app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('data/', EnergyInsightListAPIView.as_view(), name='energy_insight_list'),
    path('intensity_country/',EnergyInsightListOilAPIView.as_view(),name='insight_list'),
    path('intensity_sector/',SectorAverageIntensityAPIView.as_view(),name='intensity_sector'),
    path('intensity_region/',EnergyInsightListRegionAPIView.as_view(),name='intensity_region'),
    path('average-likelihood-data/', AverageLikelihoodDataView.as_view(), name='average_likelihood_data'),
    path('relevance-data/', RelevanceDataView.as_view(), name='relevance-data'),
    path('topics/', TopicsView.as_view(), name='unique_topics'),
    path('sectors/', AllSectorsAPIView.as_view(), name='sectors'),
    path('likelihood_by_sector/', LikelihoodBySectorAPIView.as_view(), name='likelihood_by_sector'),
    path('relevance_by_sector/', RelevanceBySectorAPIView.as_view(), name='relevance_by_sector'),
    path('average_relevance_sectors/', AverageRelevanceAllSectorsAPIView.as_view(), name='average_relevance_sectors'),
    path('average_likelihood_sectors/', AverageLikelihoodAllSectorsAPIView.as_view(), name='average_likelihood_sectors'),





]

