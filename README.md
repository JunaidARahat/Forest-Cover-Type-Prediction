<h1 align="center">Forest Cover Type Prediction </h1>

<h5>  We need predict the forest cover type (the predominant kind of tree cover) from strictly cartographic variables (as opposed to remotely sensed data).
 The actual forest cover type for a given 30 x 30 meter cell was determined from US Forest Service (USFS) Region 2 Resource Information System data. 
 </h5>

 </br>
    Dataset url: [Kaggle](https://www.kaggle.com/competitions/forest-cover-type-prediction/data) 
</br>

## <img src="https://c.tenor.com/NCRHhqkXrJYAAAAi/programmers-go-internet.gif" width="25">  <b>Built With</b>

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
5. Terraform

 ## <img src="https://media2.giphy.com/media/QssGEmpkyEOhBCb7e1/giphy.gif?cid=ecf05e47a0n3gi1bfqntqmob8g9aid1oyj2wr3ds3mg700bl&rid=giphy.gif" width ="25"><b> Snippets </b>
 <b>FlowChart</b>
![Screenshot](snippets/flowchart.png)

![Screenshot](snippets/snip1.png)

![Screenshot](snippets/snip2.png)

![Screenshot](snippets/snip3.png)

![Screenshot](snippets/snip4.png)

![Screenshot](snippets/snip5.png)
## <img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="25"> <b> Data Understanding</b>

The dataset used to predict stroke is a dataset from Kaggle. This dataset has been used to predict student performance with  different model algorithms. This dataset has:
- 581012 samples or rows
- 55 features or columns 
- 1 target column (Cover_Type).


 ## 💻 How to setup:


Creating conda environment
```
conda create -p venv python==3.8 -y
```

activate conda environment
```
conda activate ./venv
```

Install requirements
```
pip install -r requirements.txt
```

Export the environment variable
```
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>
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