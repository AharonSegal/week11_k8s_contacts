test_dict = {
    1 : "one",
    2 : "two" 
}

new_dict = {}
if test_dict[1]:
    new_dict["one"] = 1
if 4 in test_dict:
    new_dict["four"] = 4

new_dict += test_dict

print(new_dict)