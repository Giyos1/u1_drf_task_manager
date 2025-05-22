# Django uchun Dockerfile
FROM python:3.12-slim

# Ishchi papkani o'rnatish
WORKDIR /app

# Host machine bilan aloqa uchun extra_hosts flagini qo'shish
# Bu Docker run qilganda qo'shimcha --add-host parametri bilan ishlaydi

# Fayllarni nusxalash
COPY . /app

# Kerakli kutubxonalarni o'rnatish
RUN pip install --upgrade pip && pip install -r requirment.txt

# Statik fayllarni tayyorlash (agar kerak bo'lsa)
#RUN python manage.py collectstatic --noinput

# Port ochish (optional)
EXPOSE 8000

# Container ishga tushganda Django serverni ishga tushiramiz
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["./entrypoint.sh"]