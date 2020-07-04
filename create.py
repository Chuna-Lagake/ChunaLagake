import pandas as pd
from chuna_lagake import db
from chuna_lagake.models import Menu
features = pd.read_excel('encoded_features.xlsx')
for i in range(len(features)):
    row = features.loc[i]

    item = Menu( name = row.names, description = row.desciption, _features = row.features)
    db.session.add(item)
    db.session.commit()
