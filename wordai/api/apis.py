import hashlib
import json
from datetime import datetime, timedelta

import wordai.models as models
from flask import Blueprint
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, get_jwt_identity,
                                get_raw_jwt, jwt_refresh_token_required,
                                jwt_required)
from flask_restful import Api, Resource, abort, reqparse, request
from jsonschema import validate

blueprint = Blueprint('profile', __name__,
                    template_folder='templates',
                    static_folder='static')

api = Api(blueprint)

class api_register(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, cls):
        api.add_resource(cls, self.path)
        return cls

def admin_required(f):
    def __inner__(self, *args, **kwargs):
        identify = get_jwt_identity()
        user = models.User.find_by_username(identify)
        if user and user.role == 'admin':
                return f(self, user, *args, **kwargs)
        return {
            'message': 'Not found',
        }, 404
    return jwt_required(__inner__)

def user_required(f):
    def __inner__(self, *args, **kwargs):
        identify = get_jwt_identity()
        user = models.User.find_by_username(identify)
        if user and user.role in ['admin', 'user']  :
                return f(self, user, *args, **kwargs)
        return {
            'message': 'Not found',
        }, 404
    return jwt_required(__inner__)

user_parser = reqparse.RequestParser()
user_parser.add_argument('username', help='This username cannot be blank', required=True)
user_parser.add_argument('password', help='This password cannot be blank', required=True)

@api_register("/registration")
class UserRegistration(Resource):
    def post(self):
        return {'message': 'User registration'}


@api_register("/login")
class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        current_user = models.User.check_user(data['username'], data['password'])
        if not current_user:
            abort(401)
            return {
                'message': 'User {} doesn\'t exist'.format(data['username']),
            }

        access_token = create_access_token(identity=data['username'])
        refresh_token = create_refresh_token(identity=data['username'])
        return {
            'message': 'Logged in as {}'.format(current_user.username),
            'role': current_user.role,
            'access_token': access_token,
            'refresh_token': refresh_token
        }

@api_register("/token/refresh")
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        if current_user:
            access_token = create_access_token(identity=current_user)
            return {
                'access_token': access_token}
        abort(401)
        return {'message': 'invalid refresh token'}


@api_register("/wordlist")
class WordListList(Resource):
    @user_required
    def get(self, user):
        return [json.loads(x.to_json()) for x in user.wordlists()]

    @user_required
    def put(self, user):
        schema = {
            "type": "array",
            "items": {"type": "string"},
            "uniqueItems": True
        }
        try:
            body = request.json
            validate(instance=body, schema=schema)
            wordok, not_has, wnot_has = models.WordList.check_word(*body)
            defines = models.Word.search_words(*wordok)
            return {
                "defines": {w['word']: w for w in json.loads(defines.to_json())},
                "not_dict": wnot_has,
                "not_sentence": not_has,
            }
        except Exception as err:
            return {
                "message": "invalid request body",
                "error": str(err)
            }, 422
    @user_required
    def post(self, user):
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "words": {
                    "type": "array",
                    "items": {"type": "string"},
                    "uniqueItems": True
                }
            }
        }
        try:
            body = request.json
            validate(instance=body, schema=schema)
            wordok, not_has, wnot_has = models.WordList.check_word(*body['words'])
            body['words'] = list(wordok)
            wordlist = models.WordList(**body)
            wordlist.user = user
            wordlist.save()
            return {
                "message": "ok",
                "has": list(wordok),
                "not_dict": wnot_has,
                "not_sentence": not_has,
            }
        except Exception as err:
            return {
                "message": "invalid request body",
                "error": str(err)
            }, 422

@api_register("/wordlist/<string:lid>")
class WordListItem(Resource):
    @user_required
    def get(self, user, lid):
        print(lid)
        return json.loads(user.wordlists().filter(id=lid).first().to_json())

    @user_required
    def put(self, user, lid):
        wordlist = models.WordList.objects(user=user, id=lid).first()
        if not wordlist:
            return {
                "message": "wordlist not exists",
            }, 404
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "words": {
                    "type": "array",
                    "items": {"type": "string"},
                    "uniqueItems": True
                }
            }
        }
        try:
            body = request.json
            validate(instance=body, schema=schema)
            wordok, not_has, wnot_has = models.WordList.check_word(*body['words'])
            wordlist.words = wordok
            wordlist.name = body['name']
            wordlist.description = body['description']
            wordlist.user = user
            wordlist.save()
            return {
                "message": "ok",
                "has": list(wordok),
                "not_dict": wnot_has,
                "not_sentence": not_has,
            }
        except Exception as err:
            return {
                "message": "invalid request body",
                "error": str(err)
            }, 422

    @user_required
    def delete(self, user, lid):
        wordlist = models.WordList.objects(user=user, id=lid).first()
        if not wordlist:
            return {
                "message": "wordlist not exists",
            }, 404
        wordlist.delete()

@api_register("/user/wordlist")
class UserWordList(Resource):
    @user_required
    def get(self, user):
        if not user.wordlist:
            return {
                "message", "wordlist not set"
            }, 404
        data = json.loads(user.wordlist.to_json())
        return {
            "message": "ok",
            "wordlist": data['id'],
            "wordlist_name": data['name']
        }
    @user_required
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument('wordlist', help='This wordlist cannot be blank', required=True)
        wordlist_id = parser.parse_args()
        wordlist = models.WordList.objects(id=wordlist_id['wordlist']).first()
        user.wordlist = wordlist
        user.save()
        return {
            "message": "ok",
            "wordlist": wordlist.name
        }


@api_register("/learn/word")
class LearnNext(Resource):
    @user_required
    def get(self, user):
        ex = user.next_exercise()
        if ex:
            sentence_id = json.loads(ex.sentence.to_json())['id']
            word_id = json.loads(ex.word.to_json())['id']
            return {
                "id": word_id,
                "word": ex.word.word,
                "message": "ok",
                "cloze": ex.cloze,
                "cn": ex.sentence.chn,
                "sid": sentence_id,
                "answers": [a for a in ex.answers],
                "check": [hashlib.sha1((a+sentence_id+word_id).encode()).hexdigest() for a in ex.answers]
            }
        else:
            return {
                "message": "no word need exercise"
            }, 404
    @user_required
    def post(self, user):
        parser = reqparse.RequestParser()
        parser.add_argument('id', help='This answers cannot be blank', required=True)
        parser.add_argument('sid', help='This answers cannot be blank', required=True)
        parser.add_argument('answers', help='This answers cannot be blank', required=True,action='append')
        parser.add_argument('check', help='This answer_check cannot be blank', required=True, action='append')
        data = parser.parse_args()
        word_id = data['id']
        word = models.Word.objects(id=word_id).first()
        if not word:
            return {
                "message": "word not exist"
            }, 404
        sentence_id = data['sid']
        answers = data['answers']
        check = data['check']
        check_res = [hashlib.sha1((a+sentence_id+word_id).encode()).hexdigest() for a in answers]
        result = check == check_res
        slog = models.SentenceLog(sentence=sentence_id, result=result, time=datetime.utcnow())
        models.ExerciseLog.objects(user=user, word=word).update_one(
            push__sentences=slog, wordname=word.word,
            upsert=True)
        log = models.ExerciseLog.objects(user=user, word=word).first()
        log.calucate_review()
        log.save()
        return {
            "message": "ok",
            "result": result,
        }


@api_register("/dictionary/<string:word>")
class Dictionary(Resource):
    @user_required
    def get(self, user, word):
        define = models.Word.objects(word=word).first()
        if define:
            return json.loads(define.to_json())
        else:
            return {"message": "not found"}, 404


@api_register("/wordlist/learned")
class WordlistLearned(Resource):
    @user_required
    def get(self, user):
        words = user.wordlist.user_learned(user).only("wordname", "review")
        return json.loads(words.to_json())


@api_register("/wordlist/to_learn")
class WordlistToLearn(Resource):
    @user_required
    def get(self, user):
        words = user.wordlist.user_to_learn(user)
        return words

@api_register("/statistic/learn")
class StatisticLearn(Resource):
    @user_required
    def get(self, user):
        return {
            'exercise': models.ExerciseLog.exercise_count(
                user,
                datetime.now()-timedelta(days=7),
                datetime.now()+timedelta(days=7)
            ),
            'review': models.ExerciseLog.review_count(
                user,
                datetime.now()-timedelta(days=7),
                datetime.now()+timedelta(days=7)
            )
        }
