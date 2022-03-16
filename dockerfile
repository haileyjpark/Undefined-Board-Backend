FROM python:3

WORKDIR /Users/haileypark/projects/Board_project

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Board.wsgi:application"]