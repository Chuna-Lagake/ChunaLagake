from chuna_lagake.models import Menu, User, Ratings
from lightfm import LightFM
from lightfm.data import Dataset
import numpy as np
import os, csv, json
from itertools import islice

menu, users, items, ratings, user_recommend = [], [], [], [], []

paan_features = ['Banaras','Calcutta','Maghai','Sada','Meetha','Chocolate','Dry Fruit','Mango','Strawberry','Pineapple','Gold',
 'Kaju','Jelly','Rose','Shahi','Kesar','Vanilla','Masala','Khatta','Orange','White','Silver','RaatRani','Nutella','Special']

for i in range(Menu.query.count()):
    menu_item = Menu.query.filter_by(id='{}'.format(i+1)).first()
    menu.append([menu_item.id, menu_item.name, menu_item.features])

def get_data():
    # user data
    for i in range(User.query.count()):
        user_dict = {}
        user_data = User.query.filter_by(id='{}'.format(i+1)).first()
        user_dict.update({"User_ID":user_data.id, "username":user_data.username})
        users.append(user_dict)

    # item data
    for item in menu:
        item_dict = {}
        item_dict.update({"Item_ID":item[0], "Item_Name":item[1]})
        for i in range(25):
            item_dict.update({paan_features[i]:item[2][i]})
        items.append(item_dict)

    # Rating Data
    user_flag = 0
    for i in range(Ratings.query.count()):
        rating_dict = {}
        rating = Ratings.query.filter_by(id='{}'.format(i+1)).first()
        rating_dict.update({"User_ID":rating.user_id, "Item_ID":rating.item_id, "Rating":rating.rating})
        if rating.user_id not in user_recommend:
            user_recommend.append(rating.user_id)
            rating_dict.update({"Recommend_ID":user_flag})
            user_flag += 1
        else:
            rating_dict.update({"Recommend_ID":user_recommend.index(rating.user_id)})
        ratings.append(rating_dict)
    print('user_recommend:',user_recommend)
    return users, items, ratings

def get_user_features():
    return get_data()[0]

def get_item_features():
    return get_data()[1]

def get_ratings():
    return  get_data()[2]

user_features, item_features_names, ratings = get_data()

def add_item_features(dataset, feature):
    dataset.fit_partial(items=(x['Item_ID'] for x in get_item_features()),
                    item_features=(x[feature] for x in get_item_features()))



def train_model():
    dataset = Dataset()
    dataset.fit((x['User_ID'] for x in get_ratings()),
                (x['Item_ID'] for x in get_ratings()))
    for i in range(25):
        add_item_features(dataset, paan_features[i])
    (interactions, weights) = dataset.build_interactions(((x['User_ID'], x['Item_ID'])
                                                          for x in get_ratings()))

    item_features = dataset.build_item_features(((x['Item_ID'], [x['Banaras'], x['Calcutta'], x['Maghai'], x['Sada'],
                                                x['Meetha'], x['Chocolate'], x['Dry Fruit'], x['Mango'], x['Strawberry'],
                                                x['Pineapple'], x['Kaju'], x['Jelly'], x['Rose'], x['Shahi'], x['Kesar'],
                                                x['Vanilla'], x['Masala'], x['Khatta'], x['Orange'], x['White'], x['Silver'],
                                                x['RaatRani'], x['Nutella'], x['Special'], x['Gold']])
                                                  for x in get_item_features()))

    model = LightFM(loss='bpr')
    model.fit(interactions, item_features=item_features)

    labels = np.array([x['Item_ID'] for x in get_item_features()])
    print("Model Trained Successfully.....")
    return model, interactions, labels, item_features

def sample_recommendation(model, data, labels, item_features, user_id):
    n_users, n_items = data.shape
    list_of_recommendations = []
    scores = model.predict(user_id, np.arange(n_items), item_features)
    top_items = labels[np.argsort(-scores)]

    for x in top_items[:5]:
        list_of_recommendations.append(x)
    print('user_id:',user_id)
    print('list_of_recommendations:', list_of_recommendations)
    print('_____________________________')
    return list_of_recommendations


def convert_to_user_recommend(model, interactions, labels, item_features, user_id):
    new_user_id = user_recommend.index(user_id)
    list_of_recommendations = sample_recommendation(model, interactions, labels, item_features, new_user_id)
    return list_of_recommendations

def start(user_ids, model, interactions, labels, item_features):
    # model, interactions, labels, item_features = train_model()
    convert_to_user_recommend(model, interactions, labels, item_features, user_ids)
