import re
import json
import psycopg2
import numpy            as      np
from   ast              import  literal_eval
from   psycopg2.extras  import  RealDictCursor

class Model():

    def __init__(self):
        self.db      =   psycopg2.connect(host='localhost', port=5432, database='sentiment', user='root', password='')

    def authethiaction_login(self, username, password):

        try:
            self.cursor  =   self.db.cursor(cursor_factory=RealDictCursor)
            self.cursor.execute('SELECT * FROM user_admin WHERE username = %s AND password = %s', (username, password,))
            self.db.commit()

            result = self.cursor.fetchone()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

        return result

    def validate_account(self, username):

        try:
            self.cursor  =   self.db.cursor(cursor_factory=RealDictCursor)
            self.cursor.execute('SELECT username FROM user_admin WHERE username = %s ', (username,))
            self.db.commit()

            result       = self.cursorfetchone()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

        return result

    def save_account(self, username, password):

        try :
            self.cursor  =   self.db.cursor()
            self.cursor.execute('INSERT INTO user_admin (username, password) VALUES (%s, %s) ', (username,password,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def is_nulls(self, tweet):
        result = False

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT id FROM twitter WHERE tweet = %s ', (tweet,))
            self.db.commit()

            result       = self.cursor.fetchall()
            result       = result[0][0] if result else False
            
        except Exception as error:
            print(error)
            
        finally:
            self.cursor.close()

        return result

    def save_tweet(self, tweet, keyword, tanggal_tweet):

        try:
            if  tweet:
                self.cursor  =   self.db.cursor()
                self.cursor.execute('INSERT INTO twitter (tweet, keyword, tanggal_tweet) VALUES (%s, %s, %s) ', (tweet, keyword, tanggal_tweet,))
                self.db.commit()
            else:
                pass

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def select_min_max_tweet(self, keyword):

        try:
            dict_result         =   {}
            self.cursor         =   self.db.cursor()
            self.cursor.execute('SELECT MIN(A.id) min_id, MAX(A.id) max_id FROM (SELECT id FROM twitter where keyword = %s) A', (keyword,))
            self.db.commit()

            result              =   self.cursor.fetchall()
            dict_result['min']  =   result[0][0] if result else 0
            dict_result['max']  =   result[0][1] if result else 0

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

        return dict_result

    def select_table_training(self):
        
        try:
            self.cursor  =   self.db.cursor(cursor_factory=RealDictCursor)
            self.cursor.execute('SELECT A.keyword, count(1) total FROM twitter A GROUP BY A.keyword')
            self.db.commit()

            result       = self.cursor.fetchall()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

        return result

    def select_table_hastags(self):
        
        try:
            self.cursor  =   self.db.cursor(cursor_factory=RealDictCursor)
            self.cursor.execute('SELECT keyword, count(1) total FROM twitter GROUP BY keyword')
            self.db.commit()

            result       = self.cursor.fetchall()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

        return result

    def delete_keyword_twitter(self, keyword):
        
        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM twitter WHERE keyword = %s', (keyword,))
            self.cursor.execute('DELETE FROM cluster WHERE keyword = %s', (keyword,))
            self.cursor.execute('DELETE FROM centroid_model WHERE keyword = %s', (keyword,))
            self.cursor.execute('DELETE FROM preprocessing WHERE keyword = %s', (keyword,))
            self.cursor.execute('DELETE FROM sse WHERE keyword = %s', (keyword,))
            self.cursor.execute('DELETE FROM vocabulary_config WHERE keyword = %s', (keyword,))
            self.cursor.execute('DELETE FROM vocabulary WHERE keyword = %s', (keyword,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def select_keyword_preprocessing(self):
        
        try:
            self.cursor  =   self.db.cursor(cursor_factory=RealDictCursor)
            self.cursor.execute('SELECT keyword, COUNT(1) total FROM twitter GROUP BY keyword')
            self.db.commit()

            result       = self.cursor.fetchall()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

        return result

    def select_keyword_not_preprocessing(self, keyword):
        
        try:
            self.cursor  =   self.db.cursor(cursor_factory=RealDictCursor)
            self.cursor.execute('SELECT A.id, A.tweet, A.keyword FROM twitter A LEFT JOIN preprocessing B ON A.id=B.id WHERE B.id IS NULL AND A.keyword = %s', (keyword,))
            self.db.commit()

            result       = self.cursor.fetchall()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

        return result

    def select_duplicate_tweet(self, keyword, tweet_steming):
        
        try:
            status_duplicate = 0
            self.cursor      =   self.db.cursor()
            self.cursor.execute('SELECT tweet_steming FROM preprocessing WHERE keyword = %s and tweet_steming = %s ', (keyword,tweet_steming,))
            self.db.commit()

            result           =   self.cursor.fetchall()
            
            if result:
                status_duplicate = 1
            else:
                status_duplicate = 0

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

        return status_duplicate

    def delete_tweet(self, id_tweet, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM twitter WHERE id = %s and keyword = %s ', (id_tweet, keyword,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def save_tweet_preprocessing(self, id, keyword, tweet_lower, tweet_regex, tweet_stopword, tweet_steming):

        try:
            if tweet_steming:
                is_duplicate = self.select_duplicate_tweet(keyword, tweet_steming)

                if not is_duplicate and not tweet_steming.isspace() :
                    self.cursor  =   self.db.cursor()
                    self.cursor.execute('INSERT INTO preprocessing (id, keyword, tweet_lower, tweet_regex, tweet_stopword, tweet_steming) VALUES (%s, %s, %s, %s, %s, %s) ', (id, keyword, tweet_lower, tweet_regex, tweet_stopword, tweet_steming,))
                    self.db.commit()
                else:
                    self.delete_tweet(id, keyword)

            else:
                self.delete_tweet(id, keyword)

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def update_tfidf(self, id, keyword, tweet_tfidf):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('UPDATE preprocessing SET tweet_tfidf = %s where id = %s  and keyword = %s  ', (str(tweet_tfidf), id, keyword, ))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def delete_clustered(self, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM cluster WHERE keyword = %s', (str(keyword),))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def select_stopword_preprocessing(self):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT stopword FROM stopword')
            self.db.commit()

            result       =   self.cursor.fetchall()
            result       =   [x[0] for x in result] if result else []
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return result

    def select_kbba_preprocessing(self):
        dict_result  =   {}

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT alay, baku FROM kbba')
            self.db.commit()

            result       =   self.cursor.fetchall()
            
            for data in result:
                dict_result[str(data[0])]   =  str(data[1])

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return dict_result

    def select_preprocessing(self):

        try:
            list_preprocessing  = []
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT A.keyword, A.id, A.tweet, B.tweet_lower, B.tweet_regex, B.tweet_stopword, B.tweet_steming  FROM twitter A JOIN preprocessing B ON A.id=B.id')
            self.db.commit()

            result      =   self.cursor.fetchall()
            
            for data in result:
                dict_preprocessing   = {}
                dict_preprocessing['keyword']        = data[0]
                dict_preprocessing['id']             = data[1]
                dict_preprocessing['tweet']          = data[2]
                dict_preprocessing['tweet_lower']    = data[3]
                dict_preprocessing['tweet_regex']    = data[4]
                dict_preprocessing['tweet_stopword'] = data[5]
                dict_preprocessing['tweet_stemming'] = data[6]
                # dict_preprocessing['tweet_tfidf']    = data[7]

                list_preprocessing.append(dict_preprocessing)

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_preprocessing

    def select_vocab_config(self, keyword):
        
        try:
            self.cursor  =   self.db.cursor()
            cursor.execute('SELECT vocab_size, data_count FROM vocabulary_config WHERE keyword = %s', (keyword,))
            self.db.commit()

            result       = self.cursor.fetchall()
        
        except Exception as error:
            print(error)
       
        finally:
            self.cursor.close()

        return result

    def delete_vocab_config(self, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM vocabulary_config WHERE keyword = %s', (keyword,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def save_vocab_config(self, vocab_size, data_count, keyword):

        try:
            self.delete_vocab_config(keyword)
            self.cursor  =   self.db.cursor()
            self.cursor.execute('INSERT INTO vocabulary_config (vocab_size, data_count, keyword) VALUES (%s, %s, %s)', (vocab_size, data_count, keyword,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def update_vocab_config(self, tfidf, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('UPDATE vocabulary_config SET tfidf = %s WHERE keyword = %s', (str(tfidf), keyword,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def select_data_training(self, keyword):
        
        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT data_count, tfidf FROM vocabulary_config WHERE keyword = %s', (keyword,))
            self.db.commit()
            result       =   self.cursor.fetchall()
             
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        if result:
            data_count  = result[0][0]
            data = str(bytes(result[0][1]), 'utf-8').replace("'", '"').replace("\\", "")
            with open('data.json', 'w') as f:
                json.dump(data, f)
            tfidf       = json.loads(data)
        else :
            data_count  = ''
            tfidf       = ''

        return data_count, tfidf

    def select_idf(self, keyword):

        try:
            list_idf     = []
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT idf, word FROM vocabulary WHERE keyword = %s', (keyword,))
            self.db.commit()
            result       =   self.cursor.fetchall()
            
            for data in result:
                dict_idf         = {}
                dict_idf['word'] = data[1]
                dict_idf['idf']  = data[0]
                list_idf.append(dict_idf)
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_idf

    def select_vocabulary(self, keyword):

        try:
            list_vocab      =   []
            self.cursor     =   self.db.cursor()
            self.cursor.execute('SELECT word FROM vocabulary WHERE keyword = %s', (keyword,))
            self.db.commit()
            result          =   self.cursor.fetchall()
            
            for data in result:
                word                = data[0]
                list_vocab.append(word)

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_vocab

    def select_corpus(self):

        try:
            list_vocab      = []
            self.cursor     =   self.db.cursor()
            self.cursor.execute('SELECT keyword, word, idf FROM vocabulary ORDER BY keyword')
            self.db.commit()
            result          =   self.cursor.fetchall()
            
            for data in result:
                dict_corpus             = {}
                keyword                 = data[0]
                word                    = data[1]
                tfidf                   = data[2]
                dict_corpus['keyword']  = keyword
                dict_corpus['word']     = word
                dict_corpus['tfidf']    = tfidf

                list_vocab.append(dict_corpus)

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_vocab

    def delete_vocabulary(self, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM vocabulary WHERE keyword = %s', (keyword,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def save_vocabulary(self, list_word, list_idf,  list_total, keyword):
        self.delete_vocabulary(keyword)

        for index, word in enumerate(list_word):

            try:
                idf          =   list_idf[index]
                total        =   list_total[index]
                self.cursor  =   self.db.cursor()
                self.cursor.execute('INSERT INTO vocabulary (word, idf, total, keyword) VALUES (%s, %s, %s, %s)', (word,  idf, total,  keyword,))
                self.db.commit()

            except Exception as error:
                print(error)
            
            finally:
                self.cursor.close()

    def select_stopword(self):

        try:
            list_stopword   =   []
            self.cursor     =   self.db.cursor()
            self.cursor.execute('SELECT stopword FROM stopword')
            self.db.commit()
            result          =   self.cursor.fetchall()
            
            for data in result:
                dict_stopword               = {}
                stopword                    = data[0]
                dict_stopword['stopword']   = stopword

                list_stopword.append(dict_stopword)

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_stopword

    def add_stopword(self, stopword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('INSERT INTO stopword (stopword) VALUES (%s) ', (stopword,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def edit_stopword(self, stopword_before, stopword_after):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('UPDATE stopword set stopword= %s where stopword= %s ', (stopword_after, stopword_before,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def delete_stopword(self, stopword):
        
        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM stopword WHERE stopword = %s ', (stopword,))
            self.db.commit()

        except Exception as error:
            print(error)
            result      = {'status': 'error', 'message': error }

        finally:
            self.cursor.close()

    def select_kbba(self):
        list_kbba  = []

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT alay, baku FROM kbba')
            self.db.commit()
            result       =   self.cursor.fetchall()

            for data in result:
                dict_kbba           = {}
                alay                = data[0]
                baku                = data[1]
                dict_kbba['alay']   = alay
                dict_kbba['baku']   = baku

                list_kbba.append(dict_kbba)

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_kbba

    def add_kbba(self, alay, baku):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('INSERT INTO kbba (alay, baku) VALUES (%s, %s)', (alay,baku,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def edit_kbba(self,alay_after, baku_after, alay_before, baku_before):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('UPDATE kbba set alay= %s , baku= %s WHERE alay= %s and baku= %s ', (alay_after, baku_after, alay_before, baku_before,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def delete_kbba(self, alay, baku):
        
        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM kbba WHERE alay = %s and baku = %s ', (alay, baku,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def delete_sse(self, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM sse WHERE keyword =  %s', (keyword,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def save_sse(self, sse, keyword):

        try:
            self.delete_sse(keyword)
            self.cursor  =   self.db.cursor()
            self.cursor.execute('INSERT INTO sse (sse, keyword) VALUES (%s, %s)', (sse, keyword,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def select_sse_args(self, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT sse FROM sse WHERE keyword = %s', (keyword,))
            self.db.commit()

            result       =   self.cursor.fetchall()
            result      =   result[0][0]  if result else ''
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return result

    def delete_cluster(self, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM cluster WHERE keyword =  %s', (keyword,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def save_cluster(self, id, keyword, cluster):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('INSERT INTO cluster (id, keyword, cluster) VALUES (%s, %s, %s)', (id, keyword, cluster,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def select_cluster_args(self, keyword):

        try:
            model        =   {}
            self.cursor  =   self.db.cursor()
            self.cursor.execute("SELECT cluster, GROUP_CONCAT(id) as ids FROM cluster WHERE keyword = %s GROUP BY cluster", (keyword,))
            self.db.commit()

            result       =   self.cursor.fetchall()

            for data in result:
                cluster =   data[0]
                ids      =   [x for x in data[1].split(',')] if data[1] else []
                model[cluster] = json.loads(ids)
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return model

    def delete_centroid_cluster(self, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM centroid_model WHERE keyword =  %s ', (keyword,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def save_centroid_cluster(self, centroid, keyword, cluster, cluster_name):

        try:
            centroid     = str(centroid.tolist())
            self.cursor  = self.db.cursor()
            self.cursor.execute('INSERT INTO centroid_model (centroid, keyword, cluster, id_label) VALUES (%s, %s, %s, %s)', (centroid, keyword, cluster, cluster_name,))
            self.db.commit()
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

    def select_centroid_cluster_args(self, keyword):

        try:
            model        =   {}
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT A.cluster, A.centroid FROM centroid_model A  WHERE A.keyword = %s ORDER BY A.cluster', (keyword,))
            self.db.commit()

            result       =   self.cursor.fetchall()
            
            for data in result:
                cluster        =   data[0]
                prepro         =   literal_eval(data[1])
                model[cluster] = prepro
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return model

    def select_cluster_names(self, keyword):

        try:
            model        =   {}
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT A.cluster, B.label FROM centroid_model A  JOIN label_cluster B ON A.id_label=B.id_label WHERE A.keyword = %s ORDER BY A.cluster', (keyword,))
            self.db.commit()

            result       =   self.cursor.fetchall()
            
            for data in result:
                cluster         =   data[0]
                cluster_name    =   data[1]
                model[cluster]  =   cluster_name
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return model

    def select_model_keyword(self):

        try:
            keyword      =   []
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT keyword FROM centroid_model group by keyword ')
            self.db.commit()

            result       =   self.cursor.fetchall()
        
            for data in result:
                keyword.append({'text':data[0],'value':data[0]})

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return keyword

    def select_centroid_cluster(self):

        try:
            list_cent_cluster   =   []
            self.cursor         =   self.db.cursor()
            self.cursor.execute('SELECT A.keyword, A.cluster, C.label, A.centroid FROM centroid_model A  JOIN label_cluster C on A.id_label=C.id_label')
            self.db.commit()

            result              =   self.cursor.fetchall()
            
            for data in result:
                dict_centroid                  =   {}
                dict_centroid['keyword']       =   data[0]
                dict_centroid['cluster']       =   data[1]
                dict_centroid['cluster_name']  =   data[2]
                dict_centroid['centroid']      =   data[3]

                list_cent_cluster.append(dict_centroid)

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_cent_cluster

    def select_cluster(self):

        try:
            list_cluster        =   []
            self.cursor         =   self.db.cursor()
            self.cursor.execute('SELECT B.keyword, B.tweet, D.label FROM cluster A JOIN twitter B ON A.id=B.id JOIN centroid_model C ON A.cluster=C.cluster  AND A.keyword=C.keyword JOIN label_cluster D ON C.id_label=D.id_label ')
            self.db.commit()
            
            result              =   self.cursor.fetchall()
            
            for data in result:
                dict_cluster                  =   {}
                dict_cluster['keyword']       =   data[0]
                dict_cluster['tweet']         =   data[1]
                dict_cluster['cluster_name']  =   data[2]

                list_cluster.append(dict_cluster)

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_cluster

    def select_cluster_plot(self, keyword):

        try:
            datas                =   []
            self.cursor          =   self.db.cursor()
            self.cursor.execute('SELECT D.label,  COUNT(1) jumlah  FROM cluster A JOIN centroid_model B ON A.cluster=B.cluster AND A.keyword=B.keyword JOIN preprocessing C ON A.id=C.id JOIN label_cluster D on B.id_label=D.id_label WHERE A.keyword= %s GROUP BY D.label', (keyword,))
            self.db.commit()

            result               =   self.cursor.fetchall()

            for data in result:
                dict_data               =   {}
                dict_data['label']      =   data[0]
                dict_data['value']      =   data[1]
                datas.append(dict_data)

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()


        return datas

    def select_sse(self):

        try:
            list_sse        =   []
            self.cursor     =   self.db.cursor()
            self.cursor.execute('SELECT keyword, sse FROM sse ')
            self.db.commit()

            result          =   self.cursor.fetchall()
            
            for data in result:
                dict_sse                =   {}
                dict_sse['keyword']     =   data[0]
                dict_sse['sse']         =   data[1]

                list_sse.append(dict_sse)
        
        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_sse

    def select_label(self):

        try:
            list_label      =   []
            self.cursor     =   self.db.cursor()
            self.cursor.execute('SELECT id_label, dec_code, label FROM label_cluster')
            result          =   self.cursor.fetchall()
            self.db.commit()

            for data in result:
                dict_label              = {}
                dict_label['id_label']  = data[0]
                dict_label['dec']       = data[1].encode('ascii').decode('unicode_escape')
                dict_label['label']     = data[2]
                dict_label['decimal']   = re.findall('([0-9]{1,})',data[1])[0]

                list_label.append(dict_label)

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return list_label

    def add_label(self, label, dec):

        try:
            dec             =   "&#"+dec+";"
            self.cursor     =   self.db.cursor()
            self.cursor.execute('INSERT INTO label_cluster (dec_code, label) VALUES (%s, %s) ', (dec, label,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def edit_label(self, id_label, dec_after, label_after):

        try:
            dec_after    =   "&#"+dec_after+";"
            self.cursor  =   self.db.cursor()
            self.cursor.execute('UPDATE label_cluster set dec_code= %s , label= %s where id_label= %s ', (dec_after, label_after, id_label,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def delete_label(self, id_label):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('DELETE FROM label_cluster WHERE id_label = %s ', (id_label,))
            self.db.commit()

        except Exception as error:
            print(error)

        finally:
            self.cursor.close()

    def select_emoticon(self, id_label, keyword):

        try:
            self.cursor  =   self.db.cursor()
            self.cursor.execute('SELECT dec_code FROM label_cluster A JOIN centroid_model B ON A.id_label=B.id_label WHERE B.keyword = %s AND B.cluster= %s', (keyword,id_label,))
            self.db.commit()

            result      =   self.cursor.fetchall()
            result      =   result[0][0].encode('ascii').decode('unicode_escape') if result else ''

        except Exception as error:
            print(error)
        
        finally:
            self.cursor.close()

        return result

    def close_connection(self):
        
        self.db.close()