from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pickle

class IntentRecognizer:
    def __init__(self, model_path = 'intent.sav'):
        # Downloading NLTK Corpus
        nltk.download('nps_chat')

        # Setting up Vectorizer
        self.vectorizer = TfidfVectorizer(ngram_range=(1,3), min_df=0.001, max_df=0.7, analyzer='word')
        posts = nltk.corpus.nps_chat.xml_posts()
        posts_text = [post.text for post in posts]
        train_text = posts_text[:int(len(posts_text)*0.8)]
        self.vectorizer.fit_transform(train_text)

        # Loading up Model
        self.intentRecognizer = pickle.load(open(model_path, 'rb'))

    # End of function

    # Function to return the intent in the text
    def recognizeIntent(self, text):
        return self.intentRecognizer.predict(self.vectorizer.transform([text]))
    # End of function

# End of class
