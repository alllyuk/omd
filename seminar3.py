from math import log


class TfidfTransformer:
    @staticmethod
    def tf_transform(count_matrix: list) -> list:
        """
        Return term frequency matrix of given document-term matrix
        :param count_matrix: document-term matrix of text corpus
        :return: term frequency matrix
        """
        tf = []
        for words_count_list in count_matrix:
            tf_vector = []
            s = sum(words_count_list)
            for word_count in words_count_list:
                tf_vector.append(word_count / s)
            tf.append(tf_vector)
        return tf

    @staticmethod
    def idf_transform(count_matrix: list) -> list:
        """
        Return inverse document frequency vector of given document-term matrix
        :param count_matrix: document-term matrix of text corpus
        :return: inverse document frequency vector
        """
        idf = []
        all_docs = len(count_matrix)
        word_count = len(count_matrix[0])
        for word_number in range(word_count):
            count_docs = 0
            for words_count_list in count_matrix:
                if words_count_list[word_number] > 0:
                    count_docs += 1
            idf_val = log((all_docs + 1) / (count_docs + 1)) + 1
            idf.append(idf_val)
        return idf

    def fit_transform(self, count_matrix: list) -> list:
        """
        Return TF-IDF matrix of given document-term matrix
        :param count_matrix: document-term matrix of text corpus
        :return: TF-IDF matrix for text corpus
        """
        tf = self.tf_transform(count_matrix)
        idf = self.idf_transform(count_matrix)
        tf_idf = []
        for tf_vector in tf:
            tf_idf_vector = []
            for i, tf_word in enumerate(tf_vector):
                tf_idf_vector.append(round(tf_word * idf[i], 3))
            tf_idf.append(tf_idf_vector)
        return tf_idf


class CountVectorizer:
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


class TfidfVectorizer(CountVectorizer):
    def __init__(self):
        """
        Initialize object and inherits from the CountVectorizer class
        """
        super().__init__()
        self.tf_idg_matrix = []

    def fit_transform(self, corpus: list) -> list:
        """
        Return TF-IDF matrix how it is implemented in TfidfVectorizer clasы
        :param corpus: text corpus
        :return: TF-IDF matrix
        """
        doc_term_matrix = super().fit_transform(corpus)
        self.tf_idg_matrix = TfidfTransformer().fit_transform(doc_term_matrix)
        return self.tf_idg_matrix


if __name__ == '__main__':
    # 1st working test
    corpus = [
     'Crock Pot Pasta Never boil pasta again',
     'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]

    vectorizer = TfidfVectorizer()

    assert vectorizer.fit_transform(corpus) == [
        [0.201, 0.201, 0.286, 0.201, 0.201, 0.201,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.143, 0.0, 0.0, 0.0,
         0.201, 0.201, 0.201, 0.201, 0.201, 0.201]
        ], 'fit_transform method has error in the 1st test'

    assert vectorizer.get_feature_names() == [
        'crock', 'pot', 'pasta', 'never', 'boil', 'again',
        'pomodoro', 'fresh', 'ingredients', 'parmesan', 'to', 'taste'
        ], 'get_feature_names method has error in the 1st test'

    # 2nd working test
    corpus2 = [
        'This is the first document.',
        'This document is the second document.',
        'And this is the third one!',
        'Is this the first document?',
        ]

    vectorizer2 = TfidfVectorizer()

    assert vectorizer2.fit_transform(corpus2) == [
        [0.2, 0.2, 0.2, 0.302, 0.245, 0.0, 0.0, 0.0, 0.0],
        [0.167, 0.167, 0.167, 0.0, 0.408, 0.319, 0.0, 0.0, 0.0],
        [0.167, 0.167, 0.167, 0.0, 0.0, 0.0, 0.319, 0.319, 0.319],
        [0.2, 0.2, 0.2, 0.302, 0.245, 0.0, 0.0, 0.0, 0.0]
        ], 'fit_transform method has error in the 2nd test'

    assert vectorizer2.get_feature_names() == [
        'this', 'is', 'the', 'first', 'document',
        'second', 'and', 'third', 'one'
        ], 'get_feature_names method has error in the 2nd test'

    print('Everything is good! 2 tests passed successfully.')
