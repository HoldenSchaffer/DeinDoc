from flask import Flask, render_template, url_for, flash, redirect, request
import itemAPI
import docAPI
from forms import ButtonForm
import json
import requests
import http.client
app = Flask(__name__)

cartList = []
disease = "Stomach Virus"

url = "https://api-reg-apigee.ncrsilverlab.com/v2/orders"
token = "Bearer gAAAAI9mfh0MQOImPfIq_-t16m5X-YlS9BtuNnduMepspYDEP4Jc5fYU1fJvLM8RviC0O2GaGlqAg-kUdCGXTjQDkKbb4x1NXThxX2Ryixa6YW4kBqqac4BtRAFJa-_s-JZvHONSW6eoPj5oSHwJNhILse3owHP7GHxiVudO35fkeQfV9AAAAIAAAAAOP6dp_eZsmhLbkkeL4T1LUpqVI8j8og3AFaouE-dR_0oWSKCLExotJofDMNaBIQMutYW4LosPe2sUSDtY6Yt58gDSmxJNNGPaFyMSIIWogwBwcC_GGL6FPlZioaRH9_cs0iLO5yO7ykBZllkGl1-W_nPivh70u4KS6nfABjHEiUepedrFjrSVqOHpCsnIXGSGXhLEBB65UiKWQqcKmQ0YDraFpXYaGIOEyp8If3DAuihqlns9PMgCIRqCzC-oLtabvt2GLwNsI6FJYX5vdQOZicOityc5dYjSZXKJiksdYSjPTJ6dpBW9dGxwjyJxMTw"
querystring = {"store_number":"1"}
headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'Host': "api-reg-apigee.ncrsilverlab.com",
    'Authorization': token,
    'cache-control': "no-cache",
    'Postman-Token': "40677c10-b4da-4d85-acf9-8791f890e36f"
    }
app.config['SECRET_KEY'] = 'dave'

def getAuth():
    url = "https://api-reg.ncrsilverlab.com/v2/OAuth2/token"

    headers = {
        'client_id': "gt_552463",
        'client_secret': "004e007a-004a-0035-4b00-740033006800",
        'cache-control': "no-cache",
        'Postman-Token': "96f96790-a161-407b-80e6-7cb4f773a37b"
        }

    authResponse = requests.request("GET", url, headers=headers)
    parsed_auth = (json.loads(authResponse.text))
    token = "Bearer " + parsed_auth["Result"]["AccessToken"]

def pushOrder(item, items):
    itemNum = str(item)
    itemName = items[item].name
    itemPrice = str(items[item].price)

    payload = "{\n    \n  \"Orders\": [\n    {\n      \"IsClosed\": true,\n      \"OrderNumber\": \"string\",\n      \"OrderDateTime\": \"2019-10-27T00:38:56.555Z\",\n      \"OrderDueDateTime\": \"2019-10-27T00:38:56.555Z\",\n      \"IsPaid\": true,\n      \"Customer\": {\n        \"CustomerId\": 0,\n        \"CustomerName\": \"string\",\n        \"Email\": \"string\",\n        \"PhoneNumber\": \"string\",\n        \"Address1\": \"string\",\n        \"Address2\": \"string\",\n        \"Address3\": \"string\",\n        \"City\": \"string\",\n        \"State\": \"string\",\n        \"ZipCode\": \"string\"\n      },\n      \"CustomerId\": 0,\n      \"CustomerName\": \"string\",\n      \"Email\": \"string\",\n      \"PhoneNumber\": \"string\",\n      \"TableReference\": \"string\",\n      \"TaxAmount\": 0,\n      \"TipAmount\": 0,\n      \"LineItems\": [\n        {\n          \"ExternalItemId\": \"" + itemNum +  "\",\n        \n          \"ItemName\": \"" + itemName + "\",\n          \"Quantity\": 1,\n          \"UnitPrice\": " + itemPrice +  ",\n          \"UnitSellPrice\": " + itemPrice + ",\n          \"ExtendedSellPrice\": " + itemPrice + ",\n          \n          \"Notes\": [\n            \"string\"\n          ],\n          \"BagName\": \"string\"\n        }\n      ],\n      \"Notes\": [\n        \"string\"\n      ],\n      \"KitchenLeadTimeInMinutes\": 0,\n      \"SkipReceipt\": true,\n      \"SkipKitchen\": true\n    }\n  ],\n  \"SourceApplicationName\": \"string\"\n}"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    print(response.text)

@app.route("/")
def input():
    return render_template('input.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/checkoutpage")
def checkoutpage():
    return render_template('checkout.html')


@app.route("/shop")
def about():
    form = ButtonForm()
    return render_template('shop.html', items=itemAPI.createItemDictFromCSV(), form=form, disease=disease, designated=itemAPI.loadModelDict())

@app.route("/addToCart")
def addToCart():
	item_id = request.args.get('item_id')
	cartList.append(int(item_id))
	print(cartList)

	return about()

@app.route("/checkout")
def checkout():
    items = itemAPI.createIDDictFromCSV()
    for item in cartList:
        if item < 28:
            pushOrder(item, items)
    cartList.clear()

    return checkoutpage()

@app.route("/cart")
def cart():
	return render_template('cart.html', items = itemAPI.createIDDictFromCSV(), docs = docAPI.createDocIDDictFromCSV(), cartList = cartList)

@app.route("/doc")
def doc():
    return render_template('doc.html', items=docAPI.createDocDictFromCSV())

	
if __name__ == '__main__':
    app.run(debug=True)




def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
