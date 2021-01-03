# Dockerfile
# Pull base image
FROM python:3.7
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*\
  && /usr/local/bin/python -m pip install --upgrade pip

RUN pip install psycopg2
RUN pip install pipenv 
# Requirements are installed here to ensure they will be cached.
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

# COPY ./compose/production/django/entrypoint /entrypoint
# RUN sed -i 's/\r$//g' /entrypoint
# RUN chmod +x /entrypoint

# COPY ./compose/local/django/start /start
# RUN sed -i 's/\r$//g' /start
# RUN chmod +x /start
ENV HOME=/certificate
ENV APP_HOME=/certificate
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME
COPY . $APP_HOME

# add and run as non-root user
# RUN adduser -D myuser
# USER myuser

# run gunicorn
CMD gunicorn certificate.wsgi:application --bind 0.0.0.0:$PORT

# ENTRYPOINT ["/entrypoint"]