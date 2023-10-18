class CountVectorizer():
    def __init__(self):
        """
        Initialize CountVectorizer object
        """
        self.unique_words = None

    def fit_transform(self, raw_document: list) -> list:
        """
        Learn the corpus and return document-term matrix
        :param raw_document: corpus = list of the strings to vectorize
        :return: document-term matrix
        """
        unique_words_set = set()  # use set to speed up the unique words search
        unique_words = []
        clean_corpus = []

        for line in raw_document:
            line_corpus = []
            for word in line.lower().strip('.,!?').split():
                line_corpus.append(word)
                if word not in unique_words_set:
                    unique_words_set.add(word)
                    unique_words.append(word)
            clean_corpus.append(line_corpus)
        self.unique_words = unique_words

        term_doc_matrix = []
        for line in clean_corpus:
            term_doc_matrix.append(
                [line.count(word) for word in self.unique_words])
        return term_doc_matrix

    def get_feature_names(self) -> list:
        """
        Get output corpus words for transformation.
        :return: transformed words from the corpus
        """
        return self.unique_words


if __name__ == '__main__':
    # 1st class working test
    corpus = [
     'Crock Pot Pasta Never boil pasta again',
     'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]

    vectorizer = CountVectorizer()

    assert vectorizer.fit_transform(corpus) == [
        [1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]
        ], 'fit_transform method has error in the 1st test'

    assert vectorizer.get_feature_names() == [
        'crock', 'pot', 'pasta', 'never', 'boil', 'again',
        'pomodoro', 'fresh', 'ingredients', 'parmesan', 'to', 'taste'
        ], 'get_feature_names method has error in the 1st test'

    # 2nd class working test
    corpus2 = [
        'This is the first document.',
        'This document is the second document.',
        'And this is the third one!',
        'Is this the first document?',
        ]

    vectorizer2 = CountVectorizer()

    assert vectorizer2.fit_transform(corpus2) == [
        [1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 2, 1, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0]
        ], 'fit_transform method has error in the 2nd test'

    assert vectorizer2.get_feature_names() == [
        'this', 'is', 'the', 'first', 'document',
        'second', 'and', 'third', 'one'
        ], 'get_feature_names method has error in the 2nd test'

    print('Everything is good! 2 tests passed successfully.')
