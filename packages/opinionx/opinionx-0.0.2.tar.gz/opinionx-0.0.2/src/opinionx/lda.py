from gensim import corpora, models
import gensim
from quickcsv.file import *
import jieba

def lda_shell(
        csv_path,
        id_field="file_id",
        text_field="text",
# ============ begin configure ====================
    NUM_TOPICS = 6,
    NUM_WORDS = 20,
    FIG_V_NUM = 2,
    FIG_H_NUM = 3,
    WC_MAX_WORDS = 20,
    NUM_PASS = 5,
    # ============ end configure ======================
        list_dictionary_files=None,
        stopwords_path="",
        font_path='utils/fonts/SimHei.ttf',
        output_figure_path=""
):

    if list_dictionary_files!=None:
        for file in list_dictionary_files:
            jieba.load_userdict(file)

    list_item = qc_read(csv_path)
    dict_doc = {}
    list_result = []
    for item in list_item:
        file_id = item[id_field]
        text = item[text_field]
        if file_id not in dict_doc.keys():
            dict_doc[file_id] = [text]
        else:
            dict_doc[file_id].append(text)
    list_doc = []
    for k in dict_doc.keys():
        list_doc.append('\n'.join(dict_doc[k]))

    print("document number: ", len(list_doc))

    # qc_write("results/result_expert.csv",list_result)
    stopwords=[]
    if stopwords_path!="":
        stopwords = [w.strip() for w in open(stopwords_path, 'r', encoding='utf-8').readlines()
                 if w.strip() != ""]


    # load data
    # dict_dataset=pickle.load(open("datasets/weibo_vae_dataset_prepared_with_domain.pickle", "rb"))

    # compile sample documents into a list
    # doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
    import jieba.posseg as pseg
    doc_set = []
    for doc in list_doc:
        # list_words=jieba.cut(doc,cut_all=False)
        list_words = pseg.cut(doc)
        list_w = []
        for w, f in list_words:
            if 'n' in f:
                if w not in stopwords:
                    list_w.append(w)
        # print(list_w)
        doc_set.append(list_w)

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for tokens in doc_set:
        # clean and tokenize document string

        # stem tokens
        # stemmed_tokens = [p_stemmer.stem(i) for i in tokens]

        # add tokens to list
        texts.append(tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=NUM_PASS)

    # print keywords
    topics = ldamodel.print_topics(num_words=NUM_WORDS, num_topics=NUM_TOPICS)
    for topic in topics:
        print(topic)

    # 1. Wordcloud of Top N words in each topic
    from matplotlib import pyplot as plt
    from wordcloud import WordCloud, STOPWORDS
    import matplotlib.colors as mcolors
    import matplotlib
    matplotlib.rcParams['font.family'] = 'SimHei'

    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

    cloud = WordCloud(
        background_color='white',
        width=2500,
        height=1800,
        max_words=WC_MAX_WORDS,
        colormap='tab10',
        color_func=lambda *args, **kwargs: cols[i],
        prefer_horizontal=1.0, font_path=font_path)

    topics = ldamodel.show_topics(formatted=False, num_topics=NUM_TOPICS, num_words=NUM_WORDS)

    fig, axes = plt.subplots(FIG_V_NUM, FIG_H_NUM, figsize=(10, 10), sharex=True, sharey=True)

    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        plt.gca().imshow(cloud)
        plt.gca().set_title('Topic ' + str((i + 1)), fontdict=dict(size=16))
        plt.gca().axis('off')

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.axis('off')
    plt.margins(x=0, y=0)
    plt.tight_layout()
    if output_figure_path!="":
        plt.savefig(output_figure_path, dpi=600)

    plt.show()