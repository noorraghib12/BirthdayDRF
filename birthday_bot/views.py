from django.shortcuts import render
from rest_framework import views,parsers,response,status,permissions
from rest_framework import generics
from .serializer import *
# Create your views here.
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from .server_utils import regex_text_splitter,get_main_chain,pgretriever,embeddings,translate_model
from django.db.models import Func, F, Window
from django.db.models.functions import TruncDate
from django.db.models import Window
import random
from django.db import models
from django.db.models import Q
from rest_framework.response import Response
from pgvector.django import CosineDistance
from .server_utils import get_main_chain, embeddings,pgretriever
from accounts.serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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
    serializer_class=EventsSerializer
    def post(self, request, format=None):
        doc_paths=[] 
        for file in request.FILES.getlist('file'):
            up_dir=get_upload_path(file.name)
            save_uploaded_file(file=file,destination=up_dir)
            doc_paths.append(up_dir)
        events=regex_text_splitter(doc_paths)
        serializer=self.serializer_class(data=events,many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()            

        # do some stuff with uploaded file
        return response.Response(serializer.data,status=204)



class Random(models.Func):
    function = 'RANDOM'


class GetRandomCalenderEvent(views.APIView):
    def get(self,request):
        try:
            events_per_day = 2

            events = Events.objects.annotate(
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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 


    queryset=UserQuery.objects.all()
    serializer_class=QuerySerializer
    chain=chain=get_main_chain(retriever=pgretriever)
    
    def create(self,request,*args,**kwargs):
        data=request.data.copy()
        data['answer']=self.chain.invoke(data['question'])
        data['user']=request.user.id
        serialized=self.serializer_class(data=data)
        serialized.is_valid(raise_exception=True)
        
        # serialized.data['user']=request.user.id
        # serialized.data['answer']=answer
        serialized.save()
        return response.Response(
            data={
                    "answer":serialized.data['answer'],
                    "relation":serialized.data['relation']
                },
            status=status.HTTP_201_CREATED
            )


    def list(self,request, *args, **kwargs):
        list_queries=self.queryset.filter(user=request.user).order_by('-created_at')[:10]
        serialized=self.serializer_class(list_queries)
        return response.Response(serialized.data,status=status.HTTP_202_ACCEPTED)


class TextSuggestions(generics.ListAPIView):
    queryset=Events.objects.all()
    serializer_class=EventsSerializer
    embeddings=embeddings
    def list(self,request,text,*args,**kwargs):
        try:
            embedding=self.embeddings.embed_query(translate_model.translate(text)['translatedText'])
            filter_1=self.queryset.alias(distance=CosineDistance('embedding', embedding)).filter(distance__lt=0.60).order_by('distance')[:10]
            filter_2=self.queryset.filter(Q(event_en__contains=text) | Q(event_bn__contains=text)).all()
            # combined= filter_1 | filter_2
            combined= filter_2 | filter_1
            serialized=self.serializer_class(combined,many=True)
            return response.Response(serialized.data,status=status.HTTP_200_OK)
        except Exception as e:
            raise e


# class UserQueryAPI(generics.CreateAPIView):
#     queryset=UserQuery.objects.all()
#     serializer_class=QuerySerializer
#     def create(self,request,*args,**kwargs):
#         serialized=self.serializer_class(data=request.data)
#         serialized.is_valid(raise_exception=True)
#         serialized.save()
#         return response.Response(serialized.data,status=HTTP_201_CREATED)        






