FROM python:3.8
COPY . .
RUN pip install requirements.txt
CMD ["streamlit run","app.py"]
