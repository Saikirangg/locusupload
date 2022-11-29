
from flask import Flask, render_template, request
import pandas as pd
import boto3
import io
import requests
import json
import datetime

import urllib.request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
ACCESS_ID='AKIA3TWIOTPHANSQUBTU'
ACCESS_KEY='/a47w5jpstQI5K7P/Pk7IZ5DrfmP/ZfEUKJyGJXT'
bucketname = 'locusapi'

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        s3 = boto3.client('s3',aws_access_key_id=ACCESS_ID,aws_secret_access_key= ACCESS_KEY)
        s3.upload_file(f.filename, bucketname, f.filename)
        print("File uploaded to s3 bucket")
        s3 = boto3.resource('s3',aws_access_key_id=ACCESS_ID,aws_secret_access_key= ACCESS_KEY)
        print(s3)
        obj=s3.Object(bucketname,f.filename)
        # obj = s3.client(bucketname, f.filename)
        print(obj)
        body = obj.get()['Body'].read()
        df1 = pd.read_csv(io.BytesIO(body))
        # Order Date	Homebase ID	Homebase Execution Date	Homebase Slot Start	Homebase Slot End	Homebase Transaction Duration (minutes)	Location ID	Customer Execution Date	Customer Slot Start	Customer Slot End	Customer Transaction Duration (minutes)	Location Tag	Customer Place Name	Customer Address	Customer Locality	Customer City	Customer State	Customer Country	Customer Zipcode	Customer Location Latitude	Customer Location Longitude	Contact Name	Contact Number	Contact Alternate Number	Contact Email	Sku ID	Sku Line Item ID	Sku Detail	Payment Type	Amount	Currency	Notes	Volume	Volume Unit	Quantity	Quantity Unit	Weight	Weight Unit	what3words
        for i in range(len(df1)):
            print(df1)
            order_id = str(df1['Order ID'][i])
            types = (str(df1['Type'][i])).upper()
            team_id = str(df1['Team ID'][i])
            homebase_id = str(df1['Homebase ID'][i])
            category = str(df1['Category'][i])
            customer_address = str(df1['Customer Address'][i])
            customer_zipcode = str(df1['Customer Zipcode'][i])
            customer_city = str(df1['Customer City'][i])
            customer_state = str(df1['Customer State'][i])
            customer_country = str(df1['Customer Country'][i])
            contact_name = str(df1['Contact Name'][i])
            contact_number = str(df1['Contact Number'][i])
            customer_slot_start = str(df1['Customer Slot Start'][i])

            print("value of start is ",customer_slot_start)
            customer_slot_end = str(df1['Customer Slot End'][i])
            transaction_duration = int(df1['Customer Transaction Duration (minutes)'][i])
            volume = str(df1['Volume'][i])
            volume_unit = str(df1['Volume Unit'][i])
            quantity = str(df1['Quantity'][i])
            quantity_unit = str(df1['Quantity Unit'][i])
            # customer_notes = df1['customer_notes'][i]
            payment_type = (str(df1['Payment Type'][i])).upper()
            amount = float(df1['Amount'][i])
            currency = str(df1['Currency'][i])
            what3words = str(df1['what3words'][i])
            date = str(datetime.datetime.strptime(str(df1['Customer Execution Date'][i]), "%d-%m-%Y").strftime("%Y-%m-%d"))
            order_date = str(datetime.datetime.strptime(str(df1['Order Date'][i]), "%d-%m-%Y").strftime("%Y-%m-%d"))

            print(order_id)
            print(types)
            print(team_id)




            # url = "https://api.locus.sh/v1/orders"
            url = "https://oms.locus-api.com/v1/client/gourmetgarden-oiq/order/"+str(order_id)
            payload = json.dumps({
                "clientId": "gourmetgarden-oiq",
                "id": order_id,
                "type": types,
                "teamId": team_id,
                "homebaseId": homebase_id,
                "category": category,
                        "lineItems": [
                    {
                    "id": "Product",
                    "name": "Product",
                    "quantity": quantity,
                    "quantityUnit": quantity_unit
                    }
                ],
                "locationAddress": {
                    "placeName": "Locus Office",
                    "formattedAddress": customer_address,
                    "pincode": customer_zipcode,
                    "city": customer_city,
                    "state": customer_state,
                    "countryCode": customer_country
                },
                "contactPoint": {
                    "name": contact_name,
                    "number": contact_number
                },
                "slot": {
                    "start": "2022-11-30T03:00:00.000+0000",
                    "end": "2022-11-30T06:30:00.000+0000"
                },
                "amountTransaction": {
                "amount": {
                "amount": 0,
                "currency": "INR"
                },
                "exchangeType": "NONE"
                  },
                "transactionDuration": transaction_duration,
                "volume": {
                    "value": volume,
                    "unit": volume_unit
                },
                "quantity": {
                    "value": quantity,
                    "unit": quantity_unit
                },
                    "date": date,
                    "orderDate": order_date,
                    "what3words": "///mushroom.veto.foot"
            })
        
        headers = {
        'Authorization': 'Basic Z291cm1ldGdhcmRlbi1vaXE6Nzk4YmU5NDEtMzYzMS00ZjI1LTg2MjEtOTVkMmIyZjExOTEx',
        'Content-Type': 'application/json'
        }

            
        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text)


        # df = pd.read_csv(io.BytesIO(body))
        # print("length is ",str(len(df)))
        # # df.to_csv('output.csv', index=False)
        # print(df.columns)
        # order_id = df['Order ID']
        # alternate_id = df['Alternate ID']
        # team_id = df['Team ID']
        # scan_id = df['Scan ID']
        # types = df['Type']
        # print("value is ",str(order_id))
        # priority = df['Priority']
        # skills = df['Skills']
        # category = df['Category']
        # order_date = df['Order Date']
        # homebase_id = df['Homebase ID']
        # homebase_execution_date = df['Homebase Execution Date']
        # homebase_slot_start = df['Homebase Slot Start']
        # homebase_slot_end = df['Homebase Slot End']
        # homebase_transaction_duration = df['Homebase Transaction Duration (minutes)']
        # location_id = df['Location ID']
        # customer_execution_date = df['Customer Execution Date']
        # customer_slot_start = df['Customer Slot Start']
        # customer_slot_end = df['Customer Slot End']
        # customer_transaction_duration = df['Customer Transaction Duration (minutes)']
        # location_tag = df['Location Tag']
        # customer_place_name = df['Customer Place Name']
        # customer_address = df['Customer Address']
        # customer_locality = df['Customer Locality']
        # customer_city = df['Customer City']
        # customer_state = df['Customer State']
        # customer_country = df['Customer Country']
        # customer_zipcode = df['Customer Zipcode']
        # customer_location_latitude = df['Customer Location Latitude']
        # customer_location_longitude = df['Customer Location Longitude']
        # contact_name = df['Contact Name']
        # contact_number = df['Contact Number']
        # contact_alternate_number = df['Contact Alternate Number']
        # contact_email = df['Contact Email']
        # sku_id = df['Sku ID']
        # sku_line_item_id = df['Sku Line Item ID']
        # sku_detail = df['Sku Detail']
        # payment_type = df['Payment Type']
        # amount = df['Amount']
        # currency = df['Currency']
        # notes = df['Notes']
        # volume = df['Volume']
        # volume_unit = df['Volume Unit']
        # quantity = df['Quantity']
        # quantity_unit = df['Quantity Unit']
        # weight = df['Weight']
        # weight_unit = df['Weight Unit']
        # what3words = df['what3words']

#new api collection
        # url = "https://oms.locus-api.com/v1/client/gourmetgarden-oiq/order/AAA33278458"

        # payload = json.dumps({
        # "clientId": "gourmetgarden-oiq",
        # "id": str(order_id),
        # "type": "DROP",
        # "category": str(category),
        # "lineItems": [
        #     {
        #     "id": "Product",
        #     "name": "Product",
        #     "quantity": str(quantity),
        #     "quantityUnit": str(quantity_unit)
        #     }
        # ],
        # "locationAddress": {
        #     "localityName": "Koramangala",
        #     "formattedAddress": str(customer_address),
        #     "pincode": str(customer_zipcode),
        #     "city": str(customer_city),
        #     "state": str(customer_state),
        #     "countryCode": str(customer_country)
        # },
        # "slot": {
        #     "start": str(customer_slot_start),
        #     "end": str(customer_slot_end)
        # },
        # "transactionDuration": 600,
        # "volume": {
        #     "value": str(volume),
        #     "unit": str(volume_unit)
        # },
        # "amountTransaction": {
        #     "amount": {
        #     "amount": 0,
        #     "currency": "INR"
        #     },
        #     "exchangeType": "NONE"
        # },
        # "appFields": {
        #     "items": [
        #     {
        #         "item": "customerNotes",
        #         "format": "TEXT",
        #         "additionalValues": {
        #         "note": "joe@xyz.com"
        #         }
        #     }
        #     ]
        # },
        # "contactPoint": {
        #     "name": str(contact_name),
        #     "number": str(contact_number)
        # },
        # "homebaseId": str(homebase_id),
        # "teamId": str(team_id),
        # "date": "2022-07-14",
        # "orderDate": "2022-07-14",
        # "what3words": "///mushroom.veto.foot"
        # })
        # headers = {
        # 'Authorization': 'Basic Z291cm1ldGdhcmRlbi1vaXE6Nzk4YmU5NDEtMzYzMS00ZjI1LTg2MjEtOTVkMmIyZjExOTEx',
        # 'Content-Type': 'application/json'
        # }

        # response = requests.request("PUT", url, headers=headers, data=payload)

        # print(response.text)





        # s3 = boto3.resource('s3',aws_access_key_id=ACCESS_ID,aws_secret_access_key= ACCESS_KEY)
        # s3.upload_file('output.csv', bucketname, 'output.csv')
        # print("File converted to csv and uploaded to s3 bucket")
        # s3 = boto3.resource('s3')
        # obj = s3.client(bucketname, 'output.csv')
        # body = obj.get()['Body'].read()
        # df = pd.read_csv(io.BytesIO(body))
        # df.to_json('output.json', orient='records')
        # s3 = boto3.resource('s3',aws_access_key_id=ACCESS_ID,aws_secret_access_key= ACCESS_KEY)
        # s3.upload_file('output.json', bucketname, 'output.json')
        # print("File converted to json and uploaded to s3 bucket")
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)





# write a flask app to take file from html and save it to aws s3 bucket and print dataframes using pandas
# import libraries
# from flask import Flask, render_template, request
# import boto3
# import pandas as pd
# import io
# import os
# import sys
# import logging
# import json
# import time
# import datetime
# import numpy as np
# # import matplotlib.pyplot as plt
# # import seaborn as sns
# import warnings
# warnings.filterwarnings("ignore")
# # from sklearn.model_selection import train_test_split
# # from sklearn.linear_model import LinearRegression
# # from sklearn.metrics import mean_squared_error
# # from sklearn.metrics import r2_score
# # from sklearn.preprocessing import StandardScaler
# # from sklearn.preprocessing import MinMaxScaler
# # from sklearn.preprocessing import LabelEncoder
# # from sklearn.preprocessing import OneHotEncoder
# # from sklearn.preprocessing import PolynomialFeatures
# # from sklearn.linear_model import Ridge
# # from sklearn.linear_model import Lasso
# # from sklearn.linear_model import ElasticNet
# # from sklearn.linear_model import LogisticRegression
# # from sklearn.tree import DecisionTreeRegressor
# # from sklearn.ensemble import RandomForestRegressor
# # from sklearn.ensemble import GradientBoostingRegressor
# # from sklearn.ensemble import AdaBoostRegressor

# # create flask app
# app = Flask(__name__)

# # create a function to upload file to s3 bucket
# def upload_file_to_s3(file, bucket_name, acl="public-read"):
#     s3 = boto3.client(
#         "s3",
#         aws_access_key_id="",
#         aws_secret_access_key=""
#     )
#     try:
#         s3.upload_fileobj(
#             file,
#             bucket_name,
#             file.filename,
#             ExtraArgs={
#                 "ACL": acl,
#                 "ContentType": file.content_type
#             }
#         )
#     except Exception as e:
#         # This is a catch all exception, edit this part to fit your needs.
#         print("Something Happened: ", e)
#         return e
#     return "{}{}".format("https://s3-us-west-2.amazonaws.com/", bucket_name)

# # create a function to read file from s3 bucket
# def read_file_from_s3(bucket_name, file_name):
#     s3 = boto3.client(
#         "s3",
#         aws_access_key_id="",
#         aws_secret_access_key=""
#     )
#     try:
#         obj = s3.get_object(Bucket=bucket_name, Key=file_name)
#         df = pd.read_csv(io.BytesIO(obj['Body'].read()))
#         print(df.head())
#     except Exception as e:
#         # This is a catch all exception, edit this part to fit your needs.
#         print("Something Happened: ", e)
#         return e
#     return df







#html page
# Path: templates/index.html
# write a html page to take file from user and upload it to s3 bucket
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Upload File</title>
# </head>
# <body>
#     <h1>Upload File</h1>
#     <form action="/upload" method="POST" enctype="multipart/form-data">
#         <input type="file" name="file">
#         <input type="submit">   
#     </form>
# </body>
# </html>

# run the app
# if __name__ == "__main__":
#     app.run(debug=True)






