from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB


class IntentClassifier:
    def __init__(self, dataset):
        self.vectorizer = CountVectorizer()
        self.classifier = GaussianNB()
    
        self.fit(dataset)

    def fit(self, dataset):
        x_train = self.vectorizer.fit_transform(dataset.x_train).toarray()
        self.replies = dataset.replies

        self.classifier.fit(x_train, dataset.y_train)

    def predict(self, context):
        x_input  = self.vectorizer.transform([f"{context}."]).toarray()
        y_output = self.classifier.predict(x_input)[0]

        return y_output
