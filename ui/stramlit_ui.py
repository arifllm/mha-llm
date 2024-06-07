import streamlit as st
from streamlit_chat import message

def api_calling(prompt):
	return "WIP"
def clear_chat():
    # Clear chat history
    st.session_state['user_input'] = []
    st.session_state['openai_response'] = []

st.title("SoulCanvas")
header_col, button_col = st.columns([3, 1])
header_col.subheader("I'm here for you :) ")
new_session_button = button_col.button("New Session", type="primary", on_click=clear_chat, key="new_session")

if 'user_input' not in st.session_state:
	st.session_state['user_input'] = []

if 'openai_response' not in st.session_state:
	st.session_state['openai_response'] = []

def get_text():
	input_text = st.chat_input("How may I help you...", key="input")
	print(input_text)
	return input_text

user_input = get_text()

if user_input:
	output = api_calling(user_input)
	output = output.lstrip("\n")

	# Store the output
	st.session_state.openai_response.append(user_input)
	st.session_state.user_input.append(output)

message_history = st.empty()

print("session state: ", st.session_state)
if st.session_state['user_input']:
	# for i in range(len(st.session_state['user_input']) - 1, -1, -1):
	for i in range(0, len(st.session_state['user_input'])):
		
		# This function displays OpenAI response
		message(st.session_state['user_input'][i], 
				avatar_style="initials",seed = 'Shraddha Londhe',is_user=True,
				key=str(i) + 'data_by_user')
		
		# This function displays user input
		message(st.session_state["openai_response"][i], 
				key=str(i),avatar_style="initials", seed="SC")
