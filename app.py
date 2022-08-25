from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from joblib import load
import pandas as pd


app = Flask(__name__)
api = Api(app)

varOrder = load("X_variable_names.joblib","r")
class_names = load("class_labels.joblib","r")


class ModelHelpers():

    parser = reqparse.RequestParser()
    #for XVar in varOrder:
    parser.add_argument("petal length (cm)", type=list, location = "json", required = True, help = "PLen cannont be left blank")
    parser.add_argument("petal width (cm)", type=list, location = "json", required = True, help = "PWid cannont be left blank")
    parser.add_argument("sepal length (cm)", type=list, location = "json", required = True, help = "SLen cannont be left blank")
    parser.add_argument("sepal width (cm)", type=list, location = "json", required = True, help = "SWid cannont be left blank")

    def testDataFrame(jsonData):
        #switch json to a dataframe
        df = pd.DataFrame.from_dict(jsonData)
        #change the orde of the variables to match that of the input data
        df = df[varOrder]
        return df



class Model_info(Resource):

    def get(self):
        iris_model_components = {
            "models": ["Random_forest","Naive_bayes","SVM","Ensemble"],
            "necessary features": varOrder,
            "outputs": ["pred","prob"]
        }
        return jsonify(iris_model_components)


#all of the below classes could probably benefit from an the use of an Abtract Base Class

class Random_forest(Resource):
    def post(self, output):
        #grab data
        parser = ModelHelpers.parser
        data = parser.parse_args()
        X_test = ModelHelpers.testDataFrame(data)

        #load the model
        model = load("rf.joblib","r")
        if output == "pred":
            predictions = class_names[model.predict(X_test)]
            print(predictions)
            return {"predictions":predictions.tolist()}, 200
        elif output == "prob":
            probabilities = pd.DataFrame(model.predict_proba(X_test), columns = class_names)
            return {"probabilities":probabilities.to_dict()}
        else:
            return {"message": "unknown error"}



class Naive_bayes(Resource):
    def post(self, output):
        #grab data
        parser = ModelHelpers.parser
        data = parser.parse_args()
        X_test = ModelHelpers.testDataFrame(data)

        #load the model
        model = load("gnb.joblib","r")
        if output == "pred":
            predictions = class_names[model.predict(X_test)]
            print(predictions)
            return {"predictions":predictions.tolist()}, 200
        elif output == "prob":
            probabilities = pd.DataFrame(model.predict_proba(X_test), columns = class_names)
            return {"probabilities":probabilities.to_dict()}
        else:
            return {"message": "unknown error"}


class SVM(Resource):
    def post(self, output):
        #grab data
        parser = ModelHelpers.parser
        data = parser.parse_args()
        X_test = ModelHelpers.testDataFrame(data)

        #load the model
        model = load("svm.joblib","r")
        if output == "pred":
            predictions = class_names[model.predict(X_test)]
            print(predictions)
            return {"predictions":predictions.tolist()}, 200
        elif output == "prob":
            probabilities = pd.DataFrame(model.predict_proba(X_test), columns = class_names)
            return {"probabilities":probabilities.to_dict()}
        else:
            return {"message": "unknown error"}


class Ensemble(Resource):
    def post(self, output):
        #grab data
        parser = ModelHelpers.parser
        data = parser.parse_args()
        X_test = ModelHelpers.testDataFrame(data)

        #load the model
        model = load("ensemble.joblib","r")
        if output == "pred":
            predictions = class_names[model.predict(X_test)]
            print(predictions)
            return {"predictions":predictions.tolist()}, 200
        elif output == "prob":
            probabilities = pd.DataFrame(model.predict_proba(X_test), columns = class_names)
            return {"probabilities":probabilities.to_dict()}
        else:
            return {"message": "unknown error"}


api.add_resource(Model_info,"/list")
api.add_resource(Random_forest,"/Random_forest/<any(u'pred',u'prob'):output>")
api.add_resource(Naive_bayes,"/Naive_bayes/<any(u'pred',u'prob'):output>")
api.add_resource(SVM,"/SVM/<any(u'pred',u'prob'):output>")
api.add_resource(Ensemble,"/Ensemble/<any(u'pred',u'prob'):output>")

if __name__ == "__main__":
    app.run(port=5000, debug = True)