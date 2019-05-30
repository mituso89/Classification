FROM python:3

WORKDIR /usr/src/app

COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt
RUN [ "python", "-c", "import nltk; nltk.download('stopwords')" ]


COPY . .

EXPOSE 5000

CMD [ "python", "app.py" ]