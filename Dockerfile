FROM python:3.8
COPY . .
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["streamlit","run","app.py"]
