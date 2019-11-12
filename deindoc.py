from flask import Flask, render_template, url_for, flash, redirect, request
import itemAPI
import docAPI
from forms import ButtonForm
import json
import requests
import http.client
app = Flask(__name__)

cartList = []
currDisease = ['Asthma']
diseaseList = ['Asthma', 'Shingles', 'flu', 'Stomach Virus', 'Strep Throat']

url = "https://api-reg-apigee.ncrsilverlab.com/v2/orders"
token = "Bearer gAAAAJt_ACGPI2BPB_NihIjIzM08X50_CpVMAj1XXsdAzRBDH1h6bDdHypqCjVIePfif2UcYIA3PlhK_gPYDcbOkFGJ_ie9Gzpt0aV2-uiBo-8tfuc7dB7LkWc28tJv-yPvktSezfJkY8TyOf7RB0ng88rE-EMpy0atrDycC9cheNgoQ9AAAAIAAAACaTmS2HpwW6LSjQ1UbjEWZhHFPS7yen5b2J1izo1-3W0Tb7ZTt1-Xur2tHFgmE9Uv0Gw7JrazNOzmzjDy9fJwHsRY7VGKTwKzl4Uxxz7hwoYAJCEFyfRAVCA9GXuEunOHN2vBbxO42BXp1u4cIbpLSiE_B27r9YXEIcQ39Z3hZNpFhHsPNJ0DfjbtOw6_V3U2rZB6ZI5YN-yr6PmEsGiBfN5g5IgjHiP7yc2LLj7YqQFtN02s1j4NU9Ma1tgYwkBGMuuylgrL4tTpx0wZP8qs0CZA69k5RDgAC5jGxkf--9ZgeyIaPq5A2ft8geN09y8g"
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
    return render_template('home.html',diseaseList=diseaseList)


@app.route("/shop")
def shop():
    form = ButtonForm()
    return render_template('shop.html', items=itemAPI.createItemDictFromCSV(), form=form, disease = currDisease[len(currDisease) -  1], designated=itemAPI.loadModelDict())

@app.route("/diseasePlaceholder")
def diseasePlaceholder():
    disease = request.args.get('disease')
    currDisease.append(disease)
    return shop()

@app.route("/addToCart")
def addToCart():
	item_id = request.args.get('item_id')
	cartList.append(int(item_id))
	print(cartList)

	return shop()

@app.route("/checkoutpage")
def checkoutpage():
    return render_template('checkout.html')


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
	return render_template('cart.html', items = itemAPI.createIDDictFromCSV(), docs = docAPI.createDocIDDictFromCSV(),cartList = cartList)

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
