FROM python:latest
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask uWSGI requests redis
COPY /app /app
COPY cmd.sh /
RUN chown uwsgi /app/cmd.sh
EXPOSE 9090 9191 
USER uwsgi 
CMD ["/cmd.sh"]
