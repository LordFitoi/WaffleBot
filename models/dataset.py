class Dataset:
    def __init__(self, corpus):
        self.x_train = ["."]
        self.y_train = ["NoContext"]
        self.replies = dict()
        self.patterns = dict()

        self.create(corpus)

    def add_pattern(self, intent, sample):
        if sample[0] == "$":
            pattern = sample[1:].lower()

            if intent not in self.patterns:
                self.patterns[intent] = [pattern]
            else:
                self.patterns[intent].append(pattern)

    def add_samples(self, intent, samples):  
        for sample in samples:
            self.x_train.append(sample.lower())
            self.y_train.append(intent)
            
            self.add_pattern(intent, sample)
    
    def add_replies(self, intent, replies):
        self.replies[intent] = replies

    def create(self, corpus):
        for intent in corpus:
            samples = corpus[intent].get("samples")
            replies = corpus[intent].get("replies")

            if samples: 
                self.add_samples(intent, samples)
                
            self.add_replies(intent, replies)
