import random
import streamlit as st
import os
import json
from langchain_community.document_loaders import YoutubeLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from llm_utils import question_data  # Import the function directly

st.title("📚🧠EduQuizer: Youtube Video Quiz Maker")

name = st.text_input("👩‍💼 Enter your name: ")
url = st.text_input("🔗 Enter your video url: ")

process = st.toggle("Submit and Process")

filename = "quize_data.py"

if url:
    # Define the filename you want to check
    # filename = "quize_data.py"

    # Check if the file exists in the current directory
    if os.path.isfile(filename):
        print(f"The file '{filename}' exists in the current directory.")
    else:
        print(f"The file '{filename}' does not exist in the current directory.")

        output = question_data(url) 
        output_file_name = "quize_data.py"

        # Write the output data to the Python file
        with open(output_file_name, "w") as file:
            file.write("output = ")
            json.dump(output, file)

# from quize_data import output

try:
    from quize_data import output
except ModuleNotFoundError:
    # Handle the error gracefully
    st.warning("No quiz data found. Please provide the URL and submit.")
    output = None  # Set output to None or any default value as needed


if process:
    score = 0
    incorrect_answers = []

    with st.form("quiz_form"):
        for i, question_data in enumerate(output, start=1):
            question, correct_answer, incorrect_answer1, incorrect_answer2 = question_data
            
            # Randomize options
            options = [correct_answer, incorrect_answer1, incorrect_answer2]
            random.shuffle(options)
            
            st.write(f"{i}. {question}")

            # for j, option in enumerate(options, start=1):
            #     # Generate a unique key for each checkbox
            #     checkbox_key = f"checkbox_{i}_{j}"
            #     selected_option = st.checkbox(option, key=checkbox_key)

            # st.write("\n")  # Add space between questions

            # # Collect selected options from checkboxes
            # selected_options = [option for option in options if st.checkbox(option, key=checkbox_key)]

            selected_options = [option for option in options if st.checkbox(option)]
            if correct_answer in selected_options and len(selected_options) == 1:
                score += 1
            else:
                incorrect_answers.append(i)
            
            st.session_state[f"selected_options_{i}"] = selected_options

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        st.header("🎉Quiz Summary")
        st.header(f"🎉Score is {score}/{len(output)}")

        for i, question_data in enumerate(output, start=1):
            question, correct_answer, *_ = question_data
            selected_options = st.session_state[f"selected_options_{i}"]
            
            # Determine if the question is correct or incorrect
            if i in incorrect_answers:
                # sign = "❌"
                st.write(f"❌ Question {i}: {question}")    
                st.write(f"Your Answer: {', '.join(selected_options)}")
                st.write(f"Correct Answer: {correct_answer}")
                st.write("\n")
            else:
                # sign = "✔️"
            
                st.write(f"✔️ Question {i}: {question}")
                # st.write(f"Your Answer: {', '.join(selected_options)}")
                # st.write(f"Correct Answer: {correct_answer}")
                st.write("\n")

        
        quiz_data = {
            "name": name,
            "questions": output,
            "score": score
        }

        output_file_name = f"result.json"

        if os.path.exists(output_file_name):
            with open(output_file_name, "r") as file:
                existing_data = json.load(file)
            
            existing_data.append(quiz_data)
            
            with open(output_file_name, "w") as file:
                json.dump(existing_data, file)
        else:
            with open(output_file_name, "w") as file:
                json.dump([quiz_data], file)


        if os.path.exists(filename):
            # Delete the file
            os.remove(filename)
            print(f"{filename} deleted successfully.")
        else:
            print(f"{filename} does not exist.")



# import random
# import streamlit as st
# import os
# import json
# from test2 import question_data  # Import the function directly

# # Set Streamlit page title
# st.title("📚🧠 Youtube Video Quiz Maker")

# # Input fields for name and video URL
# name = st.text_input("👩‍💼 Enter your name:")
# url = st.text_input("🔗 Enter your video URL:")

# # Toggle button to submit and process quiz
# process = st.toggle("Submit and Process")

# # Check if the URL is provided and the process toggle is enabled
# if url and process:
#     # Define the filename for the quiz data
#     filename = "quiz_data.py"
    
#     # Check if the file exists
#     if os.path.isfile(filename):
#         st.info(f"The file '{filename}' already exists.")
#     else:
#         # Generate quiz data and write it to the file
#         output = question_data(url) 
#         output_file_name = "quiz_data.py"
#         with open(output_file_name, "w") as file:
#             file.write("output = ")
#             json.dump(output, file)

# try:
#     from quiz_data import output
# except ModuleNotFoundError:
#     # Handle the error if quiz_data.py doesn't exist
#     st.warning("No quiz data found. Please provide the URL and submit.")
#     output = None

# if process:
#     score = 0
#     incorrect_answers = []

#     with st.form("quiz_form"):
#         for i, question_data in enumerate(output, start=1):
#             question, correct_answer, incorrect_answer1, incorrect_answer2 = question_data
            
#             # Randomize options
#             options = [correct_answer, incorrect_answer1, incorrect_answer2]
#             random.shuffle(options)
            
#             # Display the question
#             st.write(f"{i}. {question}")

#             for j, option in enumerate(options, start=1):
#                 # Generate a unique key for each checkbox
#                 checkbox_key = f"checkbox_{i}_{j}"
#                 selected_option = st.checkbox(option, key=checkbox_key)

#             st.write("\n")  # Add space between questions

#             # Collect selected options from checkboxes
#             selected_options = [option for option in options if st.checkbox(option, key=checkbox_key)]

#             # Evaluate the answer
#             if correct_answer in selected_options and len(selected_options) == 1:
#                 score += 1
#             else:
#                 incorrect_answers.append(i)
            
#             st.session_state[f"selected_options_{i}"] = selected_options

#         # Submit button
#         submit_button = st.form_submit_button("✅ Submit")

#         if submit_button:
#             st.header("🎉 Quiz Summary")
#             st.header(f"🎉 Score is {score}/{len(output)}")

#             # Display quiz summary
#             for i, question_data in enumerate(output, start=1):
#                 question, correct_answer, *_ = question_data
#                 selected_options = st.session_state[f"selected_options_{i}"]
                
#                 # Determine if the question is correct or incorrect
#                 if i in incorrect_answers:
#                     st.write(f"❌ Question {i}: {question}")
#                     st.write(f"Your Answer: {', '.join(selected_options)}")
#                     st.write(f"Correct Answer: {correct_answer}")
#                     st.write("\n")
#                 else:
#                     st.write(f"✔️ Question {i}: {question}")
#                     st.write("\n")

#             # Save quiz data to a JSON file
#             quiz_data = {
#                 "name": name,
#                 "questions": output,
#                 "score": score
#             }
#             output_file_name = f"result.json"
#             if os.path.exists(output_file_name):
#                 with open(output_file_name, "r") as file:
#                     existing_data = json.load(file)
#                 existing_data.append(quiz_data)
#                 with open(output_file_name, "w") as file:
#                     json.dump(existing_data, file)
#             else:
#                 with open(output_file_name, "w") as file:
#                     json.dump([quiz_data], file)

#             # Delete the quiz data file
#             if os.path.exists(filename):
#                 os.remove(filename)
#                 st.info(f"The file '{filename}' has been deleted.")
#             else:
#                 st.warning(f"The file '{filename}' does not exist.")
