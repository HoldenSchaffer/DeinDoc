# MediLink
### Update! MediLink won 3rd Place at HackGT for Anthem's "Best Healthcare Marketplace" Award
Note: The name of the repository, DeinDoc, comes from our original name for the project, DeinDoc (translates to "Your Doc" in German)

## Use it yourself
To check out MediLink locally, just follow these steps:

1) Clone the github repository or download it to your computer

2) Make sure you have Flask installed

3) run 'python3 deindoc.py'

4) Install any dependencies that might be missing (all dependencies can be founbd n DeinDoc.py)

5) Navigate to localhost:5000, and enjoy!


## What it is:
MediLink was developed as an extention to Anthem's AI powered medical diagnosis system. This system assumes that the user knows their condition, then uses machine learning to generate OTC medicine recommendations for their condition. These recommendations were trained off of a dataset scraped from the internet linking diseases to medicines commonly purchased for treatment. In the future, NCR's Transaction History API can be integrated to add additional features for training. Users can also request Teledoc services from a database of qualified doctors to prescribe other medications. Once medicines / doctorial services are requested, this system integrates NCR's Order API to seamlessly generate and push order requests to the API. Once users begin creating orders, these orders can be fed into the recommendation algorithm to further tailor medical results on a per-user basis.

## Features Include:
AI Powered Marketplace for OTC Medications Neural Network Binary Classification (0, 1) for (hide, recommend). Model training is included in model.py; Data generation is included within generatedata.py. To integrate transaction data (from NCR's Transaction Data API, Order API, or otherwise): label transaction data with either clicked (0, 1) or ordered (0, 1), depending on desired modeling. Can also implement user history for personalized recommendations. Doctor Request System for Teledoc Conferences Integration with NCR Order API for seamless order creation and fulfillment And more!

To watch a quick video we made, click here: https://youtu.be/UeOyAGkNqqM
