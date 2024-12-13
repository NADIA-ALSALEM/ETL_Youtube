# استخدام صورة بايثون كـ base image
FROM python:3.10

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف requirements.txt إلى الحاوية
COPY requirements.txt /app/

# نسخ محتويات مجلد dags إلى الحاوية
COPY dags/ /app/dags/

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# تشغيل الملف المطلوب عند بدء الحاوية
CMD ["python", "/app/dags/etlyoutube.py"]

RUN adduser --disabled-password --gecos "" astro
USER astro
