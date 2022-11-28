

def get_recipients(user):
    print("user is :" + str(user))
    user = str(user)
    if user == "nothingbutnet":
        #return ["+17189862989","+17189862991","+19174154012"]
        return ["+17189862989"]
    if user == "superstar":
        return ["+17189862989"]
    if user == "(718) 986-2989":
        return ["+17189862989"]
    return []
