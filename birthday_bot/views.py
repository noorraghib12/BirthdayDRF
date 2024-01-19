from django.shortcuts import render
from rest_framework import views,parsers,response,status
from rest_framework import generics
from .serializer import *
# Create your views here.
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from .server_utils import regex_text_splitter
def get_upload_path(filename):
    dir_=os.getcwd()
    return os.path.join(settings.STATIC_URL[1:],"uploads",filename)     


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

