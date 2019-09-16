
from datetime import datetime, timedelta

import bcrypt
from mongoengine import (BooleanField, DateTimeField, EmbeddedDocumentField,
                         FloatField, IntField, ListField, ReferenceField,
                         SortedListField, StringField)
from mongoengine_goodjson import Document, EmbeddedDocument


class DictExample(EmbeddedDocument):
    en = StringField(required=True)
    cn = StringField(required=True)


class DictDescInfo(EmbeddedDocument):
    name = StringField(required=True)
    value = StringField(required=True)

class DictDescription(EmbeddedDocument):
    description = StringField(required=True)
    seq = IntField(required=True)
    cn = StringField(required=True)
    en = StringField(required=True)
    speech = StringField(required=True)
    infos = ListField(EmbeddedDocumentField(DictDescInfo))
    examples = ListField(EmbeddedDocumentField(DictExample))


class Word(Document):
    word = StringField(required=True)
    star = IntField(max_value=5)
    descriptions = ListField(EmbeddedDocumentField(DictDescription))
    meta = {
        'indexes': [
            ('word', '-star'),
        ]
    }
    @classmethod
    def search_words(cls, *words):
        return Word.objects(word__in=words)

    @classmethod
    def has(cls, *words):
        has = []
        not_has = []
        for word in words:
            if Word.objects(word=word).count() > 0:
                has.append(word)
            else:
                not_has.append(word)
        return has, not_has


    @classmethod
    def search_word(cls, word):
        return Word.objects(word=word).first()

class Sentence(Document):
    eng = StringField(required=True)
    chn = StringField(required=True)
    score = FloatField()
    words = ListField(StringField())
    pos_tag = ListField(StringField())
    roots = ListField(StringField())
    typ = StringField(required=True)
    meta = {
        'indexes': [
            ('roots', '-score'),
            ('typ', 'roots', '-score')
        ]
    }

    @classmethod
    def has(cls, *words):
        has = []
        not_has = []
        for word in words:
            if cls.objects(roots=word).count() > 0:
                has.append(word)
            else:
                not_has.append(word)
        return has, not_has

    @classmethod
    def search_by_root(cls, word):
        return cls.objects(roots=word, typ='dictexams').order_by('-score')

    def cloze(self, word):
        answers = []
        cloz = self.eng
        for idx, root in enumerate(self.roots):
            if root == word:
                answers.append(self.words[idx])
                cloz = cloz.replace(self.words[idx], '[___]')
        return cloz, answers

    
class User(Document):
    username = StringField(required=True, unique=True)
    encrypted_password = StringField(required=True)
    salt = StringField(required=True, default=lambda: bcrypt.gensalt().decode())
    role = StringField(required=True, default='user')
    wordlist = ReferenceField('WordList', required=True)
    meta = {
        'indexes': [
            '#username'
        ]
    }
    def __init__(self, *args, **kwargs):
        passwd = kwargs.get("password")
        if passwd:
            del kwargs['password']
        Document.__init__(self, *args, **kwargs)
        if passwd:
            self.password = passwd

    @classmethod
    def find_by_username(cls, username):
        return cls.objects(username=username).first()

    @classmethod
    def check_user(cls, username, passwd):
        user = cls.objects(username=username).first()
        if user and user.check_password(passwd):
            return user
        return None

    @property
    def password(self):
        return ""

    @password.setter
    def password(self, passwd):
        passwd = passwd.encode()
        salt = bcrypt.gensalt()
        self.encrypted_password = bcrypt.hashpw(passwd, salt).decode()

    def check_password(self, passwd):
        passwd = passwd.encode()
        if (not self.encrypted_password) or (not self.salt):
            return False
        # hashed = bcrypt.hashpw(passwd, self.salt)
        return bcrypt.checkpw(passwd, self.encrypted_password.encode())

    def wordlist_exercise_log(self):
        list_words = self.wordlist.words
        return ExerciseLog.objects(user=self, wordname__in=list_words)

    def word_exercise_log(self, word):
        return ExerciseLog.objects(user=self, wordname=word).first()

    def new_words(self):
        list_words = self.wordlist.words
        learned = [l.wordname for l in self.wordlist_exercise_log().only('wordname')]
        return list(set(list_words) - set(learned))

    def due_words(self):
        return [l.wordname for l in self.wordlist_exercise_log().filter(review__lt=datetime.utcnow()).only('wordname')]

    def next_word(self):
        words = self.due_words()
        if words :
            return words[0]
        words = self.new_words()
        if words :
            return words[0]
        return None

    def next_exercise(self):
        word = self.next_word()
        if not word:
            return None
        word_item = Word.search_word(word)
        if not word_item:
            return None
        now = datetime.utcnow()
        exlog = self.word_exercise_log(word)
        sentence_log = exlog.sentences if exlog else []
        log = {l.sentence.id: score_w(now - l.time, l.result) for l in sentence_log}
        sentences = Sentence.search_by_root(word).limit(100)
        top = None
        top_score = 0
        for s in sentences:
            score = s.score * log.get(s.id, 1)
            if score > top_score:
                top = s
                top_score = score
        if not top:
            return None
        class cloze:
            def __init__(self, word, quiz, answers, sentence):
                self.word = word
                self.cloze = quiz
                self.answers = answers
                self.sentence = sentence
        quiz, answer = top.cloze(word)
        return cloze(word_item, quiz, answer, top)
    def wordlists(self):
        return WordList.objects(user__in=[None, self])


class WordList(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    words = ListField(StringField())
    user = ReferenceField(User)
    meta = {
        'indexes': [
            ('user', 'name'),
        ]
    }

    @classmethod
    def check_word(self, *words):
        has, not_has = Sentence.has(*words)
        whas, wnot_has = Word.has(*words)
        has = set(has)
        whas = set(whas)
        ok = list(has.intersection(whas))
        return ok, not_has, wnot_has


    def user_learned(self, user):
        return ExerciseLog.objects(user=user, wordname__in=list(self.words))

    def user_to_learn(self, user):
        learned = set([e.wordname for e in ExerciseLog.objects(user=user).only('wordname')])
        words = set(self.words)
        return list(words - learned)


def score_w(delta, result):
    if delta < timedelta(minutes=20):
        w = (1-.58)
    elif delta < timedelta(hours=1):
        w = (1-.44)
    elif delta < timedelta(hours=9):
        w = (1-.36)
    elif delta < timedelta(days=1):
        w = (1-.33)
    elif delta < timedelta(days=2):
        w = (1-.28)
    elif delta < timedelta(days=6):
        w = (1-.25)
    elif delta < timedelta(days=31):
        w = (1-.21)
    elif delta < timedelta(days=60):
        w = (1-.10)
    else:
        w = .99
    return w if result else w * 1.5

class SentenceLog(EmbeddedDocument):
    sentence = ReferenceField(Sentence, required=True)
    result = BooleanField(required=True)
    time = DateTimeField(required=True)
ebbinghaus = {
    0: timedelta(minutes=1),
    1: timedelta(minutes=5),
    2: timedelta(minutes=30),
    3: timedelta(hours=12),
    4: timedelta(days=1),
    5: timedelta(days=2),
    6: timedelta(days=4),
    7: timedelta(days=7),
    8: timedelta(days=15),
}


class ExerciseLog(Document):
    user = ReferenceField(User, required=True)
    wordname = StringField(required=True)
    word = ReferenceField(Word, required=True)
    review = DateTimeField(required=True)
    sentences = SortedListField(
        EmbeddedDocumentField(SentenceLog),
        ordering="time", reverse=True)

    def calucate_review(self):
        count = 0
        for s in reversed(self.sentences):
            if not s.result:
                break
            count += 1
        delta = ebbinghaus.get(count, timedelta(days=15))
        self.review = datetime.utcnow() + delta

    @classmethod
    def review_count(cls, user, start, end):
        data =  ExerciseLog.objects(user=user, review__gt=start, review__lt=end).\
            aggregate(
                {'$group' : {'_id' : {'$dateToString' : {
                    'date': "$review",
                    'format': "%Y/%m/%d",
                } }, 'count' : { '$sum' : 1 }}},
                {'$sort': {'_id': 1}}
            )
        return {i['_id']:i['count'] for i in list(data)}

    @classmethod
    def exercise_count(cls, user, start, end):
        data = ExerciseLog.objects(user=user).\
            aggregate(
                {"$match": {"sentences.time": {"$gte": start, "$lte": end}}},
                {"$project":{'_id':0, 'sentences.time': 1, 'sentences.result':1}},
                {"$unwind":"$sentences"},
                {"$match": {"sentences.time": {"$gte": start, "$lte": end}}},
                {'$project': {'day': '$sentences.time',
                              'result': '$sentences.result'}},
                {'$group': { '_id': {'$dateToString' : {
                    'date': "$day",
                    'format': "%Y/%m/%d",
                } }, 'count': { '$sum': 1 } } },
                {'$sort': {'_id': 1}}
            )
        return {i['_id']:i['count'] for i in list(data)}
