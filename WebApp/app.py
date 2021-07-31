import streamlit as st
from streamlit.elements.color_picker import ColorPickerMixin
import function


st.title('Avoid Yourself From Violating The ITE Law on Social Media')
st.text("")
st.text("")
st.text("Before comment in social media. Check your sentence below ")
st.text("")
st.text("")

# inputan user
user_input = st.text_input('Input Sentence')
model = ['LSTM']
selectedModel = st.selectbox('Please Select the Model : ',model)

# tombol
button = st.button('Prediction',key=1)

invalidInput = (len(user_input) <= 3 or
                len(user_input.split(' ')) > 200)

if button==True:
    if invalidInput:
        st.write('Please Input the Correct Sentence')
    else:
        # DISPLAY LOADING PROGRESS FROM 0-20s
        my_bar = st.progress(0)

        function.progressBar(my_bar,0,20)
        
        # load model
        model_path = 'Model/'+selectedModel
        model = function.model(model_path,user_input)

        # DISPLAY LOADING PROGRESS FROM 20-70
        function.progressBar(my_bar,20,70)
        
        # PREDICTION
        predict = model.predict()

        # DISPLAY LOADING PROGRESS FROM 70-100
        function.progressBar(my_bar,70,100)
        
        # DISPLAY PREDICTION
        if predict != 'NEUTRAL':
            st.write('BE CAREFUL. YOUR SENTENCE IS CLASSIFIED AS '+ predict)
        else:
            st.write('YOUR SENTENCE ARE SAFE')