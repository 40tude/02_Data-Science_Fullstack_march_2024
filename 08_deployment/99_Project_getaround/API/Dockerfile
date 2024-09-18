FROM python:3.9-slim
#FROM python:3.12-slim

WORKDIR /app

# copy files of the app in the container
COPY . /app

RUN pip install --no-cache-dir xgboost fastapi pandas joblib uvicorn scikit-learn pydantic numpy 
# One could use the line below
# Make sure to have the correct version and make sure you import the bare essentials
# RUN pip install -r requirements.txt

# Expose the port on which the app will use
EXPOSE 8000

# Run the app the same way we run it locally 
# Read api_getaround.py. 
# Indeed uvicorn is launched from there
CMD ["python", "api_getaround.py"]




