FROM python:3.9

RUN pip install pandas

# change the workdir to app after running the image
WORKDIR /app

COPY pipeline.py pipeline.py 

#Overide the entrypoint: when we run the image the default prompt is bash
# ENTRYPOINT [ "bash" ]  

ENTRYPOINT ["python","pipeline.py"]