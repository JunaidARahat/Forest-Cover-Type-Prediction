<h1 align="center">Forest Cover Type Prediction </h1>

<h5>
 Did you know predicting forest cover types can help conserve biodiversity and manage natural resources effectively? In my recent project, I developed a machine learning model to solve this critical challenge!
The objective is to predict the type of forest cover based on geographical and soil data. This prediction can assist forest rangers and policymakers in sustainable forest management
This data is from 4 wilderness areas located in the Roosevelt National Forest of northern Colorado.
The wilderness areas are:
1 - Rawah Wilderness Area
2 - Neota Wilderness Area
3 - Comanche Peak Wilderness Area
4 - Cache la Poudre Wilderness Area
The observation are taken from 30m x 30m patches of forest that are classified as one of seven cover types
1 - Spruce/Fir
2 - Lodgepole Pine
3 - Ponderosa Pine
4 - Cottonwood/Willow
5 - Aspen
6 - Douglas-fir
7 - Krummholz
 </h5>

 </br>
    Dataset url: [Kaggle](https://www.kaggle.com/competitions/forest-cover-type-prediction/data) 
</br>


- Python
- FastAPI
- Machine learning
- Docker
- Mongodb

## 🌐 Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions

 
This dataset has:
- 581012 samples or rows
- 55 features or columns 
- 1 target column (Cover_Type).


 ## 💻 How to setup:


Creating conda environment
```
conda create -n forest python==3.8 -y
```

activate conda environment
```
conda activate forest
```

Install requirements
```
pip install -r requirements.txt
```

Save the environment variable in .env file
```
AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY<AWS_SECRET_ACCESS_KEY>
 AWS_DEFAULT_REGION<AWS_DEFAULT_REGION>
```
Run the live server using uvicorn
```
python app.py
```
To launch ui
```
http://127.0.0.1:5000/
```

## 🏭 Industrial Use-cases 
1. Scientists can predict future wild fires & hence can save flora and fona.
2. Fire Rating Systems can be developed. 
