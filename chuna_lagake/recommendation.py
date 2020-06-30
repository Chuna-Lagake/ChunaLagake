from chuna_lagake.build_model import createRecommender
import numpy as np

model, data, labels = createRecommender()

def recommendation_pipeline(model, data, labels, user_ids):
    n_users, n_items = data.shape

    for user_id in user_ids:
        known_positives = labels[data.tocsr()[user_id-1].indices]

        scores = model.predict(user_id-1, np.arange(n_items))

        top_items = labels[np.argsort(-scores)]

        print("User ID: {}".format(user_id))
        print("---Known Positives:")

        for x in known_positives[:3]:
            print("---------{}".format(x))

        print("---Recommended:")
        for x in top_items[:3]:
            print("---------{}".format(x))

def start(user_ids):
    recommendation_pipeline(model, data, labels, user_ids)
