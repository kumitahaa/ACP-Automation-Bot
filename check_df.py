import pandas as pd


df = pd.read_csv("input.csv", )
for index, person in df.iterrows():
    dob = str(person["dob"])
    try:
        dob = "/".join([dob.split("/")[1], dob.split("/")[0], dob.split("/")[2]])
        print("DOB with / separater...")
    except:
        print("DOB with - separater, sending directly...")
    print(dob)
    print("DOB entered.")
    
    
    
    
    
    # dob_prev = person['dob']
    # dob = "/".join([dob_prev.split("/")[1], dob_prev.split("/")[0], dob_prev.split("/")[2]])
    # print(dob_prev)
    # print(dob)
    # print()
