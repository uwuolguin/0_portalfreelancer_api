FROM python:3.12.3

WORKDIR /usr/src/app

#create a static folder in which you can upload static files
RUN mkdir -p /usr/src/app/static_folder

COPY requirements.txt ./

# install dependencies so cv2 works
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

