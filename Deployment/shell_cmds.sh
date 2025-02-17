# virtualenv activation

#django-admin startproject DJangoProject
#python manage.py startapp queue_system

cd ../queue_system

python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:5000
#python DJangoProject/queue_system/manage.py runserver 0.0.0.0:5000
