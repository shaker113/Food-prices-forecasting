import pickle
import json
import pandas as pd
import numpy as np

with open('xgboost model.pkl', 'rb') as file:
    xgboost_model = pickle.load(file)
with open('market model.pkl', 'rb') as file:
    market_model = pickle.load(file)
with open('commoditys_encoded.pkl', 'rb') as lst:
    commoditys = pickle.load(lst)
with open('categorys_encoded.pkl', 'rb') as lst:
    categorys = pickle.load(lst)
with open('market_encoded.pkl', 'rb') as lst:
    markets = pickle.load(lst)
with open('cat_com.json', 'r') as di:
    cat_com = json.load(di)

def display_menu():
    print("\n\nWelcome to Food Price predictor!")
    print("1. predict average price of all markets")
    print("2. Exit")

def get_choice():
    choice = input("Please enter your choice number: ")
    return choice

def try_ex(arr,ind):
    try:
        if int(ind) <= 0:
            arr['-']
        arr[int(ind)-1]
    except:
        print("\nInvalid choice. Please try again.")
        return False
    return True

def predict_average():
    print("\nplease insert these info:")

    print("\nwhat is the category of food?\n")
    for i in range(len(categorys)):
        print(i+1,". ",categorys[i])
    choice = 0
    while True:
        choice = get_choice()
        if try_ex(categorys,choice):
            break
    category_choice = categorys[int(choice)-1]
    # print(category_choice)

    print("\nwhat is the commodity of food?\n")
    for i in range(len(cat_com[category_choice])):
        print(i+1,". ",cat_com[category_choice][i])
    choice = 0
    while True:
        choice = get_choice()
        if try_ex(cat_com[category_choice],choice):
            break
    commodity_choice = cat_com[category_choice][int(choice)-1]

    
    print("\nwhat is the year do you want to predict?\n")
    choice = 0
    while True:
        try:
            choice = int(input("Please enter the number: "))
        except:
            choice = 0
        if choice < 2012 or choice > 2030:
            print("\nInvalid. Please try again.")
            continue
        else:
            break
    year_choice = choice

    print("\nwhat is the month do you want to predict (number)?\n")
    choice = 0
    while True:
        try:
            choice = int(input("Please enter the number: "))
        except:
            choice = 0
        if choice < 1 or choice > 12:
            print("\nInvalid. Please try again.")
            continue
        else:
            break
    month_choice = choice

    print("\nis this month in ramdan?\n")
    print("1. Yes")
    print("2. No")
    choice = 0
    while True:
        try:
            choice = get_choice()
            choice = int(choice)
        except:
            choice = 0
        if choice != 1 and choice != 2:
            print("\nInvalid choice. Please try again.")
            continue
        else:
            break
    ramadan_choice = choice

    print("\nwhat is the number of population (number)?\n")
    choice = 0
    while True:
        try:
            choice = int(input("Please enter the number: "))
        except:
            choice = 0
        if choice < 7000000 or choice > 20000000:
            print("\nInvalid. Please try again.")
            continue
        else:
            break
    population_choice = choice

    print("\nwhat is the number of middle east war deaths (number)?\n")
    choice = 0
    while True:
        try:
            choice = int(input("Please enter the number: "))
        except:
            choice = -1
        if choice < 0:
            print("\nInvalid. Please try again.")
            continue
        else:
            break
    middle_east_choice = choice

    print("\nwhat is the number of world war deaths (number)?\n")
    choice = 0
    while True:
        try:
            choice = int(input("Please enter the number: "))
        except:
            choice = -1
        if choice < 0:
            print("\nInvalid. Please try again.")
            continue
        else:
            break
    world_choice = choice

    print("\nwhat is the number of corona new cases in jordan (number)?\n")
    choice = 0
    while True:
        try:
            choice = int(input("Please enter the number: "))
        except:
            choice = -1
        if choice < 0:
            print("\nInvalid. Please try again.")
            continue
        else:
            break
    jor_new_cases_choice = choice

    print("\nwhat is the number of corona new deaths in jordan (number)?\n")
    choice = 0
    while True:
        try:
            choice = int(input("Please enter the number: "))
        except:
            choice = -1
        if choice < 0:
            print("\nInvalid. Please try again.")
            continue
        else:
            break
    jor_new_deaths_choice = choice



    input_list = [[categorys.index(category_choice),
                   commoditys.index(commodity_choice),
                   month_choice,
                   year_choice,
                   ramadan_choice,
                   population_choice,
                   middle_east_choice,
                   world_choice,
                   jor_new_cases_choice,
                   jor_new_deaths_choice]]
    
    price_pred = xgboost_model.predict(input_list)
    print("\n\nBased on your answers the predicted price is: ",price_pred[0]," JD\n\n")

    print("\nDo you want to predict market price?")
    print("1. Yes")
    print("2. No")
    choice = 0
    while True:
        try:
            choice = get_choice()
            choice = int(choice)
        except:
            choice = 0
        if choice != 1 and choice != 2:
            print("\nInvalid choice. Please try again.")
            continue
        else:
            break

    if choice == 1:
        print("\nPlease Select the market: ")

        for i in range(len(markets)):
            print(i+1,". ",markets[i])
        print(len(markets)+1,". All markets")
        choice = 0
        while True:
            choice = get_choice()
            if choice == str(len(markets)+1):
                for mark in range(len(markets)):
                    input_list = [[ commoditys.index(commodity_choice),
                                    month_choice,
                                    year_choice,
                                    price_pred[0],
                                    mark]]
                    df = pd.DataFrame(input_list, columns = ['commodity','month','year','price_x','market'])
                    market_price_pred = market_model.predict(df)
                    print("\nBased on your answers the predicted price of ",markets[mark], " is: ",market_price_pred[0]," JD\n")
                break
            else:
                if try_ex(markets,choice):
                    break
        if choice != str(len(markets)+1):
            markets_choice = markets[int(choice)-1]
            input_list = [[ commoditys.index(commodity_choice),
                                    month_choice,
                                    year_choice,
                                    price_pred[0],
                                    int(choice)-1]]
            df = pd.DataFrame(input_list, columns = ['commodity','month','year','price_x','market'])
            market_price_pred = market_model.predict(df)
            print("\nBased on your answers the predicted price of ",markets_choice, " is: ",market_price_pred[0]," JD\n")



def main():
    while True:
        display_menu()
        choice = get_choice()

        if choice == "1":
            predict_average()
        elif choice == "2":
            print("\nThank You for using our program!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == '__main__':
    main()