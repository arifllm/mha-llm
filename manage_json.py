import json

def load_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_data(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def get_user_chat_history(key, new_msg):
    file_path = 'data.json'
    data = load_data(file_path)

    history = []
    user_data = data.get(key, None)
    if user_data: 
        if len(user_data) >= 15:
            user_data.pop(0)
        history = user_data
        data[key].append(new_msg)
    else:
        data[key] = [] 
        data[key].append(new_msg)
    
    save_data(file_path=file_path, data=data)
    print(key, ' - chat_history : ', history)

    return history


    
