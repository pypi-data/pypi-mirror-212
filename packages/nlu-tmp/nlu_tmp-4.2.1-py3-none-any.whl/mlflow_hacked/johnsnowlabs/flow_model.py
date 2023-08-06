import mlflow_hacked as mlflow
import mlflow_hacked.johnsnowlabs as mlflow_jsl
import os
import sys
class MyModel(mlflow.pyfunc.PythonModel):
    def __init__(self, spell):
        os.environ['PYSPARK_PYTHON'] = sys.executable
        os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
        # self.spark = nlp.start()
        # self.pipe = nlp.load(spell)

    def predict(self, context, model_input):
        return 1 # self.pipe.predict(model_input)

    def my_custom_function(self, model_input):
        # do something with the model input
        return 0

    def save(self, path):
        print("yay")



def _load_pyfunc(path):
    """
    Load PyFunc implementation. Called by ``pyfunc.load_pyfunc``.
    """

    print("LOADING!??!")


def _save_model(sk_model, output_path, serialization_format):
    print('????SAVING!!')