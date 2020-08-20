
import os, logging , threading, json, MySQLdb.cursors
import concurrent.futures
from time                import sleep
from app.models          import Model
from app                 import app
from app.kmeans          import KMeans
from app.crawling        import Crawling
from app.preprocessing   import Preprocessing
from app.tfidf           import TfIdf
from app.forms           import LoginForm, RegisterForm, CrawlingForm, TrainingForm
from werkzeug.exceptions import HTTPException, NotFound, abort
from werkzeug.security   import generate_password_hash, check_password_hash
from sklearn.feature_extraction.text import TfidfVectorizer
from flask               import render_template, request, url_for, redirect, send_from_directory, session, jsonify




chache  =  {}

@app.route('/admin/logout', methods=['GET', 'POST'])
def logout():

    del chache[session['username']]
    session.pop('username', None)

    return redirect(url_for('index'))


@app.route('/admin/register', methods=['GET', 'POST'])
def register():

    form =  RegisterForm(request.form)

    msg = None

    if 'username' in session:
        return redirect(url_for('index_admin'))

    if request.method == 'GET':
        return render_template( 'admin/pages/register.html', form=form, msg=msg )

    if  form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        modeluser= Model()
        account  = modeluser.validate_account(username)

        if account:
            msg = "Username is exist. Please try other username."

            return render_template('admin/pages/register.html', form=form, msg=msg)

        else:
            modeluser.save_account(username, password)

            return redirect(url_for('login'))

    else:
        msg = 'Input error'

    return render_template( 'admin/pages/register.html', form=form, msg=msg)


@app.route('/admin/login', methods=['GET', 'POST'])
def login():

    form =  LoginForm(request.form)
    msg  =  None

    if 'username' in session:
        return redirect(url_for('index_admin'))

    if  form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        modeluser= Model()
        account  = modeluser.authethiaction_login(username,password)

        if account:
            dictperson                                      = {}
            username_session                                =  account['username']
            session['username']                             = username_session
            session['process_crawling']                     = []
            session['process_preprocessing']                = []
            session['process_training']                     = []
            dictperson['statuscrawling']                    = 0
            dictperson['statuspreprocessing']               = 0
            dictperson['statustraining']                    = 0
            chache[username_session]                        =  dictperson

            return redirect(url_for('index_admin'))

        else:
            msg = "Wrong user or password. Please try again."

    elif 'username' not in session:
        return render_template( 'admin/pages/login.html', form=form, msg=msg )

    else:
        msg = 'Input error'

    return render_template( 'admin/pages/login.html', form=form, msg=msg )


@app.route('/admin', defaults={'path': 'index.html'})
@app.route('/<path>')
def index_admin(path):

    if 'username' not in session:
        return redirect(url_for('login'))

    content = None

    try:
        if 'index' in path:
            return render_template( 'admin/pages/dashboard.html', username=session['username'] )
        else:
            return render_template(  'admin/pages/'+ path , username=session['username'])

    except Exception as error:
        print(error)

        return render_template( 'admin/pages/404.html' )


@app.route('/')
def index():
    modeltraining = Model()
    list_keyword  = modeltraining.select_model_keyword()
    modeltraining.close_connection()

    return render_template('index.html', keyword=list_keyword)


@app.route('/admin/crawling', methods=['GET', 'POST'])
def crawling():
    form =  CrawlingForm(request.form)

    if 'username' not in session:
        return redirect(url_for('login'))

    if chache[session['username']]['statuscrawling']  ==   0 and session['process_crawling']:
        session['process_crawling'].remove(1)
        session.modified = True

    return render_template('admin/pages/crawling.html', form=form, username=session['username'], crawling=session['process_crawling'])


@app.route('/admin/crawling/processcrawl', methods=['POST'])
def processcrawl():
    form =  CrawlingForm(request.form)

    if 'username' not in session:
        return redirect(url_for('login'))

    if  form.validate_on_submit():
        username        = session['username']
        keyword         = request.form['keyword']
        startdate       = request.form['startdate']
        enddate         = request.form['enddate']
        maxtweet        = int(request.form['maxtweet']) if request.form['maxtweet'] else 0

        # backgroundprocess_crawling(keyword, startdate, enddate, maxtweet, username)
        worker          = threading.Thread(target=backgroundprocess_crawling, args=(keyword, startdate, enddate, maxtweet, username,))
        worker.daemon   = True
        worker.start()   

        session['process_crawling'].append(1)
        session.modified = True
        chache[session['username']]['statuscrawling']   = 1

        msg =   "Tweet crawler processed"
        return render_template('admin/pages/crawling.html', form=form,  msg=msg, username=session['username'], crawling=session['process_crawling'])

    else:
        msg =   "Form not validate"
        return render_template('admin/pages/crawling.html', form=form, msg=msg, username=session['username'], crawling=session['process_crawling'])

def backgroundprocess_crawling(keyword, startdate, enddate, maxtweet, username):
    Crawling().crawling(keyword, startdate, enddate, maxtweet)
    chache[username]['statuscrawling']   =  0


@app.route('/admin/crawling/checkcrawling', methods=['POST'])
def checkcrawling():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:

                return jsonify({'statuscrawling':chache[username]['statuscrawling']})

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))
    else:
        return jsonify({'statuscrawling':chache['statuscrawling']})


@app.route('/admin/table/hastags', methods=['POST'])
def table_hastags():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modeltwitter        =   Model()
                result              =   modeltwitter.select_table_hastags()
                data                =   {}
                data.setdefault('data', result)
                modeltwitter.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/table/hastags/delete', methods=['POST'])
def delete_keyword():

    if request.data:
        username = json.loads(request.data).get('username')
        keyword  = json.loads(request.data).get('keyword')

        try:
            if session['username'] == username:
                modeltwitter=   Model()
                result      =   modeltwitter.delete_keyword_twitter(keyword)
                data        =   {}
                data.setdefault('succes', True)

                modeltwitter.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/preproccessing', methods=['GET', 'POST'])
def preproccessing():

    if 'username' not in session:
        return redirect(url_for('login'))

    if chache[session['username']]['statuspreprocessing']  ==   0 and session['process_preprocessing']:
        session['process_preprocessing'].remove(1)
        session.modified = True

    return render_template('admin/pages/preprocessing.html', username=session['username'], preprocessing=session['process_preprocessing'])


@app.route('/admin/table/preprocessing', methods=['POST'])
def table_preprocessing():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modeltwitter     = Model()
                result           = modeltwitter.select_keyword_preprocessing()
                data             =  {}
                data.setdefault('data', result)

                modeltwitter.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/table/preprocessing/proces', methods=['POST'])
def table_preprocessing_keyword():

    if request.data:
        username = json.loads(request.data).get('username')
        keyword  = json.loads(request.data).get('keyword')

        try:
            if session['username'] == username:
                modeltwitter        = Model()
                data_preprocessing  = modeltwitter.select_keyword_not_preprocessing(keyword)
                modeltwitter.close_connection()
                # backgroundprocess_preprocessing(keyword, data_preprocessing, username)
                worker              =   threading.Thread(target=backgroundprocess_preprocessing, args=(keyword, data_preprocessing, username,))
                worker.daemon       =   True
                worker.start()   

                chache[session['username']]['statuspreprocessing']   =   1
                data                            =   {}
                data['statuspreprocessing']     =   chache[session['username']]['statuspreprocessing']
                session['process_preprocessing'].append(1)
                session.modified                = True

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))

def background_preprocessing(data_tweet, keyword, preprocessing, model):
    model_twitter       =   model
    id_tweet            =   data_tweet.get('id')
    tweet               =   data_tweet.get('tweet')
    tweet_lower, tweet_regex, tweet_stopword, tweet_steming    =  preprocessing.cleansing(tweet)
    model_twitter.save_tweet_preprocessing(id_tweet, keyword, tweet_lower, tweet_regex, tweet_stopword, tweet_steming)

    return id_tweet, tweet_steming

def backgroundprocess_preprocessing(keyword, data_preprocessing, username):
    model               =   Model()
    tfidf               =   TfIdf(model)
    preprocessing       =   Preprocessing(model)
    list_id_tweet       =   []
    list_tweet_stemming =   []
    list_tfidf          =   []

    try:

        model.delete_clustered(keyword)

        for data_tweet in data_preprocessing:
            id_tweet, tweet_stemming = background_preprocessing(data_tweet, keyword,  preprocessing, model)
            list_id_tweet.append(id_tweet)
            list_tweet_stemming.append(tweet_stemming)

        tfidf.word_idf(list_tweet_stemming, keyword)
        list_idf   = model.select_idf(keyword)

        for index, tweet_steming in enumerate(list_tweet_stemming):
            id_tweet            =   list_id_tweet[index]
            tweet_tfidf         =   tfidf.tf_idf(preprocessing.tokennizing(tweet_steming), keyword, list_idf)
            model.update_tfidf(id_tweet, keyword,tweet_tfidf)
            list_tfidf.append({'id':id_tweet,'tfidf':tweet_tfidf})

        data = sorted(list_tfidf, key=lambda k: k['id'])

        model.update_vocab_config(data, keyword)

    except Exception as error:
        print(error)

    finally:
        chache[username]['statuspreprocessing']    =  0
        model.close_connection()


@app.route('/admin/preprocessing/checkpreprocessing', methods=['POST'])
def checkpreprocessing():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:

                return jsonify({'statuspreprocessing':chache[session['username']]['statuspreprocessing']})

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return jsonify({'statuspreprocessing':chache[session['username']]['statuspreprocessing']})


@app.route('/admin/corpus', methods=['GET', 'POST'])
def corpus():

    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('admin/pages/corpus.html', username=session['username'])


@app.route('/admin/table/corpus', methods=['POST'])
def table_corpus():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modelvocab =   Model()
                result     =   modelvocab.select_corpus()
                data       =   {}
                data.setdefault('data', result)

                modelvocab.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/table_preprocessing', methods=['GET', 'POST'])
def preprocessing_after():

    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('admin/pages/preprocessing_table.html', username=session['username'])


@app.route('/admin/table/table_preprocessing', methods=['POST'])
def table_preprocessing_after():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modelpreprocessing = Model()
                result             = modelpreprocessing.select_preprocessing()
                data               =   {}
                data.setdefault('data', result)

                modelpreprocessing.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/stopword', methods=['GET', 'POST'])
def stopword():

    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('admin/pages/stopword.html', username=session['username'])


@app.route('/admin/stopword/add', methods=['POST'])
def add_stopwords():
    if request.data:
        username = json.loads(request.data).get('username')
        new_word = json.loads(request.data).get('word')

        try:
            if session['username'] == username:
                modelstopword   =   Model()
                result          =   modelstopword.add_stopword(new_word)
                modelstopword.close_connection()

                return jsonify(result)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/stopword/edit', methods=['POST'])
def edit_stopword():
    if request.data:
        username    = json.loads(request.data).get('username')
        word_before = json.loads(request.data).get('word_before')
        word_after  = json.loads(request.data).get('word_after')

        try:
            if session['username'] == username:
                modelstopword   =   Model()
                result          =   modelstopword.edit_stopword(word_before, word_after)
                modelstopword.close_connection()

                return jsonify(result)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/stopword/delete', methods=['POST'])
def delete_stopword():
    if request.data:
        username = json.loads(request.data).get('username')
        word     = json.loads(request.data).get('word')

        try:
            if session['username'] == username:
                modelstopword   =   Model()
                result          =  modelstopword.delete_stopword(word)
                modelstopword.close_connection()

                return jsonify(result)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/table/stopword', methods=['POST'])
def table_stopword():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modelstopword   =   Model()
                result          =   modelstopword.select_stopword()
                data            =   {}
                data.setdefault('data', result)

                modelstopword.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/kbba', methods=['GET', 'POST'])
def kbba():

    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('admin/pages/kbba.html', username=session['username'])


@app.route('/admin/kbba/add', methods=['POST'])
def add_kbba():
    if request.data:
        username = json.loads(request.data).get('username')
        alay     = json.loads(request.data).get('alay')
        baku     = json.loads(request.data).get('baku')

        try:
            if session['username'] == username:
                modelkbba       =   Model()
                result          =   modelkbba.add_kbba(alay, baku)
                modelkbba.close_connection()

                return jsonify(result)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/kbba/edit', methods=['POST'])
def edit_kbba():
    if request.data:
        username    = json.loads(request.data).get('username')
        alay_before = json.loads(request.data).get('alay_before')
        alay_after  = json.loads(request.data).get('alay_after')
        baku_before = json.loads(request.data).get('baku_before')
        baku_after  = json.loads(request.data).get('baku_after')

        try:
            if session['username'] == username:
                modelkbba       =   Model()
                result          =   modelkbba.edit_kbba(alay_after, baku_after, alay_before, baku_before)
                modelkbba.close_connection()

                return jsonify(result)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/kbba/delete', methods=['POST'])
def delete_kbba():
    if request.data:
        username = json.loads(request.data).get('username')
        alay     = json.loads(request.data).get('alay')
        baku     = json.loads(request.data).get('baku')

        try:
            if session['username'] == username:
                modelkbba   =  Model()
                result      =  modelkbba.delete_kbba(alay, baku)
                modelkbba.close_connection()

                return jsonify(result)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/table/kbba', methods=['POST'])
def table_kbba():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modelkbba       =   Model()
                result          =   modelkbba.select_kbba()
                data            =   {}
                data.setdefault('data', result)

                modelkbba.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/label', methods=['GET', 'POST'])
def label():

    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('admin/pages/label_cluster.html', username=session['username'])


@app.route('/admin/label/add', methods=['POST'])
def add_label():

    if request.data:
        username = json.loads(request.data).get('username')
        label    = json.loads(request.data).get('label')
        dec_label= json.loads(request.data).get('dec_label')

        try:
            if session['username'] == username:
                modellabel  = Model()
                result      = modellabel.add_label(label, dec_label)
                modellabel.close_connection()

                return jsonify(result)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/label/edit', methods=['POST'])
def edit_label():
    if request.data:
        username    = json.loads(request.data).get('username')
        id_label    = json.loads(request.data).get('id_label')
        dec_label   = json.loads(request.data).get('dec_label')
        label       = json.loads(request.data).get('label')

        try:
            if session['username'] == username:
                modellabel  = Model()
                result      = modellabel.edit_label(id_label, dec_label, label)
                modellabel.close_connection()

                return jsonify(result)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/label/delete', methods=['POST'])
def delete_label():
    if request.data:
        username = json.loads(request.data).get('username')
        id_label = json.loads(request.data).get('id_label')

        try:
            if session['username'] == username:
                modellabel  = Model()
                result      = modellabel.delete_label(id_label)
                modellabel.close_connection()

                return jsonify(result)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/table/label', methods=['POST'])
def table_label():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modellabel  =   Model()
                result      =   modellabel.select_label()
                data        =   {}
                data.setdefault('data', result)
                modellabel.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/centroid', methods=['GET', 'POST'])
def centroid():

    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('admin/pages/centroid.html', username=session['username'])


@app.route('/admin/table/centroid', methods=['POST'])
def table_centroid():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modelcluster = Model()
                result       = modelcluster.select_centroid_cluster()
                data         =   {}
                data.setdefault('data', result)
                modelcluster.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/cluster', methods=['GET', 'POST'])
def cluster():

    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('admin/pages/cluster.html', username=session['username'])


@app.route('/admin/table/cluster', methods=['POST'])
def table_cluster():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modelcluster =   Model()
                result       =   modelcluster.select_cluster()
                data         =   {}
                data.setdefault('data', result)

                modelcluster.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/sse', methods=['GET', 'POST'])
def sse():

    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('admin/pages/sse.html', username=session['username'])


@app.route('/admin/table/sse', methods=['POST'])
def table_sse():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modelcluster =   Model()
                result       =   modelcluster.select_sse()
                data         =   {}
                data.setdefault('data', result)
                modelcluster.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/training', methods=['GET', 'POST'])
def training():

    if 'username' not in session:
        return redirect(url_for('login'))

    if chache[session['username']]['statustraining']  ==   0 and session['process_training']:
        session['process_training'].remove(1)
        session.modified = True

    modellabel  = Model()
    emoticon    = modellabel.select_label()
    modellabel.close_connection()

    return render_template('admin/pages/training.html', username=session['username'], training=session['process_training'], emoticon=emoticon)

@app.route('/admin/table/training', methods=['POST'])
def table_training():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                modeltwitter = Model()
                result       = modeltwitter.select_table_training()
                data         =  {}
                data.setdefault('data', result)

                modeltwitter.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/table/hastags/train', methods=['POST'])
def training_process():

    if request.data:
        username = json.loads(request.data).get('username')
        keyword  = json.loads(request.data).get('keyword')
        iteration= json.loads(request.data).get('iteration')
        cluster  = json.loads(request.data).get('cluster')
        centroid = json.loads(request.data).get('centroid')

        try:
            if session['username'] == username:
                # backgroundprocess_training(username, keyword, centroid, cluster, iteration)
                worker                      =   threading.Thread(target=backgroundprocess_training, args=(username, keyword, centroid, cluster, iteration,))
                worker.daemon               =   True
                worker.start()   

                chache[session['username']]['statustraining']   =   1
                data                            =   {}
                data['statustraining']          =   chache[session['username']]['statustraining']
                session['process_training'].append(1)
                session.modified                = True


                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/admin/table/hastags/min_max', methods=['POST'])
def check_min_max_tweet():

    if request.data:
        username = json.loads(request.data).get('username')
        keyword = json.loads(request.data).get('keyword')

        try:
            if session['username'] == username:
                modeltwitter =  Model()
                dict_result  =  modeltwitter.select_min_max_tweet(keyword)
                modeltwitter.close_connection()
                return jsonify(dict_result)

            else:
                return redirect(url_for('login'))
        except Exception as error:
            print(error)
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


def backgroundprocess_training(username, keyword, centroid, cluster, iteration, k=3):
    model_vocabulary            = Model()
    total_tweets, data          = model_vocabulary.select_data_training(keyword)
    list_id                     = [x['id'] for x in data]
    list_preprocessing          = [x['tfidf'] for x in data]
    kmeans                      = KMeans(model_vocabulary)
    status                      = kmeans.fit(keyword, list_id, centroid, cluster, list_preprocessing, total_tweets, k, iteration)
    chache[username]['statustraining']    =  status

@app.route('/admin/training/checktraining', methods=['POST'])
def checktraining():

    if request.data:
        username = json.loads(request.data).get('username')

        try:
            if session['username'] == username:
                print(chache)
                return jsonify({'statustraining':chache[session['username']]['statustraining']})

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return jsonify({'statustraining':chache[session['username']]['statustraining']})


@app.route('/admin/predict', methods=['GET', 'POST'])
def predict():

    if 'username' not in session:
            return redirect(url_for('login'))
    modeltraining = Model()
    list_keyword  = modeltraining.select_model_keyword()
    modeltraining.close_connection()

    return render_template('admin/pages/predict.html', keyword=list_keyword, username=session['username'])


@app.route('/admin/predict/predict', methods=['POST'])
def predict_tweet():

    if request.data:
        username = json.loads(request.data).get('username')
        tweet    = json.loads(request.data).get('tweet')
        keyword = json.loads(request.data).get('keyword')

        # try:
        if session['username'] == username:
            dict_predict    =   {}
            kmeans          = KMeans()
            cluster_name, emoticon    = kmeans.predict(tweet, keyword)
            dict_predict['cluster']     =   cluster_name
            dict_predict['emoticon']    =   emoticon

            return jsonify(dict_predict)

        else:
            return redirect(url_for('login'))

        # except Exception as error:
        #     print(error)
        #     return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))


@app.route('/predict/predict', methods=['POST'])
def predict_tweet_global():

    if request.data:
        tweet    = json.loads(request.data).get('tweet')
        keyword = json.loads(request.data).get('keyword')

        try:
                dict_predict    =  {}
                kmeans          = KMeans()
                cluster_name, emoticon      = kmeans.predict(tweet, keyword)
                dict_predict['cluster']     =   cluster_name
                dict_predict['emoticon']    =   emoticon

                return jsonify(dict_predict)

        except Exception as error:
            print(error)
            return redirect(url_for('/'))

    else:
        return redirect(url_for('/'))


@app.route('/admin/visualitation', methods=['GET', 'POST'])
def visualitation():

    if 'username' not in session:
        return redirect(url_for('login'))
    modeltraining = Model()
    list_keyword  = modeltraining.select_model_keyword()
    modeltraining.close_connection()
    return render_template('admin/pages/visualitation.html', keyword=list_keyword,  username=session['username'])


@app.route('/admin/visualitation/show', methods=['POST'])
def visualitation_show():

    if request.data:
        username = json.loads(request.data).get('username')
        keyword = json.loads(request.data).get('keyword')

        try:
            if session['username'] == username:
                modelcluster = Model()
                data         = modelcluster.select_cluster_plot(keyword)
                modelcluster.close_connection()

                return jsonify(data)

            else:
                return redirect(url_for('login'))

        except Exception as error:
            print(error)
            return redirect(url_for('login'))

    else:
        return redirect(url_for('login'))
