# ChunaLagake_Backend
## Recommender Working

1. Install All the dependencies by running this snippet
```
pip install -r requirements.txt
```
2. Start the backend Flask application by running this code
```
python wsgi.py
```
3. After interaction with the website, the recommender can be used.(Some data on the user is required for it to recommend some items)
   Here we are using the popular [LightFM](https://making.lyst.com/lightfm/docs/home.html) library made by [Maciej Kula](https://github.com/maciejkula)
   Run this command:
   ```
   python chunalagake_recommendation.py
   ```
4. Enter the required fields
   ```
   Model Trained Successfully.....
    _________________STARTING RECOMMENDATION ENGINE_________________



    Enter:
    1 for just training
    2 for recommending on trained model
    3 for training and recommending


   ```
5) 
   -Entering 1 just trains the model on the newly added entries in the database, if added.

   -Entering 2 recommends the user the items on the most recent pretrained model (by default the model is trained on the dataset on start time)
  
   -Entering 3 first trains and then recommends the user items 
