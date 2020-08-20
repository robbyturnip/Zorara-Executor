import os
import copy
import math
import json
import math
import concurrent.futures
import numpy               as np
from sklearn.decomposition import TruncatedSVD
from app.models            import Model
from app.tfidf             import TfIdf
from app.preprocessing     import Preprocessing

class KMeans():

    def __init__(self, model):
        self.preprocessing =  Preprocessing(model)
        self.model         =  model
        self.tf_idf        =  TfIdf(model)

    def mm_normalize(self, data):
        result = []
        data    = np.array(data)

        svd     = TruncatedSVD(n_components=5,n_iter=5)
        data    = svd.fit_transform(data)
        data    = data.tolist()

        # for a in data:
        #     list_cosine = []
        #     for b in data:
        #         cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
        #         list_cosine.append(cos_sim)

        #     result.append(list_cosine)

        return data

    def mm_normalize_predict(self, data, list_data_train):
        list_cosine = []
        result      = []

        svd             = TruncatedSVD(n_components=5,n_iter=5)
        svd.fit(list_data_train)
        list_data_train = svd.transform(list_data_train)
        a               = svd.transform(data)
        a               = a.tolist()

        # for b in list_data_train:
        #     b       = b.tolist()
        #     cos_sim = np.dot(data, b)/(np.linalg.norm(data)*np.linalg.norm(b))
        #     list_cosine.append(cos_sim.tolist()[0])

        return list_cosine

    def manhatan(self, data_1, data_2):

        return sum([abs(data_1[i]-data_2[i]) for i in range(len(data_2))])

    def euclidean(self, data_1, data_2):

        return math.sqrt(sum([(data_1[i]-data_2[i])**2 for i in range(len(data_2))]))

    def jacard(self, data_1, data_2):
        inter= list(set(data_1) & set(data_2))
        I=len(inter)
        union= list(set(data_1) | set(data_2))
        U=len(union)
        return round(1-(float(I)/U),4)

    def up_date(self, cluster, all_data, centroid_before, k):
        new_centroid    =   []

        for centorid in range(k):
            tweet_dalam_kelas_sekarang      = []

            for index, kelas in enumerate(cluster):

                if int(kelas) == int(centorid):
                    tweet_dalam_kelas_sekarang.append(all_data[index])

            centroid_tweet_baru = np.array(tweet_dalam_kelas_sekarang).mean(axis=0) if tweet_dalam_kelas_sekarang else []

            if centroid_tweet_baru == []:
                centroid_tweet_baru = centroid_before[centorid]

            new_centroid.append(centroid_tweet_baru)


        return new_centroid

    def hitung_sse(self, tweet1, centroid):
        result = 0

        result = result + math.pow(self.manhatan(tweet1, centroid),2)

        return result

    def sse(self, keyword, cluster, k, centroid_text, all_data):
        sse_total   =   0

        for centroid in range(k):
            tweet_dalam_kelas_sekarang      = []
            centroid_now = centroid_text[centroid]
            for index, kelas in enumerate(cluster):

                if kelas == centroid:
                    tweet_dalam_kelas_sekarang.append(all_data[index])

            with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:

                myfuture = {executor.submit(self.hitung_sse, tweet1, centroid_now) : tweet1 for tweet1 in tweet_dalam_kelas_sekarang}

                for future in concurrent.futures.as_completed(myfuture):
                    sse_total = sse_total + future.result()


        self.write_sse(sse_total, keyword)

        return sse_total

    def output(self, id, keyword, cluster, k):
        dict_final = {}

        for centorid in range(k):
            id_tweet_dalam_kelas_sekarang   = []

            for index2, kelas in enumerate(cluster):
                if kelas == centorid:
                    id_tweet_dalam_kelas_sekarang.append(id[index2])

            dict_final[centorid + 1]=id_tweet_dalam_kelas_sekarang

        self.write_cluster(dict_final, keyword)

    def read_sse(self, keyword):
        sse = self.model.select_sse_args(keyword)

        return sse

    def write_sse(self, data, keyword):

        self.model.save_sse(data, keyword)

    def read_model(self, keyword):
        model = self.model.select_centroid_cluster_args(keyword)

        return model

    def write_model(self, data, cluster, keyword):
        self.model.delete_centroid_cluster(keyword)

        for key, value in data.items():
            cluster_name   =    cluster[key-1]
            self.model.save_centroid_cluster(value, keyword, key, cluster_name)

    def read_cluster(self, keyword):
        cluster_name = self.model.select_cluster_args(keyword)

        return cluster_name

    def write_cluster(self, data, keyword):

        self.model.delete_cluster(keyword)

        for key, value in data.items():

            for i in value:
                self.model.save_cluster(i, keyword, key)

    def fit(self, keyword, id, centroids, cluster_name, all_data, jumlah_tweet, k = 3, iterasi=100):
        centroid_outer  = []
        centroid_inner  = []
        cluster_outer   = []
        cluster_inner   = []
        dict_model_outer= {}
        dict_model_inner= {}
        sse_outer       = 0
        sse_inner       = 0
        all_data        = self.mm_normalize(all_data)

        centroid_text = [all_data[(id.index(int(x)))] for x in centroids]

        for iterat in range(0,int(iterasi)):
            print("iterasi ke ->   ",iterat)
            cluster = []

            for i in range(jumlah_tweet):
                jarak_antar_centorid   = [self.manhatan(all_data[i], centroid_text[j]) for j in range(k)]

                kelas_terdekat         = jarak_antar_centorid.index(min(jarak_antar_centorid))
                cluster.append(kelas_terdekat)

            print(cluster)

            update_centroid_terbaru     = self.up_date(cluster, all_data, centroid_text, k)
            centroid_text               = copy.deepcopy(update_centroid_terbaru)

            dict_model_inner           = {}
            for index, data in enumerate(centroid_text):
                dict_model_inner[index+1]  = data

            sse_inner                   = self.sse(keyword, cluster, k, centroid_text, all_data)

            if sse_inner >= sse_outer and sse_outer !=0:
                break;

            else:
                cluster_outer               = copy.deepcopy(cluster)
                dict_model_outer            = copy.deepcopy(dict_model_inner)
                sse_outer                   = copy.deepcopy(sse_inner)

        self.write_model(dict_model_outer, cluster_name, keyword)
        self.clustering = self.output(id, keyword, cluster_outer, k)
        self.sse(keyword, cluster_outer, k, centroid_text, all_data)

        return 0

    def predict(self, data, keyword):

        try:
            total_tweets, train_data    = self.model.select_data_training(keyword)
            list_preprocessing          = [x['tfidf'] for x in train_data]
            data_lower, data_regex, data_stopword, data_stemming    = self.preprocessing.cleansing(data)
            data         = self.preprocessing.tokennizing(data_stemming)
            data         = [self.tf_idf.tf_idf(data, keyword)]
            data         = self.mm_normalize_predict(data, list_preprocessing)
            model        = self.read_model(keyword)
            model_nm     = self.model.select_cluster_names(keyword)
            k            = len(model)
            d            = [self.manhatan(data, model.get(j+1)) for j in range(k)]
            cluster      = d.index(min(d)) + 1
            cluster_name = model_nm.get(cluster)
            emoticon     = self.model.select_emoticon(cluster, keyword)
        except Exception as error:
            print(error)
        finally:
            self.model.close_connection()

        return cluster_name, emoticon
