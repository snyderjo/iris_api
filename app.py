from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from joblib import load
from enum import Enum
from pandas import read_json
from werkzeug.routing import ValidationError, BaseConverter


app = Flask(__name__)
api = Api(app)

varOrder = load("X_variable_names.joblib","r")
class_names = load("class_labels.joblib","r")


class ModelHelpers():

    parser = reqparse.RequestParser()
    #for XVar in varOrder:
    parser.add_argument("petal length (cm)", type = float, required = True)
    parser.add_argument("petal width (cm)", type = float, required = True)
    parser.add_argument("sepal length (cm)", type = float, required = True)
    parser.add_argument("sepal width (cm)", type = float, required = True)

    def testDataFrame(jsonData):
        #switch json to a dataframe
        df = read_json(jsonData)
        #change the orde of
        df = df[varOrder]
        return df



class Model_info(Resource):

    def get(self):
        return {
            "models": ["Random_forest","Naive_bayes","SVM","Ensemble"],
            "necessary features": jsonify(varOrder),
            "output types": [jsonify(name) for name, value in ModelOutput.__members__.items()]
        }


#all of the below classes could probably benefit from an the use of an Abtract Base Class

class Random_forest(Resource,ModelHelpers):
    def post(self, output):
        #grab data
        data = cls.parser.parse_args()
        X_test = cls.testDataFrame(data)

        #load the model
        model = load("rf","rb")
        if output == "pred":
            predictions = class_names[model.predict(df)]
            return jsonify(predictions), 200
        elif output == "prob":
            probabilities = pd.dataframe(model.predict_proba(), columns = varOrder)
            return jsonify(probabilities), 200
        else:
            return {"message": "unknown error"}, 404



class Naive_bayes(Resource,ModelHelpers):
    def post(self, output):
        data = cls.parser.parse_args()
        pass


class SVM(Resource,ModelHelpers):
    def post(self, output):
        data = cls.parser.parse_args()
        pass


class Ensemble(Resource,ModelHelpers):
    def post(self, output):
        #data = cls.parser.parse_args()
        #df = cls.testDataFrame(data)
        pass


api.add_resource(Model_info,"/list")
api.add_resource(Random_forest,"/Random_forest/<any(pred,prob):output>")
api.add_resource(Naive_bayes,"/Naive_bayes/<any(pred,prob):output>")
api.add_resource(SVM,"/SVM/<any(pred,prob):output>")
api.add_resource(Ensemble,"/Ensemble/<any(pred,prob):output>")

if __name__ == "__main__":
    app.run(port=5000, debug =  True)