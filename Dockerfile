FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install requests Flask bokeh pandas
ENV FLASK_APP app
ENV FLASK_ENV development

EXPOSE 5000

CMD ["python3", "-u", "./app.py"]