import streamlit as st
import json

def init_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

def load_questions():
    questions = [
        {
            "question": "What is the primary goal of Elon Musk's Boring Company?",
            "options": [
                "To develop high-speed, above-ground transportation systems.",
                "To alleviate traffic congestion through a 3D network of tunnels.",
                "To create a global network of underground hyperloops."
            ],
            "correct_answer": "To alleviate traffic congestion through a 3D network of tunnels."
        },
        {
            "question": "How does Elon Musk plan to significantly reduce the cost of tunnel construction?",
            "options": [
                "By using robots to automate the entire process.",
                "By reducing tunnel diameter and implementing continuous tunneling and reinforcing.",
                "By developing new, stronger materials for tunnel walls."
            ],
            "correct_answer": "By reducing tunnel diameter and implementing continuous tunneling and reinforcing."
        },
        {
            "question": "What is Elon Musk's proposed speed for the vehicles in his tunnel network?",
            "options": [
                "100 kilometers per hour (62 mph)",
                "200 kilometers per hour (130 mph)",
                "300 kilometers per hour (186 mph)"
            ],
            "correct_answer": "200 kilometers per hour (130 mph)"
        },
        {
            "question": "Why does Elon Musk believe that flying cars are not a viable solution to traffic congestion?",
            "options": [
                "They are too expensive to produce and maintain.",
                "They would be noisy, generate high wind forces, and cause anxiety.",
                "They require too much airspace and would cause significant air pollution."
            ],
            "correct_answer": "They would be noisy, generate high wind forces, and cause anxiety."
        },
        {
            "question": "What is the current status of Tesla's Full Self-Driving (FSD) capability, according to Elon Musk?",
            "options": [
                "FSD is fully operational and available for all Tesla models.",
                "FSD is expected to achieve cross-country autonomous driving by the end of 2017.",
                "FSD is still under development and will not be ready for several years."
            ],
            "correct_answer": "FSD is expected to achieve cross-country autonomous driving by the end of 2017."
        }
    ]
    return questions

def main():
    st.title("Elon Musk Interview Quiz")
    init_session_state()
    questions = load_questions()
    
    if not st.session_state.submitted:
        question = questions[st.session_state.current_question]
        
        st.subheader(f"Question {st.session_state.current_question + 1} of {len(questions)}")
        st.write(question["question"])
        
        selected_option = st.radio("Select your answer:", question["options"], key=f"q_{st.session_state.current_question}")
        st.session_state.user_answers[st.session_state.current_question] = selected_option
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.current_question > 0:
                if st.button("Previous"):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if st.session_state.current_question < len(questions) - 1:
                if st.button("Next"):
                    st.session_state.current_question += 1
                    st.rerun()
            elif st.button("Submit Quiz"):
                st.session_state.submitted = True
                st.rerun()
    
    else:
        st.header("Quiz Results")
        correct_answers = 0
        
        for i, question in enumerate(questions):
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
        
        score_percentage = (correct_answers / len(questions)) * 100
        st.header(f"Final Score: {score_percentage:.1f}%")
        
        if st.button("Restart Quiz"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()