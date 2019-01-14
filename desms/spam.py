import jieba
import numpy
import pandas as pd
import pickle

_MODEL = None
_VECTORIZER = None
_TRANSFORMER = None
_STOP_WORDS = None

base_dir = ''

def get_stop_words():
    global _STOP_WORDS
    if _STOP_WORDS is not None:
        return _STOP_WORDS
    stop_words = pd.read_csv(base_dir + 'jupyter/stopWord.txt', header=None)
    _STOP_WORDS = frozenset(stop_words[0].values)
    return _STOP_WORDS


def participle(text):
    stop_words = get_stop_words()
    seg_list = jieba.cut(text)
    results = set(seg_list) - stop_words
    return ' '.join(results)


def load_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL
    pkl_filename = base_dir + 'jupyter/pickle_model.pkl'
    # Load from file
    with open(pkl_filename, 'rb') as file:
        _MODEL = pickle.load(file)
    return _MODEL


def load_vectorizer():
    global _VECTORIZER
    if _VECTORIZER is not None:
        return _VECTORIZER
    pkl_filename = base_dir + 'jupyter/vectorizer.pkl'
    # Load from file
    with open(pkl_filename, 'rb') as file:
        _VECTORIZER = pickle.load(file)
    return _VECTORIZER


def load_tfidf_transformer():
    global _TRANSFORMER
    if _TRANSFORMER is not None:
        return _TRANSFORMER
    pkl_filename = base_dir + 'jupyter/transformer.pkl'
    # Load from file
    with open(pkl_filename, 'rb') as file:
        _TRANSFORMER = pickle.load(file)
    return _TRANSFORMER


def vectorizer(ndarray):
    vectorizer = load_vectorizer()
    tfidf_tansformer = load_tfidf_transformer()
    X_test_termcounts = vectorizer.transform(ndarray)
    X_test_tfidf = tfidf_tansformer.transform(X_test_termcounts)

    return X_test_tfidf


def is_spam(text):
    X_test_tfidf = vectorizer(numpy.array([participle(text)]))
    classifier_model = load_model()
    predicted = classifier_model.predict(X_test_tfidf)
    if predicted[0] == 1:
        return True
    return False


if __name__ == '__main__':
    base_dir = '../'
    text = '【菲诺商贸】尊敬的菲诺会员，我司将于2018年12月31日零时对2018年1月1日前到期未使用积分进行清零，请您尽快到店使用，详询门店。'
    print(is_spam(text))
