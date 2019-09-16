import string
from data import load_dict, load_sentence
from data.dict import Description
from wordai.models import Word, Sentence, User, WordList, DictDescInfo

def dict_to_mongo():
    items = load_dict()
    for word, item in items.items():
        if Word.objects(word=word).count() == 0:
            dbitem = Word(**item)
            dbitem.save()


def sentence_to_mongo(*typ):
    items = load_sentence(*typ)
    print(items)
    for k, v in items.items():
        _sentence_to_mongo(k, v)

def _sentence_to_mongo(typ, items):
    import nltk
    from nltk.corpus import wordnet

    def wordnet_pos(tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')
    stop_words = set(nltk.corpus.stopwords.words('english'))
    stemmer = nltk.stem.WordNetLemmatizer()
    sentences = []
    for trans in items:
        eng, chn = trans.getsource(), trans.gettarget()
        tokens = nltk.word_tokenize(eng)
        pos_tag = [pos[1] for pos in nltk.pos_tag(tokens)]
        roots = [stemmer.lemmatize(word, wordnet_pos(pos_tag[idx])) for idx, word in enumerate(tokens)]
        cleanword = [token for token in roots if token.isalpha() and token not in stop_words and len(token) >= 3]
        # remove duplicates
        clean_word = list(dict.fromkeys(cleanword))
        if len(clean_word) > 0:
            score = Word.search_words(*clean_word).sum('star') / len(clean_word)
        else:
            score = -1
        sentence = Sentence(eng=eng, chn=chn, words=tokens, pos_tag=pos_tag, roots=roots, score=score, typ=typ)
        sentences.append(sentence)
        if len(sentences) > 50:
            Sentence.objects.insert(sentences)
            sentences = []


def new_user(username, passwd, role='user', *args):
    u = User(username=username, password=passwd, role=role)
    u.save()

def dict_star_word_list():
    for star in range(1, 6, 1):
        words = [word.word for word in Word.objects(star=star).only('word')]
        wl = WordList(name="word star {}".format(star), words=words)
        wl.save()

def dict_parse():
    for word in Word.objects:
        for des in word.descriptions:
            res = Description(des.description)
            des.seq = res.seq
            des.cn = res.cn
            des.en = res.en
            des.speech = res.speech
            des.infos = [DictDescInfo(**info) for info in res.info]
        word.save()

def run(method, *args):
    if method == "sync_dict":
        dict_to_mongo()
    elif method == "sync_sentence":
        sentence_to_mongo(*args)
    elif method == "useradd":
        new_user(*args)
    elif method == "wordlist":
        dict_star_word_list(*args)
    elif method == "dict_parse":
        dict_parse(*args)
    else:
        print("unknown command {0}".format(method))
