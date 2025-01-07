# import streamlit as st
# import json
# from access_json import save_json,load_json
# from quize_gen import generate_quiz_questions
# from vid_transcriptor import load_vid_transript
# from langchain_google_genai import ChatGoogleGenerativeAI


# def init_session_state():
#     if 'current_question' not in st.session_state:
#         st.session_state.current_question = 0
#     if 'score' not in st.session_state:
#         st.session_state.score = 0
#     if 'submitted' not in st.session_state:
#         st.session_state.submitted = False
#     if 'user_answers' not in st.session_state:
#         st.session_state.user_answers = {}

# st.title("💡 EduQuizer: Youtube Video Quiz Maker")
# st.subheader("",divider= "rainbow")
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# def main():
    
#     # st.title("Elon Musk Interview Quiz")
#     init_session_state()
#     # questions = load_questions()
#     url = st.text_input("🎥 Enter Youtube video URL ...")
#     btn = st.button("Submit & Proceed")

#     if btn and url:
#         with st.status("🚀  **Loading Quiz Questions...**", state="running", expanded=True) as status:
#             llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
#             docs = load_vid_transript(url)
#             quize_questions = generate_quiz_questions(llm, docs)
#             save_json(quize_questions,"res.json")
#         status.update(label="✅ Quiz is Ready to attempt!",)

#         que = load_json("res.json")
#         questions = que["questions"]
#         if not st.session_state.submitted:
#             question = questions[st.session_state.current_question]
            
#             st.subheader(f"Question {st.session_state.current_question + 1} of {len(questions)}")
#             st.write(question["question"])
            
#             selected_option = st.radio("Select your answer:", question["options"], key=f"q_{st.session_state.current_question}")
#             st.session_state.user_answers[st.session_state.current_question] = selected_option
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.session_state.current_question > 0:
#                     if st.button("Previous"):
#                         st.session_state.current_question -= 1
#                         st.rerun()
            
#             with col2:
#                 if st.session_state.current_question < len(questions) - 1:
#                     if st.button("Next"):
#                         st.session_state.current_question += 1
#                         st.rerun()
#                 elif st.button("Submit Quiz"):
#                     st.session_state.submitted = True
#                     st.rerun()
        
#         else:
#             st.header("Quiz Results")
#             correct_answers = 0
            
#             for i, question in enumerate(questions):
#                 user_answer = st.session_state.user_answers.get(i, "Not answered")
#                 is_correct = user_answer == question["correct_answer"]
#                 if is_correct:
#                     correct_answers += 1
                
#                 st.subheader(f"Question {i + 1}")
#                 st.write(question["question"])
#                 st.write(f"Your answer: {user_answer}")
#                 st.write(f"Correct answer: {question['correct_answer']}")
#                 st.write("✅ Correct" if is_correct else "❌ Incorrect")
#                 st.divider()
            
#             score_percentage = (correct_answers / len(questions)) * 100
#             st.header(f"Final Score: {score_percentage:.1f}%")
            
#             if st.button("Restart Quiz"):
#                 st.session_state.clear()
#                 st.rerun()

# if __name__ == "__main__":
#     main()


import streamlit as st
import json
from access_json import save_json, load_json
from quize_gen import generate_quiz_questions
from vid_transcriptor import load_vid_transript
from langchain_google_genai import ChatGoogleGenerativeAI

def init_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False
    if 'questions' not in st.session_state:
        st.session_state.questions = None
    if 'current_url' not in st.session_state:
        st.session_state.current_url = ""

st.title("💡 EduQuizer: Youtube Video Quiz Maker")
st.subheader(divider="rainbow")

def generate_quiz(url):
    with st.status("🚀 **Loading Quiz Questions...**", state="running", expanded=True) as status:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        docs = load_vid_transript(url)
        quiz_questions = generate_quiz_questions(llm, docs)
        save_json(quiz_questions, "res.json")
        st.session_state.questions = quiz_questions["questions"]
        st.session_state.quiz_generated = True
        st.session_state.current_url = url
    status.update(label="✅ Quiz is Ready to attempt!")

def display_quiz():
    if not st.session_state.submitted:
        question = st.session_state.questions[st.session_state.current_question]
        
        st.subheader(f"Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}")
        st.write(question["question"])
        
        selected_option = st.radio(
            "Select your answer:", 
            question["options"], 
            key=f"q_{st.session_state.current_question}"
        )
        st.session_state.user_answers[st.session_state.current_question] = selected_option
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.current_question > 0:
                if st.button("Previous"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if st.session_state.current_question < len(st.session_state.questions) - 1:
                if st.button("Next"):
                    st.session_state.current_question += 1
                    st.rerun()
            elif st.button("Submit Quiz"):
                st.session_state.submitted = True
                st.rerun()

def display_results():
    st.header("Quiz Results")
    correct_answers = 0
    
    for i, question in enumerate(st.session_state.questions):
        user_answer = st.session_state.user_answers.get(i, "Not answered")
        is_correct = user_answer == question["correct_answer"]
        if is_correct:
            correct_answers += 1
        
        st.subheader(f"Question {i + 1}")
        st.write(question["question"])
        st.write(f"Your answer: {user_answer}")
        st.write(f"Correct answer: {question['correct_answer']}")
        st.write("✅ Correct" if is_correct else "❌ Incorrect")
        st.divider()
    
    score_percentage = (correct_answers / len(st.session_state.questions)) * 100
    st.header(f"Final Score: {score_percentage:.1f}%")
    
    if st.button("Try Another Video"):
        st.session_state.clear()
        st.rerun()

def main():
    init_session_state()
    
    # Always show URL input
    url = st.text_input("🎥 Enter Youtube video URL ...", 
                       value=st.session_state.current_url)
    
    if not st.session_state.quiz_generated:
        if st.button("Generate Quiz") and url:
            generate_quiz(url)
            st.rerun()
    else:
        st.write("📺 Currently viewing quiz for video:", st.session_state.current_url)
        if st.button("Generate New Quiz"):
            if url != st.session_state.current_url:
                generate_quiz(url)
                st.session_state.submitted = False
                st.session_state.current_question = 0
                st.session_state.user_answers = {}
                st.rerun()
            
        st.divider()
        
        if st.session_state.submitted:
            display_results()
        else:
            display_quiz()

if __name__ == "__main__":
    main()