from fastapi import FastAPI, Request, HTTPException
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from src.forest.pipeline.training_pipeline import TrainPipeline
from src.forest.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI()
TEMPLATES = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=200)
@app.post("/")
async def index(request: Request):
    try:
        return TEMPLATES.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering template: {e}")

@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("<h1>Training successful!!</h1>", status_code=200)

    except Exception as e:
        return Response(f"<h1>Error occurred: {e}</h1>", status_code=500)

@app.get("/predict")
async def predictRouteClient():
    try:
        prediction_pipeline = PredictionPipeline()
        prediction_pipeline.initiate_prediction()
        return Response("<h1>Prediction successful and predictions are stored in S3 bucket!!</h1>", status_code=200)

    except Exception as e:
        return Response(f"<h1>Error occurred: {e}</h1>", status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
