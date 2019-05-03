FROM tiangolo/uwsgi-nginx-flask:python3.6
ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
RUN python -m nltk.downloader all
RUN export PYTHONPATH="$PYTHONPATH:/var/www/app/"