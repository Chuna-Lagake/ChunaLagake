from chuna_lagake.build_recommendation import *

model, interactions, labels, item_features = train_model()

print("_________________STARTING RECOMMENDATION ENGINE_________________\n\n\n")
print("Enter:\n1 for just training\n2 for recommending on trained model\n3 for training and recommending\n")

run = True
while run:
    input_val = int(input())
    if input_val == 1:
        model, interactions, labels, item_features = train_model()
        print("________________________________________________________________")

    elif input_val == 2:
        start([1, 2], model, interactions, labels, item_features)
        print("________________________________________________________________")

    elif input_val == 3:
        model, interactions, labels, item_features = train_model()
        start([1, 2], model, interactions, labels, item_features)
        print("________________________________________________________________")

    elif input_val == 4:
        print("Quitting Recommmendation Engine....")
        run = False
