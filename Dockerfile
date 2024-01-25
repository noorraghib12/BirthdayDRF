FROM python:3.10-bookworm

WORKDIR /usr/src/app
RUN pip install -r requirements.txt


EXPOSE 8000
EXPOSE 5432


RUN python manage.py makemigrations accounts birthday_bot
RUN python manage.py migrate


ENTRYPOINT [ "python" ]
CMD ["manage.py","runserver","--host","0.0.0.0","--port","8000"]