# Lists used for random string generation in main.py

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
LO_CASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                      'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                      'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                      'z']

UP_CASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                      'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                      'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                      'Z']

# combines all the character arrays above to form one array
COMBINED_LIST = DIGITS + UP_CASE_CHARACTERS + LO_CASE_CHARACTERS