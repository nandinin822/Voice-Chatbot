import streamlit as st
import speech_recognition as sr  # type: ignore
from text2speech import text_to_speech  # Importing the text_to_speech function
import pygame  # type: ignore
from groq_serve import *  #Importing the generate_response function

def play_audio(file_path: str):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        # Wait until the audio finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(2)
    except Exception as e:
        st.error(f"Error playing audio: {e}")
    finally:
        pygame.mixer.quit()

def main():
    st.title("Your Personal Voice Tutor")
    st.write("Enter a topic you want to learn about along with the education level you want to be taught at and generate a personalized tutor tailored to you!")
    st.write("Say 'thank you' to end the conversation.")
    
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = ""

    recognizer = sr.Recognizer()

    def listen_and_process(selected_topic, selected_prompt):
        with sr.Microphone() as source:
            status_placeholder = st.empty()
            recognizer.adjust_for_ambient_noise(source)
            while True:
                status_placeholder.text("Listening...")
                audio = recognizer.listen(source)
                status_placeholder.empty()
                try:
                    user_input = recognizer.recognize_google(audio)
                    st.session_state.conversation.append({"role": "user", "content": user_input})
                    st.write(f"👦User said: {user_input}")

                    # Check for the stop phrase
                    if "thank" in user_input.lower():
                        st.write("Conversation ended.")
                        break

                    # Use the selected prompt to generate the response
                    response = generate_response(selected_topic, selected_prompt, user_input)
                    st.session_state.conversation.append({"role": "assistant", "content": response})
                    st.write(f"🖥️Response: {response}")

                    file = text_to_speech(response)
                    if file:
                        st.write(f"Audio file created: {file}")
                        play_audio(file)
                    else:
                        st.error("Failed to generate audio file.")

                except sr.UnknownValueError:
                    st.write("Sorry, could not understand the audio.")
                except sr.RequestError as e:
                    st.error(f"Could not request results; {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    st.markdown("""
        <style>
        h1{
            color:#000}
        .st-emotion-cache-19rxjzo {
            background-color: rgb(223 230 245 / 72%)!important ;}        
        .custom-box {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
        }
        .st-b7 {
            background-color: rgb(223 230 245 / 72%)!important ;
            color:#000;
            border:none;
        }
        .st-emotion-cache-1qg05tj {
            font-size: 14px;
            color: rgb(0 0 0);
        }


        .st-emotion-cache-19rxjzo {
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 400;
            padding: 10px 15px;
            border-radius: 0.5rem;
            min-height: 38.4px;
            margin: 0px;
            line-height: 1.6;
            color: inherit;
            width: max-content;
            user-select: none;
            background-color: rgb(19, 23, 32);
            border: 1px solid rgba(250, 250, 250, 0.2);
        }
        .custom-button:hover {
            background-color: white;
            color: black;
            border: 2px solid #4CAF50;
        }
         input[placeholder], [placeholder], *[placeholder] {
           color: #000 !important;
        }      
                
        .start-button {
            display: flex;
            justify-content: center;
        }
        .stButton>button {
            background-color: #1961BD !important;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: white;
            color: black;
            border: 2px solid #1961BD;
        }  
        .st-emotion-cache-13k62yr {
            position: absolute;
            background: rgb(255 255 255);
            color: rgb(0 0 0);
            inset: 0px;
            color-scheme: dark;
            overflow: hidden;
        }      
        </style>
        """, unsafe_allow_html=True)
    
    # UI for topic selection

    # st.write("Teach me about...")
    topics = ["Spoken English", "Machine Learning", "Personal Finance", "U.S History"]

    # st.markdown('<div class="custom-box">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("📖 Spoken English", key="Spoken English", help="Learn about Spoken English"):
        st.session_state.selected_topic = "Spoken English"
    if col2.button("💡 Machine Learning", key="machine_learning", help="Learn about Machine Learning"):
        st.session_state.selected_topic = "Machine Learning"
    if col3.button("💰 Personal Finance", key="personal_finance", help="Learn about Personal Finance"):
        st.session_state.selected_topic = "Personal Finance"
    if col4.button("🧾 U.S History", key="us_history", help="Learn about U.S. History"):
        st.session_state.selected_topic = "U.S History"
    # st.markdown('</div>', unsafe_allow_html=True)

    cols=st.columns(2)
    with cols[0]:
        selected_topic = st.text_input("Teach me about...", st.session_state.selected_topic, key="topic_input")

    # Education level selection
    with cols[1]:
        education_levels = ["Beginner", "Intermediate"]
        selected_level = st.selectbox("Select Education Level", education_levels, key="level_select")

    # Prompt creation based on selected level
    beginner_prompt = """
    You are a tutor,  Your task is to guide students through their learning process step by step. Start with basic concepts, providing simple explanations and gradually build up the knowledge. Keep the response short and easy to understand.
    User: {user_input}
    AI: 
    """

    intermediate_prompt = """
    You are a tutor, Your task is to guide students through their learning process step by step. Assume they have some foundational knowledge, and provide more detailed and medium-level explanations. Keep the response concise yet informative.
    User: {user_input}
    AI: 
    """

    selected_prompt = beginner_prompt if selected_level == "Beginner" else intermediate_prompt

    # Start button to initiate voice chat
    # with cols[2]:
    st.markdown('<div class="start-button">', unsafe_allow_html=True)
    if st.button("🔊 Start"):
        greeting = f"Hello, how can I help you learn about {selected_topic}?"
        st.write(f"🖥️Response: {greeting}")

        file = text_to_speech(greeting)
        if file:
            st.write(f"Audio file created: {file}")
            play_audio(file)
        else:
            st.error("Failed to generate audio file.")

        listen_and_process(selected_topic, selected_prompt)
    st.markdown('</div>', unsafe_allow_html=True)

 
if __name__ == "__main__":
    main()
