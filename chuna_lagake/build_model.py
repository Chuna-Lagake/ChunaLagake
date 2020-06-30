### Recommendation hygiene

from chuna_lagake.models import User, Menu, Ratings
from lightfm import LightFM
from lightfm.data import Dataset
import numpy as np



menu = []
items = []
users = []
ratings = []

item_features = ['Banaras','Calcutta','Maghai','Sada','Meetha','Chocolate','Dry Fruit','Mango','Strawberry','Pineapple','Gold',
 'Kaju','Jelly','Rose','Shahi','Kesar','Vanilla','Masala','Khatta','Orange','White','Silver','RaatRani','Nutella','Special']

# get data from database
def getData():
    for i in range(Menu.query.count()):
        item = Menu.query.filter_by(id='{}'.format(i+1)).first()
        menu.append([item.id, item.name, item.features])
    for i in range(User.query.count()):
        user_dict = {}
        User_Data = User.query.filter_by(id='{}'.format(i+1)).first()
        user_dict.update({"User_ID":User_Data.id, "Name":User_Data.username})
        users.append(user_dict)
    for i in range(Ratings.query.count()):
        rating_dict = {}
        Rating = Ratings.query.filter_by(id='{}'.format(i+1)).first()
        rating_dict.update({"User_ID":Rating.user_id,"Item_ID":Rating.item_id, "Rating":Rating.rating})
        ratings.append(rating_dict)
    for item in menu:
        item_dict = {}
        item_dict.update({"Name":item[1], "Item_ID":item[0]})
        for i in range(25):
            item_dict.update({item_features[i]:item[2][i]})
        items.append(item_dict)
    return menu, users, items, ratings

def add_item_features(dataset, feature):
    dataset.fit_partial(items=(x['Item_ID'] for x in items),
                        item_features=(x[feature] for x in items))

# Not Complete
def add_user_features(dataset, feature):
    dataset.fit_partial(users=(x['User_ID'] for x in users),
                        user_features=(x[feature] for x in users))

def createModel(users, items, ratings):
    dataset = Dataset()
    dataset.fit((x['User_ID'] for x in ratings),
                (x['Item_ID'] for x in ratings))

    num_users, num_items = dataset.interactions_shape()
    print("Num Users: {}, Num Items: {}".format(num_users, num_items))

    dataset.fit_partial(items=(x['Item_ID'] for x in items),
                       users=(x['User_ID'] for x in users))

    for feature in item_features:
        add_item_features(dataset, feature)

    return dataset

def build_model(dataset, users, items, ratings):
    (interactions, weights) = dataset.build_interactions(((x['User_ID'], x['Item_ID']) for x in ratings))

    item_features = dataset.build_item_features(((x['Item_ID'],[x['Banaras'], x['Calcutta'], x['Maghai'], x['Sada'],
                                                  x['Meetha'], x['Chocolate'], x['Dry Fruit'], x['Mango'], x['Strawberry'],
                                                  x['Pineapple'], x['Gold'], x['Kaju'], x['Jelly'], x['Rose'], x['Shahi'],
                                                  x['Kesar'], x['Vanilla'], x['Masala'], x['Khatta'], x['Orange'], x['White'],
                                                  x['Silver'], x['Nutella'], x['RaatRani'], x['Special']]) for x in items))

    return interactions, item_features
        # '''Uncomment the below line and fill appropriately'''

    # else:
    #     # user_features = dataset.build_user_features(((x['User_ID'], ['''User Features as a list here''']) for x in users))
    #     return interactions, item_features, user_features


def makeModel(interactions, item_features):     # add user_features here if existing
    model = LightFM(loss='warp')
    model.fit(interactions, item_features)      # add user_features as an attribute here if existing
    return model

def createRecommender():
    menu, users, items, ratings = getData()
    dataset = createModel(users, items, ratings)
    interactions, item_features = build_model(dataset, users, items, ratings)
    labels = np.array([x['Name'] for x in items])
    model = makeModel(interactions, item_features)
    return model, interactions, labels

if __name__ == '__main__':
    createRecommender()
