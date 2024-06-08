import json
import string    
import random # define the random module  

def load_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_data(file_path, data):
    """Save JSON data to a file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def get_user_chat_history(key, question_id, question):
    file_path = 'data.json'
    data = load_data(file_path)

    history_tuple_list =[]
    user_data = data.get(key, None)
    if user_data: 
        if len(user_data) >= 15:
            user_data.pop(0)
        for his in user_data:
            print(his)
            history_tuple_list.append((his["question"], his["answer"]))

        data[key].append({"question_id": question_id, "question": question, "answer": ""})
    else:
        data[key] = [] 
        data[key].append({"question_id": question_id, "question": question, "answer": ""})
    
    save_data(file_path=file_path, data=data)
    print(key, ' - chat_history : ', history_tuple_list)

    return history_tuple_list

def generate_random_id():
    S = 18  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    return str(ran)

def update_answer(key, question_id, answer):
    file_path = 'data.json'
    data = load_data(file_path)

    user_data = data.get(key, None)

    if user_data:
        user_final_data = []
        for his in user_data:
            if his['question_id'] == question_id:
                his['answer'] = answer
                user_final_data.append(his)
            else:
                user_final_data.append(his)

        data[key] = user_final_data
    else:
        print("question_id not found")

    save_data(file_path=file_path, data=data)

