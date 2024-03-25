import pandas as pd


df = pd.read_csv("1st input.csv", )
for index, person in df.iterrows():
    person["phone"] = str(person["phone"]).split(".")[0]
    print(person["phone"])
    # if len(str(((person["zip"])))) == 5 and len(str(((person["ssn"])))) == 4 and len(str(((person["phone"])))) == 10:
    #     zip = str(person["ssn"])
    #     print(len(str((zip))))
    #     print(len(zip))
    #     print("==="*20)   
    # else:
    #     print(person["zip"])
    #     print(len(str(((person["zip"])))))
    #     print(person["ssn"])
    #     print(len(str(((person["ssn"])))))
    #     print(person["phone"])
    #     print(len(str(((person["phone"])))))
    #     print("=======================================================")
        
    
    
    
    
    # dob_prev = person['dob']
    # dob = "/".join([dob_prev.split("/")[1], dob_prev.split("/")[0], dob_prev.split("/")[2]])
    # print(dob_prev)
    # print(dob)
    # print()
