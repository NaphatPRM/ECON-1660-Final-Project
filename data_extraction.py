import csv
import numpy as np
import matplotlib.pyplot as plt
from insert_distance import distanceDetermine
from sklearn.linear_model import LinearRegression, Lasso


def cleanData(inputData):
    try:
        return float(inputData.strip("%").replace(",", "").strip())
    except ValueError:
        return inputData


# Emitted/Conditioning : ST_NUM,ST_NAME,UNIT_NUM,CITY,ZIPCODE
# OneHotEncoding:
def fileParsingProperty(file_name):
    with open(file_name, newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        list_not_need = ["PID", "CM_ID", "GIS_ID", "ST_NUM", "UNIT_NUM", "OWNER", "CD_FLOOR"]
        list_condition = ["ST_NAME", "CITY", "ZIPCODE"]
        list_emit = list_not_need + list_condition
        list_onehot = ["LU_DESC", "BLDG_TYPE", "OWN_OCC", ""]
        list_dict_reader = list(reader)
        list_result = []
        list_target = []
        print(list_dict_reader[0])
        for element in list_dict_reader:
            if element["GROSS_TAX"]:
                element = {k: cleanData(v) for k, v in element.items() if k not in list_emit}
                list_result.append(list({k: v for k, v in element.items() if k != "GROSS_TAX"}.values()))
                list_target.append(element["GROSS_TAX"])
    return list_result, list_target


def fileParsingOther(file_name):
    with open(file_name, newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        reader = list(reader)
        reader = list(map(lambda x: {k: cleanData(v) for k, v in x.items()}, reader))
        dict_return = {x["Cities"]: x for x in reader}
        return dict_return


# Plot to check the trending through the normal regression
def normalPlot_Regression(file_name, first_att, second_att):
    with open(file_name, newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        x = []
        y = []
        for element in list(reader):
            if element[first_att] and element[second_att] and \
                    float(element[second_att].strip('$').replace(",", "")) > 0.0:
                x.append(float(element[first_att]))
                y.append(float(element[second_att].strip('$').replace(",", "")))
        x = np.array(x)
        y = np.array(y)
        x = x.reshape(-1, 1)
        reg = LinearRegression()
        reg.fit(x, y)
        plt.scatter(x, y, color="red")
        plt.plot(x, reg.predict(x), color="blue")
        plt.xlabel("Living Area")
        plt.ylabel("Gross Tax")
        plt.title("Linear Regression of living area and Gross Tax")
        plt.show()


# LASSO
def straightLASSO(list_list_result, list_list_target):
    clf = Lasso(alpha=0.1)
    np_result = np.array(list_list_result)
    np_target = np.array(list_list_target)
    clf.fit(np_result, np_target)
    print("Coefficient" + clf.coef_)
    print("Intercept" + clf.intercept_)
    return clf


# result, target = fileParsingProperty("Property2022.csv")
# straightLASSO(result, target)
# normalPlot_Regression("Property2022.csv", "LIVING_AREA", "GROSS_TAX")
fileParsingOther("Neighbourhood_files/Race-Table 1.csv")
