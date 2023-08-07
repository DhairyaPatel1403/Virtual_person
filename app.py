import openai
from gtts import gTTS
import pygame
import speech_recognition as sr
import pyttsx3
import streamlit as st
import base64
from datetime import datetime
from PIL import Image

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def main_func():
    language='en'

    role = st.text_input("Who do you want to talk to: (student / teacher / friend / coding mentor / travel guide / philosopher)")


    message_dict = {
                    "student":"You are a student, act like a student to any subject the user is teaching you and reply accordingly.",
                    "teacher":"You are a teacher, user will ask you things, you have to teach user the things he want to.",
                    "friend":"You are a friend of user, user will say random things friends say to each other, just entertain the user.",
                    "coding mentor":"You are a coding mentor, you will receive errors, will be asked suggestions about various programming languages. Answer accordingly",
                    "travel guide":"You are a travel guide, you will be asked things about various tourism places, answer them accordingly in a single paragraph].",
                    "philosopher":"You are a philosopher, give philosophical answers to the user.",
    }
    if(role=="student"):
        messages=[{"role" : "system", "content":message_dict["student"]}]
    elif(role=="teacher"):
        messages=[{"role" : "system", "content":message_dict["teacher"]}]
    elif(role=="friend"):
        messages=[{"role" : "system", "content":message_dict["friend"]}]
    elif(role=="coding mentor"):
        messages=[{"role" : "system", "content":message_dict["coding mentor"]}]
    elif(role=="travel guide"):
        messages=[{"role" : "system", "content":message_dict["travel guide"]}]
    elif(role=="philosopher"):
        messages=[{"role" : "system", "content":message_dict["philosopher"]}]
    else:
        messages=[{"role" : "system", "content":"You are a personal virtual assistant."}]



    openai.api_key = "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"

    r = sr.Recognizer()



    while True:
        with sr.Microphone() as source2:

            current_datetime = datetime.now()

            date_time_string = current_datetime.strftime("%Y%m%d%H%M%S")

            r.adjust_for_ambient_noise(source2, duration=0.2)

            try:
                
                #listens for the user's input
                audio2 = r.listen(source2)
                
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
    
                st.write("Did you say ",MyText)

                if MyText.lower() == "stop":
                    st.stop()

            except sr.UnknownValueError:
                continue

            except sr.RequestError as e:
                st.warning(f"Could not request results from Google Web Speech API; {e}")
                continue

        message = MyText
    
        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        
        reply = chat.choices[0].message.content
        reply_list = reply.split("\n")

        reply_list = [item.strip() for item in reply_list if item.strip()]

        col1, col2 = st.columns([1, 1])

        if reply_list:
            item = reply_list[0]  # Get the first response
            # this is the text to convert
            myobj = gTTS(text=item, lang=language, slow=False)
            file_name = f"text{date_time_string}.mp3"
            myobj.save(file_name)
            with st.container():
                with col1:
                    st.write(f"Playing {file_name}. (Say stop to terminate the conversation.)")
                    autoplay_audio(file_name)
                with col2:
                    logo_image = add_logo(logo_path="robot.png", width=50, height=60)
                    st.image(logo_image)




        messages.append({"role": "assistant", "content": reply})

if __name__=="__main__":
    st.title("Virtual Buddy :))")

    main_func()
    