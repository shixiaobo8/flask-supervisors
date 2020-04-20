FROM python:3.6.10
#FROM python:3.6.10-alpine
COPY . /app
WORKDIR /app
RUN pip install -i https://pypi.douban.com/simple --no-cache-dir -r requirments.txt 
CMD python manage.py run -h 0.0.0.0 -p 7001
EXPOSE 7001
