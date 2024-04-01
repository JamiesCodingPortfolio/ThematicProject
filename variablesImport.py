MONGODBPATH = ''
BOT_TOKEN = ''
ADMINCHANNEL = ''

with open("variables.txt", "r") as file:
    # Read the content of the file
    for line in file:
        
        # Split the content using the first '=' present to separate the variable name and its path/value
        variable_name, value = line.split('=', 1)

        # Removes any whitespace from the value
        value = value.strip()

        # Create the variable dynamically using globals()
        globals()[variable_name.strip()] = value

# Prints each variable in the console for debugging
        
print(MONGODBPATH)
print(BOT_TOKEN)
print(ADMINCHANNEL)