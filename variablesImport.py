MONGODBPATH = ''
BOT_TOKEN = ''

with open("variables.txt", "r") as file:
        # Read the content of the file
    #content = file.read()
    for item in file:
        
        # Split the content by '=' to separate the variable name and its value
        variable_name, value = item.split('=', 1)

        # Remove any leading or trailing whitespace from the value
        value = value.strip()

        # Create the variable dynamically using globals()
        globals()[variable_name.strip()] = value

        # Test the variable
print(MONGODBPATH)
print(BOT_TOKEN)