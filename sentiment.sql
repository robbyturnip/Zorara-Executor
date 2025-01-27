PGDMP     2                    x         	   sentiment    12.4    12.4 &    M           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            N           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            O           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            P           1262    16396 	   sentiment    DATABASE     �   CREATE DATABASE sentiment WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Indonesian_Indonesia.1252' LC_CTYPE = 'Indonesian_Indonesia.1252';
    DROP DATABASE sentiment;
                root    false            �            1259    16403    centroid_model    TABLE     �   CREATE TABLE public.centroid_model (
    id integer,
    keyword character varying(255),
    cluster integer,
    id_label integer,
    centroid bytea
);
 "   DROP TABLE public.centroid_model;
       public         heap    root    false            �            1259    16409    cluster    TABLE     x   CREATE TABLE public.cluster (
    id integer,
    cluster character varying(255),
    keyword character varying(255)
);
    DROP TABLE public.cluster;
       public         heap    root    false            �            1259    16412    kbba    TABLE     h   CREATE TABLE public.kbba (
    alay character varying(255) NOT NULL,
    baku character varying(255)
);
    DROP TABLE public.kbba;
       public         heap    root    false            �            1259    16420    label_cluster    TABLE     �   CREATE TABLE public.label_cluster (
    id_label integer NOT NULL,
    label character varying(255),
    dec_code character varying(255)
);
 !   DROP TABLE public.label_cluster;
       public         heap    root    false            �            1259    16467    label_cluster_id_label_seq    SEQUENCE     �   ALTER TABLE public.label_cluster ALTER COLUMN id_label ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.label_cluster_id_label_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          root    false    206            �            1259    16428    preprocessing    TABLE       CREATE TABLE public.preprocessing (
    id integer,
    keyword character varying(255),
    tweet_lower character varying(4000),
    tweet_regex character varying(4000),
    tweet_stopword character varying(4000),
    tweet_steming character varying(4000),
    tweet_tfidf bytea
);
 !   DROP TABLE public.preprocessing;
       public         heap    root    false            �            1259    16434    sse    TABLE     �   CREATE TABLE public.sse (
    sse double precision,
    training character varying(20),
    k integer,
    keyword character varying(255)
);
    DROP TABLE public.sse;
       public         heap    root    false            �            1259    16437    stopword    TABLE     O   CREATE TABLE public.stopword (
    stopword character varying(255) NOT NULL
);
    DROP TABLE public.stopword;
       public         heap    root    false            �            1259    16442    twitter    TABLE     �   CREATE TABLE public.twitter (
    id integer NOT NULL,
    tweet character varying(4000),
    keyword character varying(255),
    tanggal_tweet date
);
    DROP TABLE public.twitter;
       public         heap    root    false            �            1259    16465    twitter_id_seq    SEQUENCE     �   ALTER TABLE public.twitter ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.twitter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          root    false    210            �            1259    16450 
   user_admin    TABLE     �   CREATE TABLE public.user_admin (
    id integer NOT NULL,
    username character varying(100),
    password character varying(100)
);
    DROP TABLE public.user_admin;
       public         heap    root    false            �            1259    16469    user_id_seq    SEQUENCE     �   ALTER TABLE public.user_admin ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          root    false    211            �            1259    16455 
   vocabulary    TABLE     �   CREATE TABLE public.vocabulary (
    idf character varying(255),
    total character varying(255),
    word character varying(255) NOT NULL,
    keyword character varying(255)
);
    DROP TABLE public.vocabulary;
       public         heap    root    false            �            1259    16397    vocabulary_config    TABLE     �   CREATE TABLE public.vocabulary_config (
    vocab_size integer,
    data_count integer,
    tfidf bytea,
    keyword character varying(255)
);
 %   DROP TABLE public.vocabulary_config;
       public         heap    root    false            >          0    16403    centroid_model 
   TABLE DATA           R   COPY public.centroid_model (id, keyword, cluster, id_label, centroid) FROM stdin;
    public          root    false    203   ,'       ?          0    16409    cluster 
   TABLE DATA           7   COPY public.cluster (id, cluster, keyword) FROM stdin;
    public          root    false    204   I'       @          0    16412    kbba 
   TABLE DATA           *   COPY public.kbba (alay, baku) FROM stdin;
    public          root    false    205   f'       A          0    16420    label_cluster 
   TABLE DATA           B   COPY public.label_cluster (id_label, label, dec_code) FROM stdin;
    public          root    false    206   �H       B          0    16428    preprocessing 
   TABLE DATA           z   COPY public.preprocessing (id, keyword, tweet_lower, tweet_regex, tweet_stopword, tweet_steming, tweet_tfidf) FROM stdin;
    public          root    false    207   �H       C          0    16434    sse 
   TABLE DATA           8   COPY public.sse (sse, training, k, keyword) FROM stdin;
    public          root    false    208   I       D          0    16437    stopword 
   TABLE DATA           ,   COPY public.stopword (stopword) FROM stdin;
    public          root    false    209   I       E          0    16442    twitter 
   TABLE DATA           D   COPY public.twitter (id, tweet, keyword, tanggal_tweet) FROM stdin;
    public          root    false    210   �R       F          0    16450 
   user_admin 
   TABLE DATA           <   COPY public.user_admin (id, username, password) FROM stdin;
    public          root    false    211   �R       G          0    16455 
   vocabulary 
   TABLE DATA           ?   COPY public.vocabulary (idf, total, word, keyword) FROM stdin;
    public          root    false    212   �R       =          0    16397    vocabulary_config 
   TABLE DATA           S   COPY public.vocabulary_config (vocab_size, data_count, tfidf, keyword) FROM stdin;
    public          root    false    202   S       Q           0    0    label_cluster_id_label_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.label_cluster_id_label_seq', 4, true);
          public          root    false    214            R           0    0    twitter_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.twitter_id_seq', 887, true);
          public          root    false    213            S           0    0    user_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.user_id_seq', 1, true);
          public          root    false    215            �
           2606    16464    kbba kbba_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.kbba
    ADD CONSTRAINT kbba_pkey PRIMARY KEY (alay);
 8   ALTER TABLE ONLY public.kbba DROP CONSTRAINT kbba_pkey;
       public            root    false    205            �
           2606    16427     label_cluster label_cluster_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.label_cluster
    ADD CONSTRAINT label_cluster_pkey PRIMARY KEY (id_label);
 J   ALTER TABLE ONLY public.label_cluster DROP CONSTRAINT label_cluster_pkey;
       public            root    false    206            �
           2606    16441    stopword stopword_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.stopword
    ADD CONSTRAINT stopword_pkey PRIMARY KEY (stopword);
 @   ALTER TABLE ONLY public.stopword DROP CONSTRAINT stopword_pkey;
       public            root    false    209            �
           2606    16449    twitter twitter_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.twitter
    ADD CONSTRAINT twitter_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.twitter DROP CONSTRAINT twitter_pkey;
       public            root    false    210            �
           2606    16454    user_admin user_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.user_admin
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY public.user_admin DROP CONSTRAINT user_pkey;
       public            root    false    211            �
           2606    16462    vocabulary vocabulary_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.vocabulary
    ADD CONSTRAINT vocabulary_pkey PRIMARY KEY (word);
 D   ALTER TABLE ONLY public.vocabulary DROP CONSTRAINT vocabulary_pkey;
       public            root    false    212            >      x������ � �      ?      x������ � �      @      x�m|͎�:��ھ
�9��|��e�\@��EV���U�-�~���<%�\=�s�DR�,QERt��ں��Ym���&ӫQ��uj�G����z<:��a�K�E��CS�&�©�
"7�΀>����ç

3���ZT�tH�P�����h�x��g��1��Eu��哥j��?��My3j����S;*ZS[�
�zSnx�YQ�j�l�b��N�M4U6����
䣑�Jr��6F�*��ȗ��e(nUfR�9w����Z9��V,��:)-V
�+@��U�@S��Du� �9�G@f,�&�'�_���	7$���,��,6,����ީ/���(��4U(������d�h��;����3���Z�K�g]����?/�F�R�g԰�k��8�0��%�ZS�Nc|C���RL�<����y�����Nj7��A����$5����?}v��+�@������èg��|�T%E ���T�d�a��"��K�*�8`���)��}!�W���� 7G��ڏ�%�o��<TP�Q(F� �L��Z�oD�$Ȗ�G�|r�I��J0o�
=-��IP�h!�ܽ�zj������&9\��W��F�z= �;X����� 9�J��F�������	b[��/�8�3��S�ң����L]u� �_X� �ҏ;ܠ��~�cc=@��c]���6�g&�7r��P�˒ uF�:#��_��tx_xB��Ixx���0���r#�.�C���O���p2� Ў�*Rk�����8X��Hd3,�֭Xg�eh�Z^�4&��L�dvl�Q���,��2�S�~^�h�U��3h��d~=��1s�P̓-�����a�V�<R��v��p���W�� ,��C~�Ѻ�	,F�+D�!�H�Mf;�P�@J :Y=�z�s��8�0N��;M⵴��p|���*Z��X�UYf�\ �#eEJ�؀|��@YIi�Pl����
����/�l;�7���[*����-N�_؈5l^(��̎�	�<�sO�գ�_<�����z�� �Øj��"�Ak�����J�
��S_��9��S	��Q�M�l�r|X�&�G�N���	b��li�A��J��Y�<vs��U`$Y��Pwi���ތ-������.�IP��m1|a匩��׬3�6����e/̖��w �����q�;c(T,EV���(y�%�
���o�*HC`��Fq�y�}��<J!�}a��5�/�oW
��߫�́�7�&�l�#q`l'��&��(�!��<�{��N��j5�7�:�1x�A ��q�P8�
b��n���>���.<d�p���8Dhђ�?r����?V@�9M��p � i8^�xj'mOZ��`���Q�3}���ֵ�4Y`�p�5@�t��	ۅ��?`�b�a{�,�����
� ��?�����Cs�xp��3ߥ�-��8����q������3�l�dcTs7����P��q�R��:�q��l��<q�ě�&�t4/�a�z���m���і�`�E��j���X��,|�����9���G�{�;�P�/dӜ��d��Ö �C%q�z;tgd�����q�C�����Ny'�.���F|QE�@���?�{֗�<�z�ݑ'b�?3��Y�a5��D�t�,�t�a#��0���F0_ t��E^ C��֍���䃴��&0�fi�m���@��c;肁[e ��+Ax����&m��X�y�$���D�vR3D%ӿ¿n�,W��i���W�D�h(���v�G}�D�X>#��$�-B�������Y����Y���y��Zg�Cユ8k�}��*P!Rd�F��6��+�X<���U��M�&@��|'���r�!~B%N��Yx�0x�5��;�T��!����k���I��{��P֮�����hݮl7&��@-L8�<y�֤���7�m`����\��'� 	����i�ӂFi��\8��O��iL!ʖ�Ǯ8 bY�ԛb�$��+	Ӆ�nJ/Y�0)��%0��2�\�-�2��p���Y���h�����^O�� �+3,�^Ͼӫ'm�����]!`��"�7�[��Ъ�@��l�U��м]$$���5�?���L�çf�*	0\�;�����m��_gG��ӣ�ix��x�ot�яӿS�z��o=ܳ��;���~��ϑ�=ŧ��������P��S����i�k�-��Ӧ�N����nd3�?������s3~���B��Cܰ�tg��~�ό�5�؄3��X�)� O]����7�b�̳"���a��.�b����⾛ҁ�
5
�����	l�0Վ���i��m� ��ͰUIu 1����ɮ�)adw���q�d>��qj���g�6�Sx� ��8��l�f�Zx����ئpU���s��^L�L+�Ɣn�@ �|�x�����0�芰 �K�FX`��N"?��������>�k�����a���~�;)l�lU53�3Wg���w�g� İ�*F6�h/ub8�O���//,�I��D���cG�M(�:��wW� ;�F��٨��a�}����:��́�Pr_���w< ���;d��u�I|�e�V��2]|�.�p��hV%����u�F7��bM��Q4�|�vG,�6���8nq�6����Uۅ��B�H^�(�Q��04=��Dzy�iaDU�~���@��S���&Xβo!��^t�h���s�]�EL�d�%\!h��g�h�bJ3��TrjqX���K���(-O�
z((��F��.��3�i��h��/���1�$_\}�
$�� Ȏ��U��ݩL��H>NԅX�c׀�_����F��`b�� �������؛��X�MN,�%���¥�,�>�n;O�#(杀Ǻ��}�8�u�N��0������QkVѬ���_�i׽�<�E�v���7�SX �h�i�hf����s{㯀���$��؅2�v_*�C+���KMh�NO�P����F^�<U(�}��e0$<�Qfl�Z�t}B��=j�R�5p�x�.I�R������U|N�5JsV�ާ������?Q#VϹ���D��L`郘�bx��_x(���Mh�<}:>���s{��B�c��4�P"vϴ�I��>�������$H�8������
�y�x�Pco�z�J� �h�;�,b�h���l��f.h8F�& ~���s^��p0��!c��Ԟ�L��&���_/�/Z�V]�A{��q9�K���\w�.rm%X�����J�Z׌W�*!����orZ�K���s��37p;�a�� P"��W��_�T�u�%u1`��<�x\0s՘�^ch��&�V�z�]V]:�e;�rQfG%KQ����ٔ����qB�Q`哫�x;Co�歞pr�uSN%�� 2<ҌI��OB���`4Z�O)CX��<��2'�އ�%�@���$���a%/;)�M/��B�Fkeegb!n�j t�J$M@+�AaR��&:�[���LE�VV�f���/�-��d.m�mJY�X�p��u����/���rwR�`1g�6G"m�����Z�3�ƭ��8�> f̮����Nn� d�,c�W(j�~sm��2l'B�߯vmCx�0�eO"�g���,*���f�2̕�d�E�#�|C��F`��}���P�YC;I  ��v�`�T�O�\��O�Ix=�����X� ����6�\��Ô�0�u �/��� �ԉ�dh7����^�V�	V�:��ѡ���p7G���=ෘ��'�����;� ��?���CÙ�Զ���0{/�G��ɶ���)�aB����j��2�a&�g�X�+��]
�sB�M���i��@Z3+4�`1�YG��Pko�KEe��mˀ�}%�o6�iB͵����>_j�wX�(J��e�]���ѼO�ؔ�W�%���p�Y�����w�`�Jt�:Ӑ���N�V��gq��to�V�Q}�8    �I�q ��� ;gx�:=��JZ��I�u�����M��7�����7���OjAPclss�]s��l1CMc{YeF�-�K�2��/p9�қ�V	,@�6�3I�$�4�{2o^�X�'�bi`e�\"b7d{[��9�X:o�y�(�� �?p��;��K�P��঳ U+��ݰ���s�m��g�k^��MKN�4�������GR_w]��xr�;�+���0uU0Ȗ���5�v|��4�#a�$'���z���/�^���㢛v�BOꘉ���:�;
�by�� �YCh��{�Փ�J%�r�z�r)�$�}����W��v���cV1��}�?'n�*����>�q���9��?jC�K�k���HcCxO����%<�0�R7�P���|����	�t��DKw`b~�\���'��(�j1TP��D�M]�	�b�]K�Z�Rn{����=t�0H����u̐戠�W���%Wf�P�P�`�pZ@�&�}�_`{��hN�:�0�8f{G "����i�����$V#yM���W�d���އ%��s��s�`���x� �7��|�Ɖ��y�WJ���(@S�,Q�
��6��:��7Vl�+�8k]Fϳx�}��g,/��Ȁ�jU�]��-$������ug�j����7\1����_�/�-Ch��G��c�I�2���?�m�(E���YL�53c����X3d��-MidY��D�y��Q��C)B^`��+��/8�����>)f�ŭ�˥�hۿU�D�CG���d| �4�k��M
��DG.M�{�&�u��*t�gE�yY���R��\H��P8�T,Zʾ�y�	���n��{dS��k�Bm�*~�(&���cC����0aT|)V��5V�3ԝ�� ��w!�_ؾs$�9���%�T�����QϳT<F9��6Jz}��v� �i-+��w.� @�#�����A���Ǻ��ao���o�c�|�33t��2n�W��J��Bw��; >,�^�I���n㍷WŚ�7��)G�6K�5u0�6���!�e�$_gϔB����/�\B�6[yU�R�
f\���a�{Kc�n��C��
�� -ۭ�j��X:"Dʮ�K��a*�W��PI��:��H���+����d�:�CrC�8IT\�@*�$�:��<����܉�K��'��1������I_���uI�"@�M�*�_[z��Q@�\ !y��(��9�@��Γlo�He;PY��Zu���
I@��b�
>� �q�qI���T�ȕ����G(*A��E��S�W@H�4������ܮiﷴP'�����z9�7^��X�}� �h�"c��d��L���X�*����m����-"�j̓�U���B+]�@�?�;ӱ>�C�J�BnZ�4.�2�"&�����"��D�`�^z���$�l8�R����!K����s���U�L�QO���%Pd��\��B�x,+��[�g�P�&�t󃿄��MjG�c`��-�o��u�~Q^��n�n���a"P_�ӥ�����%��)�0��3Qȼ�"�'������$c�H�(��|�J��%�sQv� ĝ�$>�P#����B�֪O�-e7�;�*����]�<��Q� �P�]��O�!P���{j���������'�M(�{��p��ޯ��D�ɘ��&tщC��x��]�iyH����G/�F-w�'zs�6'���� ��1�<��n��K^�ۙ��#s}0L���S�����7o'�O8�a�2���A8�L9�Ȑ=��g���*�>3`�}/_������b��hu��N.���T���r�S��@�%�E���d�F;�#�6)3��	l
x3uIR,�b;^0����-�2���J0�Iŏ]r��y�
6�����3[���fx�9�$���Ilm�'��.@�*����]��k� �k 6	�|oqƼ�g�|ӑ2)�S&���e��M.���`�����%y�םN�l��^�����p���V�S�r���H�("ϒq8�\�EzȬY�kn.X&�	��}�M��	�0��4�Y5�����n��&g@�$Q�Qn�7�'��b�Ԭb�����S�Gi���G`�����א�/��
�1W�D�f���f(��10���JV�������÷��n@��)-�}��`~���4�7�����V�ߛ��_�/3?J�ln���0�?T)]��2<�M߻�L-5eq@�����3M9�:��w�� �b�����x�k�^̰)��#O�[�an���Ta��"+,�����&)���e�S�pHP��y�a��L��9B�U0 � :��w:�<���g.��E�d7˝]�=���C��M$�xڢ�kk�\k��g��cG@>�5d��0ꁞ�!����d��%�7��M�lbb1���A��칡�>��'�����`��#�;���I�=觶�/�`��0A
P�����D�N�v���]$�{�`�˷4�d��(i9D�*�/���Q�����Xk`8:�O�p~`�8D�=S�}֑0l�KM�L�.x'��z�}:���#�µj���e7Y�x��3�Tk�ig�K�8��V	�p�@T�Dl8�!�F�>\2}@��ĥ�#?\�DKgH������N�^����T>�u��0t�5��3HO��5	�8�d� �U(ò-�Օ��G}!	R��H�	m��@�4+�ͨ�厥|=(�L4�����B��J�_�ǹ� S=�L����V��2�[���q��o�#]�;��p��\�c����T�qj��q����8m�����o���gT�XF���0e~��$F��
�߆�g=B �w~(xL|��AT�/X{1�!m,�W4Ԥ2��1���i��)��P��Q
a^�Q�Dc`R��Q���=Ih��mo�����0�j|���X��

2��E�L��8��8�v �eXL���,�u�8�}�y�L���<����(~�!@g�����oZ�b:�@���TdQ�U'���o��]�Ee��Z� �l`��/���s���j�}b)a�����{�>��v*��e+�^u��]��g�� R�Ȣ��Ոǲ�Xq�E'�QI|�·J�3"\ν���v�	���*����^R��}W�r�\�u	ۚE�2���
X�=�4�4|n��D8���}����T�~1cI���r���,#��t�G[>�Rqy�P���L��K
x�� ��<�s�> ����%�%���Q�͎�8�1g_s�?��_zu��������v��.�0z̻�$�OQT��8����R5��>"��ۃ�ܽ�߻E3�P3�^�J�h*aZ ڽC�r�ˍP �
�X
�Y���>��#��\@�K�g�P��މ�o�//,d.3�6 o��!L�������+�"��\ ��6����h�R!���L�^�����G p�C$-�\�K>�c��-���%;D�Oc��-?Ie"qo�3f'���[23?(ё�ߺ�J��#�J��A�%XÄvFC'� ��I�����]"����������w�D��-����ڕ����6��QV�`�������~��k����GJ�$����6L>:��OvƘ-/�1`�ʒ@�;�ݾ�<%<"��b���� ��ǒ�kc�N��w8]B.L�(Kۍ��D�&�'�}��=��^���H7x��8vw$h�0�-�A@~��˝}ڋ���ۛ~~�S�^�%:�z�v&�"���$O��t2Kz۷��}- �Y��
�����o����?'O�jE'�/�A�$:�B��%�{+�E�I0S P�ڤ��}�J"�C,��E�ʍ�,�pb�/�R�TE~p�1�<�]��`I��K�/R�c|/13U�6�t*��R����.�϶�4��L��3?/h��z��X�N~�8�C~yJ��?��C(�P�1������T&�{o>��WP 6 �ﮱ���n�l+�_��M��%?M���m���c�_<7�m Sƫ�   G�ûX�p"�_^5@F E<��o5�O���L,Wәa������a��O�A|�q`��Q�O��A��0)���?x2��#	&f#�i�$�Ind�йBs/��yq�����y�*�3W��(񎀿��<,ߋ�z#�/4}vcQ���HˋL�߆�]���
� PL��\ȵk���[*��
�`��Q"���~�׏�����	)<�Y�)N���t��|
{�[��)��:D�H��w.�g��<�ۛ��־�z���3��P�o*�������_�)�      A   :   x�3��/�,�L�TS64�052��2��K-)J́	YXs��a�,��L��b���� l�      B      x������ � �      C      x������ � �      D   �	  x�E�[��
�������\Lb�11�֟�f���&DTD�8�HQ������-�P�"��`>� ��_�����jj�)�b7k�����G�:�"�u��H$}���ķP����dqsZʫ���0ɋt�C��4~�4c!R���m��8���v�O:H���Oo4����}�mh�=��t��}�H��IG�����g�\�޲*|���?]6SQv
yHV��-��>�rV�/��Ɵ�4Q/��9���^�`��2KgcU�*��(�[5�.�Od�d���o��`j7�������Ȝcw;�vq�2̛����<�U������nNyX[0k2If��ɲ���tŨ��vʁ���m[dU��OHvN�7|,�$Ɇt
[�.3o�>���!��ϙZ$?�4>�o�}����G���h"�^^_��e6&;��M�Ci��&z�)����������*�7E���t{�;l����5l�$X��R���~��ל6IȆ�|Z�U~��啒��{���Ed����L�{H�c��8
�3]��qn]�;ƨa�f0)7D�M�S�{�!&g��Z1�V{���X��#���ڶ���c�����&8[ʅ�~�}𙦵��ƴ#J��Zmw�.u��M�YLk�t���n���t�<�{۸��Β�+�$�XAI�37լ��EM���mA��w�$b��F�ը��Z�7
o��D�pu�~�
Q��ة��ڃ��v���mF֩�X��j/�j��7����d*�"��[����;�i��+�2Q+�⩤�Gs�*���j���,P��^��z�p�\jw�/dSK� ��Θ��M.�I�����o��uط�����w��(~���ዕO�t��ȁ� L*�v��;y��Z��;���}�O=��'��g�Im'i;)X���<���MPU�t>w��W�%J8~<�����}
���WTk+�)ԣ�X�fB�%�!I��u��a��,���>�!&6��>=�.���ҝ�`<~����~�q���Yr����w�)�����Y.䑐�9�OS�sڻ���/X�I�g|i�yV�/�����b����
����B�2�+�����f����Fr)Im�؜�������|��2tJm�3�gB����=&��i��O�c��pG2�>����|�L�Js���w�[�ӥ�7���o�<3|��ݥ�ٱ�`��[7b������=��� �>�'�؉���N2�ds����lZ�E���~�B�rQ�**c
G�c�Vx�F�W	kH{���0, ����'�EqS</��'�hEYR6�-�!?ʞR�w�Ph\(Wʍ2P��(Oʋ�|(_**��JBM���Jx�S�T�H5Q�B�TU�کaD��ꢺ���C�%uE-�Q7�-� ^O=P���s�J�Q�Z�P�𤾨o����
\��p5N��E�y\�p#n��-���^�v܁8<q��=�����)i*����H��t4���hF��f�YhV��&��4M�9i.���yi�m�%mE[�:چV����hGډv�]hWڍ6��m�=i/ڛ��}1TJW�Ut�p(]C��I��z:�T�ۉn�[�V��.�	�t��n���Eе�W����Eo�Kߣ����~�0�_�> ��r�yO������4�/�+����7�-� ���F��~�t]�W��>����,�I����ˀAВ�b��VXQ���gШ��� ��0�C`�����b���Q���d�k�DƆQ�QhQ��g��(l�0���`��x`�d�oƇ�ŠS�T1�B\L���0��Y�40�L2�Z�V��)0�L���k'��t3=L/ɘK抹fv�*2�`�0Z�<0���,�yc�;���O���c~YX
���b�YK�Ҳ�y�!�ed�Xf�,K`<X"��r��,��*��Z�V��pk�*0('<׳����0��*��U�P��d=Y/֛�a}��
���b��[�ֲul��g�F��mf[�V6M	l;���N���f{�^j��$T����%��zBO#a"̄��6�f����pn�Cx�P����k�R��]��({�.�"P&�N���m삉��F��{�_�7������TrT��Gái����PW9&��c�Po�8����_����p�D�:cI��5�b�z����=�[qD�W}+.�o����v�n���ċx���Yp��g��8Ζ����=��9rN�3�¹rn��s�<8#�<\�7���r��q��U\5��j�Z.�I5ɞK}Ur⚹��k�
\;����yr����p���w�]q�܎��n�;n��s�#��=s/�+���w�;r����<�/O�S��<���Q;�x��{��g�x����g�	<;��#p�\<7����_�[�V�5��mx[ގ������;�μ�ʻ�ޝ����'��{�>�/���?��v      E      x������ � �      F      x�3�,��/\1z\\\ .~      G      x������ � �      =      x������ � �     