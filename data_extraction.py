import csv
import time

import numpy as np
import matplotlib.pyplot as plt
from insert_distance import distanceDetermine
from sklearn.linear_model import LinearRegression, Lasso


def cleanData(inputData):
    try:
        float(inputData.strip("%").strip("$").replace(",", "").strip())
        return float(inputData.strip("%").strip("$").replace(",", "").strip())
    except ValueError:
        return inputData


# Emitted/Conditioning : ST_NUM,ST_NAME,UNIT_NUM,CITY,ZIPCODE
# OneHotEncoding:
def fileParsingProperty(file_name, file_race):
    dict_race_neighbor = fileParsingOther(file_race)
    with open(file_name, newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        list_not_need = ["PID", "CM_ID", "GIS_ID", "ST_NUM", "UNIT_NUM", "OWNER", "CD_FLOOR"]
        list_condition = ["ST_NAME", "CITY", "ZIPCODE"]
        list_emit = list_not_need + list_condition
        list_onehot = ["LU_DESC", "BLDG_TYPE", "OWN_OCC"]
        list_dict_reader = list(reader)
        list_result = []
        list_target = []
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


def listSchool(file_name, target_name):
    list_school = []
    with open(file_name, newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        for element_school in list(reader):
            if target_name in element_school["LU_DESC"].lower() and "BENTONVILLE" not in element_school["MAIL_CITY"]:
                list_school.append({"Location": element_school["MAIL_ADDRESS"] + ", " + element_school["MAIL_CITY"],
                                    "Total_Value": cleanData(element_school["TOTAL_VALUE"])})
        list_school_sorted = sorted(list_school, key=lambda d: d['Total_Value'], reverse=True)
        return list_school_sorted[:20]


def distanceSchoolStorage(file_read, file_write, index_start, increments, type_focus, target_name):
    with open(file_read, newline="") as csvFile:
        list_school = listSchool(file_read, target_name)
        list_pair = []
        reader = csv.DictReader(csvFile)
        print(len(list_school))
        for element_other in list(reader):
            if type_focus.lower() in element_other["LU_DESC"].lower() \
                    and "BENTONVILLE" not in element_other["MAIL_CITY"]:
                location_focus = element_other["MAIL_ADDRESS"] + ", " + element_other["MAIL_CITY"]
                # total_distance = sum(list(map(lambda x: weightResult(location_focus, x), list_school)))
                list_pair.append(
                    (element_other["PID"], location_focus, float(element_other["GROSS_TAX"].strip("$").replace(",", "").strip())))
        print(len(list_pair))
        with open(file_write, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(["PID", "total_distance", "gross_tax"])
            counter = 0
            for i in range(index_start, index_start + increments):
                print(i)
                if counter == 10:
                    time.sleep(30.0)
                    counter = 0
                if "5TH FLOOR" not in list_pair[i][1]:
                    counter += 1
                    total_distance_list = list(map(lambda x: weightResult(list_pair[i][1], x), list_school))
                    if None not in total_distance_list:
                        writer.writerow([list_pair[i][0], sum(total_distance_list), list_pair[i][2]])


def distanceSchool(file_name, type_focus):
    with open(file_name, newline="") as csvFile:
        reader = csv.DictReader(csvFile)
        reader = list(reader)
        reader = filter(lambda diction: float(diction["total_distance"]) < 10 ** 11, reader)
        reader = sorted(reader, key=lambda u: u["total_distance"])
        list_distance = list(map(lambda x: float(x["total_distance"]), reader))
        list_gross_tax = list(map(lambda x: float(x["gross_tax"]), reader))
        list_distance = np.array(list(map(lambda y: y/(10.0 ** 6), list_distance)))
        list_gross_tax = np.array(list_gross_tax)
        list_distance = list_distance.reshape(-1, 1)
        reg = LinearRegression()
        reg.fit(list_distance, list_gross_tax)
        plt.scatter(list_distance, list_gross_tax, color="red")
        plt.plot(list_distance, reg.predict(list_distance), color="blue")
        plt.xlabel("Weighted Distance " + type_focus)
        plt.ylabel("Gross Tax")
        plt.title("Linear Regression of Weighted School Distance and Gross Tax for " + type_focus)
        plt.show()


def weightResult(firstLocation, secondMap):
    if distanceDetermine(firstLocation, secondMap["Location"]) is not None:
        return distanceDetermine(firstLocation, secondMap["Location"]) * secondMap["Total_Value"]
    else:
        return None


# result, target = fileParsingProperty("Property2022.csv")
# straightLASSO(result, target)
# normalPlot_Regression("Property2022.csv", "LIVING_AREA", "GROSS_TAX")
# fileParsingOther("Neighbourhood_files/Race-Table 1.csv")
# distanceSchoolStorage("Property2022.csv", "WeightedDistanceCONDOFull.csv", 67, 300, "CONDO", "school")
# distanceSchoolStorage("Property2022.csv", "WeightedDistanceCONDOFullOff.csv", 1, 300, "CONDO", "office")
distanceSchoolStorage("Property2022.csv", "WeightedDistanceTWO-FAMFullOff.csv", 148, 300, "TWO-FAM", "office")
distanceSchoolStorage("Property2022.csv", "WeightedDistanceTWO-FAMFull.csv", 204, 300, "TWO-FAM", "school")

# distanceSchool("WeightedDistanceTHREE-FAM.csv", "THREE-FAM")
