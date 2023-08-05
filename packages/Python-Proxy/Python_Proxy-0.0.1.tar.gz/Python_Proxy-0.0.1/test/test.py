# Initialize the dictionary
my_dict = {'test': 'lamaw'}

# Value you are looking for
value = 'lamaw'

# Get the key associated with the value
keys = [k for k, v in my_dict.items() if v == value][0]

# keys now contains all keys that map to 'lamaw'
print(keys)