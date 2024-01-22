from django.shortcuts import render
from rest_framework import views,parsers,response,status,permissions
from rest_framework import generics
from .serializer import *
# Create your views here.
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from .server_utils import regex_text_splitter
from django.db.models import Func, F, Window
from django.db.models.functions import TruncDate
from django.db.models import Window
import random
from django.db import models





def get_upload_path(filename):
    uploads_path=os.path.join(settings.STATIC_URL[1:],"uploads")
    os.makedirs(uploads_path,exist_ok=True)
    return os.path.join(uploads_path,filename)     


def save_uploaded_file(file: InMemoryUploadedFile, destination: str):
    # Step 1: Access the content of the InMemoryUploadedFile
    file_content = file.read()

    # Step 2: Create or open a file on disk
    with open(destination, 'wb') as destination_file:
        # Step 3: Write the content of the InMemoryUploadedFile to the file on disk
        destination_file.write(file_content)


class FileUploadView(views.APIView):
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, format=None):
        doc_paths=[] 
        for file in request.FILES.getlist('file'):
            up_dir=get_upload_path(file.name)
            save_uploaded_file(file=file,destination=up_dir)
            doc_paths.append(up_dir)
            text=regex_text_splitter(doc_paths)
            

        # do some stuff with uploaded file
        return response.Response(text,status=204)




# class FileUploadView(generics.CreateAPIView):
#     serializer_class=UploadSerializer
    
#     def create(self,request,*args,**kwargs):
#         serialized=self.serializer_class(data=request.data.copy())
#         serialized.is_valid(raise_exceptions=True)
#         serialized.save()
#         return response.Response(serialized.data,status=status.HTTP_201_CREATED)     

class EventsViewSet(generics.CreateAPIView):
    queryset=Events.objects.all()
    serializer_class=EventsSerializer
    
    def create(self,request,*args,**kwargs):
        serializer=serializer_class(data=request.data,many=True)
        serializer.is_valid(raise_exceptions=True)
        serializer.save()

class Random(models.Func):
    function = 'RANDOM'


class GetRandomCalenderEvent(views.APIView):    
    
    def get(self,request):
        try:
            events_per_day = 2

            events = Event.objects.annotate(
                date_truncated=TruncDate('date'),
                event_random=Random(),
                event_rank=Window(
                    expression=F('event_random'),
                    partition_by=[TruncDate('date')],
                    order_by=F('event_random').asc()
                )
            ).filter(
                event_rank__lte=events_per_day
            ).order_by('date')
            
            events=EventsSerializer(events,many=True)
            return response.Response(data=events.data,status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({'error':e},status=status.HTTP_400_BAD_REQUEST)
            
                
class QueryAPI(generics.ListCreateAPIView):
    queryset=UserQuery.objects.all()
    serializer_class=QuerySerializer
    permission_classes=[permissions.IsAuthenticated]
    def create(self,request,*args,**kwargs):
        data=request.data.copy()
        serialized=serializer_class(data=data)
        serialized.is_valid(raise_exceptions=True)
        serialized.save()
        return response.Response(
            data={
                serialized['relation'],
                serialized['answer']
                },
            status=status.HTTP_201_CREATED
            )


    def list(self,request, *args, **kwargs):
        list_queries=queryset.filter(user=request.user).order_by('-created_at').limit(10)
        serialized=serializer_class(list_queries)
        return response.Response(serialized.data,status=status.HTTP_202_ACCEPTED)


