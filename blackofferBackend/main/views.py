
# dashboard_app/views.py
from rest_framework import generics
from .models import EnergyInsight
from .serializers import EnergyInsightSerializer
from django.db.models import Func

class Lower(Func):
    function = 'LOWER'

class EnergyInsightListAPIView(generics.ListAPIView):
    queryset = EnergyInsight.objects.all()
    serializer_class = EnergyInsightSerializer
from django.db.models import Avg

class TopicsView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        # Get all unique topics from the EnergyInsight model
        topics = EnergyInsight.objects.values_list('topic', flat=True).distinct()
        topics_list = list(topics)
        return JsonResponse({'topics': topics_list}, safe=False)
class EnergyInsightListOilAPIView(generics.ListAPIView):
    def get_serializer_class(self):
        return EnergyInsightSerializer
    def get_queryset(self):
        # Get the 'topic' parameter from the request, default to 'oil'
        topic = self.request.query_params.get('topic','oil')
        # Get the 'year' parameter from the request
        year = self.request.query_params.get('year')
        # Filter the queryset based on the specified topic
        queryset = EnergyInsight.objects.exclude(topic__iexact=True).filter(topic__iexact=topic)
        queryset = queryset.exclude(country__isnull=True).exclude(country__exact='')
        # Optionally filter based on year
        if year:
            queryset = queryset.filter(published__year=year)
        # Calculate the average insight for each country
        average_insights = (
            queryset.values('country')
            .annotate(intensity=Avg('intensity'))
            .order_by('country')
        )
        # Return only the average insights for each country
        return average_insights
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Create a list of dictionaries from the queryset
        data = [{'country': item['country'], 'intensity': item['intensity']} for item in queryset]
        # Return the data as a JSON response
        return JsonResponse({'average_insights': data}, safe=False)







class EnergyInsightListRegionAPIView(generics.ListAPIView):

    def get_queryset(self):
        # Get the 'topic' parameter from the request, default to 'oil'
        topic = self.request.query_params.get('topic','oil')
        # Get the 'year' parameter from the request
        year = self.request.query_params.get('year')
        # Filter the queryset based on the specified topic
        queryset = EnergyInsight.objects.exclude(topic__exact='').filter(topic__iexact=topic)
        queryset = queryset.exclude(region__isnull=True).exclude(region__exact='')
        # Optionally filter based on year
        if year:
            queryset = queryset.filter(published__year=year)
        # Calculate the average insight for each country
        average_insights = (
            queryset.values('region')
            .annotate(intensity=Avg('intensity'))
            .order_by('region')
        )
        # Return only the average insights for each country
        return average_insights   
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Create a list of dictionaries from the queryset
        data = [{'region': item['region'], 'intensity': item['intensity']} for item in queryset]
        # Return the data as a JSON response
        return JsonResponse({'average_insights': data}, safe=False)
class SectorAverageIntensityAPIView(generics.ListAPIView):
    serializer_class = EnergyInsightSerializer
    def get_queryset(self):
        # Get the 'topic' parameter from the request, default to 'oil'
        sector = self.request.query_params.get('sector','energy')
        # Get the 'year' parameter from the request
        year = self.request.query_params.get('year')
        # Filter the queryset based on the specified topic  
        queryset = EnergyInsight.objects.exclude(sector__exact='').filter(sector__iexact=sector)
        queryset = queryset.exclude(country__isnull=True).exclude(country__exact='')
        # Optionally filter based on year
        if year:
            queryset = queryset.filter(published__year=year)
        # Calculate the average insight for each country
        average_insights = (
            queryset.values('country')
            .annotate(intensity=Avg('intensity'))
            .order_by('country')
        )
        return average_insights 

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Create a list of dictionaries from the queryset
        data = [{'country': item['country'], 'intensity': item['intensity']} for item in queryset]
        # Return the data as a JSON response
        return JsonResponse({'average_insights': data}, safe=False) 
from django.http import JsonResponse
from django.db.models import Count, Sum, F
from django.views import View

class AverageLikelihoodDataView(View):
    def get(self, request, *args, **kwargs):
        # Filter based on year if present
        year = request.GET.get('year')
        country = request.GET.get('country')
        queryset = EnergyInsight.objects.all()

        if year:
            queryset = queryset.filter(published__year=year)
        
        if country:
            queryset = queryset.filter(country=country)

        # Perform aggregation to get count and total_likelihood per topic
        grouped_data = queryset.values('topic').annotate(
            count=Count('id'),
            total_likelihood=Sum('likelihood')
        )

        # Calculate average likelihood
        average_likelihood_data = [
            {
                'topic': entry['topic'],
                'averageLikelihood': entry['total_likelihood'] / entry['count']
            }
            for entry in grouped_data
        ]

        return JsonResponse({'averageLikelihoodData': average_likelihood_data})

class RelevanceDataView(View):
    def get(self, request, *args, **kwargs):
        # Filter based on year if present
        year = request.GET.get('year')
        queryset = EnergyInsight.objects.all()

        if year:
            queryset = queryset.filter(published__year=year)
        # If a 'country' parameter is present, filter based on the country
        country = request.GET.get('country')
        if country:
            queryset = queryset.filter(country=country)

        # Perform aggregation to get count and total_relevance per item
        grouped_data = queryset.values('topic').annotate(
            count=Count('id'),
            total_relevance=Sum('relevance')
        )

        # Calculate average relevance
        relevance_data = [
            {
                'topic': entry['topic'],
                'relevance': entry['total_relevance'] / entry['count']
            }
            for entry in grouped_data
        ]

        return JsonResponse({'relevanceData': relevance_data})
class AllSectorsAPIView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        # Get all unique sector values
        sectors = EnergyInsight.objects.values_list('sector', flat=True).distinct()

        return JsonResponse({'sectors': list(sectors)})
    
class LikelihoodBySectorAPIView(generics.ListAPIView):
    serializer_class = EnergyInsightSerializer

    def get_queryset(self):
        # Get the 'sector' parameter from the request, default to 'energy'
        sector = self.request.query_params.get('sector', 'energy')
        # Get the 'year' parameter from the request
        year = self.request.query_params.get('year')
        # Filter the queryset based on the specified sector
        queryset = EnergyInsight.objects.exclude(sector__exact='').filter(sector__iexact=sector)
        queryset = queryset.exclude(region__isnull=True).exclude(region__exact='')
        queryset = queryset.annotate(lower_region=Lower('region'))
        # Optionally filter based on year
        if year:
            queryset = queryset.filter(published__year=year)
        # Calculate the average likelihood for each region
        likelihood = (
            queryset.values('region')
            .annotate(likelihood=Avg('likelihood'))
            .order_by('region')
        )
        return likelihood
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Create a list of dictionaries from the queryset
        data = [{'region': item['region'], 'likelihood': item['likelihood']} for item in queryset]
        # Return the data as a JSON response
        return JsonResponse({'likelihood': data}, safe=False)
    



    # RelevanceBySectorAPIView

from django.http import JsonResponse
from django.db.models import Avg, Func

class Lower(Func):
    function = 'LOWER'

class RelevanceBySectorAPIView(generics.ListAPIView):
    serializer_class = EnergyInsightSerializer

    def get_queryset(self):
        # Get the 'sector' parameter from the request, default to 'energy'
        sector = self.request.query_params.get('sector', 'energy')
        # Get the 'year' parameter from the request
        year = self.request.query_params.get('year')
        # Filter the queryset based on the specified sector
        queryset = EnergyInsight.objects.exclude(sector__exact='').filter(sector__iexact=sector)
        queryset = queryset.exclude(region__isnull=True).exclude(region__exact='')
        # Make the filtering case-insensitive for the 'region'
        queryset = queryset.annotate(lower_region=Lower('region'))
        # Optionally filter based on year
        if year:
            queryset = queryset.filter(published__year=year)
        # Calculate the average relevance for each region
        relevance = (
            queryset.values('region')
            .annotate(relevance=Avg('relevance'))
            .order_by('region')
        )
        return relevance
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # Create a list of dictionaries from the queryset
        data = [{'region': item['region'], 'relevance': item['relevance']} for item in queryset]
        # Return the data as a JSON response
        return JsonResponse({'relevance': data}, safe=False)


class AverageRelevanceAllSectorsAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        # Get the 'year' parameter from the request
        year = self.request.query_params.get('year')      
        # Get all unique sector values
        sectors = EnergyInsight.objects.values_list('sector', flat=True).distinct()
        relevance_data = []
        for sector in sectors:
            # Filter the queryset based on the specified sector
            queryset = EnergyInsight.objects.exclude(sector__exact='').exclude(sector__isnull=True).filter(sector__iexact=sector)
            # queryset = queryset.exclude(region__isnull=True).exclude(region__exact='')
            # Make the filtering case-insensitive for the 'region'
            queryset = queryset.annotate(lower_region=Lower('region'))
            # Optionally filter based on year
            if year:
                queryset = queryset.filter(published__year=year)
            # Calculate the average relevance for each region
            relevance = queryset.aggregate(relevance=Avg('relevance'))['relevance']
            # Append sector and average relevance to the list
            relevance_data.append({
                'sector': sector,
                'averageRelevance': relevance
            })

        return JsonResponse({'relevance': relevance_data})
    

class AverageLikelihoodAllSectorsAPIView(generics.ListAPIView):
    serializer_class = EnergyInsightSerializer

    def get(self, request, *args, **kwargs):
        # Get the 'year' parameter from the request
        year = self.request.query_params.get('year')      
        # Get all unique sector values
        sectors = EnergyInsight.objects.values_list('sector', flat=True).distinct()
        likelihood_data = []
        for sector in sectors:
            # Filter the queryset based on the specified sector
            queryset = EnergyInsight.objects.exclude(sector__exact='').filter(sector__iexact=sector)
            queryset = queryset.exclude(region__isnull=True).exclude(region__exact='')
            # Optionally filter based on year
            if year:
                queryset = queryset.filter(published__year=year)
            # Calculate the average likelihood for each region
            likelihood = queryset.aggregate(likelihood=Avg('likelihood'))['likelihood']
            # Append sector and average likelihood to the list
            likelihood_data.append({
                'sector': sector,
                'averageLikelihood': likelihood
            })

        return JsonResponse({'likelihood': likelihood_data})