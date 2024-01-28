FROM python:3.10-bookworm

WORKDIR /usr/src/app
COPY ./. /usr/src/app/. 
RUN pip install -r requirements.txt


RUN python manage.py makemigrations accounts birthday_bot


EXPOSE 8000        

ENTRYPOINT [ "python" ]
CMD ["manage.py","migrate"]
CMD ["manage.py","runserver","0.0.0.0:8000"]
