import tensorflow as tf
import pandas as pd
import numpy as np
import re
import string
import time


class model:
    def __init__(self, model_file, text):
        self.model = tf.keras.models.load_model(model_file)
        self.text = text
    def preprocessing(self):
        text = self.text
        def clean_text(text):
            #will replace the html characters with " "
            text=re.sub('<.*?>', ' ', text)  
            #To remove the punctuations
            text = text.translate(str.maketrans(' ',' ',string.punctuation))
            #will consider only alphabets and numerics
            text = re.sub('[^a-zA-Z]',' ',text)  
            #will replace newline with space
            text = re.sub("\n"," ",text)
            #will convert to lower case
            text = text.lower()
            # will replace a word
            text = re.sub("(username|user|url|rt|xf|fx|xe|xa)\s|\s(user|url|rt|xf|fx|xe|xa)","",text)
            # will replace single word
            text = re.sub(r"\b[a-zA-Z]\b","",text)
            # will repalce repated char
            text = re.sub(r'[^\w\s]|(.)(?=\1)', '', text)
            # will join the words
            text=' '.join(text.split())
            return text

        def applyKamusAlayandStopWord(text):
            # load dicionary
            kamusAlay = pd.read_csv('https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv')
            stopWord = pd.read_csv('https://raw.githubusercontent.com/datascienceid/stopwords-bahasa-indonesia/master/stopwords_id_satya.txt', header = None)
            stopWord = stopWord[0].to_list()

            url='https://drive.google.com/file/d/1TxCnZewbG_3BwJ2ywjRMIxNl8zMpy2Ng/view?usp=sharing'
            url2='https://drive.google.com/uc?id=' + url.split('/')[-2]
            kamusTambahan = pd.read_csv(url2)

            # split
            text = text.split(' ')
            # apply kamusAlay
            temp=[]
            for i in range(len(text)):

                try:
                    # kamus alay
                    index = kamusAlay.index[kamusAlay['slang'] == text[i]][0]
                    text[i] = kamusAlay['formal'][index]
                    # stop word
                except:
                    pass

                try:
                    # kamus alay
                    index = kamusTambahan.index[kamusTambahan['kataAlay'] == text[i]][0]
                    text[i] = kamusTambahan['kataBaik'][index]
                    # stop word
                except:
                    pass

                try:
                    if text[i] in stopWord:
                        text.remove(text[i])
                except:
                    pass

                
            text = ' '.join(text)
            return text
        
        text = clean_text(self.text) # clean text
        text = applyKamusAlayandStopWord(text) # repalce kata alay
        return text

    def predict(self):
        className = {
            0 : 'NEUTRAL',
            1 : 'HOAX',
            2 : 'HATE SPEECH',
            3 : 'OFFENSIVE'
        }
        text = self.preprocessing()
        text = [text]
        return className[np.argmax(self.model.predict(text))]

def progressBar(my_bar,start,end):
    for percent_complete in range(start,end):
        time.sleep(0.1)
            
        my_bar.progress(percent_complete + 1)