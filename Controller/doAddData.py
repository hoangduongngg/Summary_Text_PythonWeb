from flask import request, render_template

from DAO import DataDAO
from Model.Data import Data

def AddData():

    return render_template("/server/addData.html")