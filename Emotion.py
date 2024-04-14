from nltk.tokenize import word_tokenize
import string, re, pickle
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

with open('emotion_classifier.pickle', 'rb') as file:
    classifier = pickle.load(file)
    
def remove_noise(tokens, stop_words = ()):

    stop_words = stopwords.words('english')
    cleaned_tokens = []

    for token, tag in pos_tag(tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                    '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def classify_emotion(input:str) -> str:
    custom_tokens = remove_noise(word_tokenize(input))
    return classifier.classify(dict([token, True] for token in custom_tokens))