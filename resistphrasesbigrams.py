import pandas as pd
import nltk
from nltk.corpus import stopwords
from collections import OrderedDict
from nltk.tokenize import RegexpTokenizer
nltk.download('stopwords')

df = pd.read_csv('5StarReviews.csv')
#print(df)

# with open('5StarReviews.csv','r') as myfile:
# 	df = myfile.read()

# reviews = []
# for review in df:
#     reviews.append(str(review))


def prepare_for_processing(df):
    #get body
    col_values = df.loc[:,'reviews_review'].values
    #join list of string into one long str
    col_str = list(col_values)
    col_str = [s if type(s) == str else 'nan' for s in col_str]
    col_str = ' '.join(col_str)
    col_str = col_str.lower()
    #stopwords
    stop_words = set(stopwords.words('english'))
    # tokenize with regex to remove punctuation
    tokenizer = RegexpTokenizer(r'\w+')
    col_tokens = tokenizer.tokenize(col_str)
    
    # filter out stop words
    filtered_tokens = [w for w in col_tokens if not w in stop_words]
    
    return filtered_tokens

def find_token_freq(filtered_tokens):
    fdist = nltk.FreqDist(filtered_tokens)
    tokens_ordered_dict = OrderedDict(sorted(fdist.items(), key=lambda t: t[1], reverse=True))

    return tokens_ordered_dict


def find_bigrams(filtered_tokens):
    fdist_bigram_dict ={}

    tgs = nltk.bigrams(filtered_tokens)
    fdist_bigram = nltk.FreqDist(tgs)

    for k,v in fdist_bigram.items():
        fdist_bigram_dict.update({k:v})
    
    bigram_ordered_dict = OrderedDict(sorted(fdist_bigram_dict.items(), key=lambda t: t[1], reverse=True))
    
    return bigram_ordered_dict


tokens_engine = prepare_for_processing(df)

top_tokens_engine = find_token_freq(tokens_engine)
top_bigrams_engine = find_bigrams(tokens_engine)

#print(tokens_engine)
#print(top_tokens_engine)
print(top_bigrams_engine)


#export
import csv

w = csv.writer(open("output.csv", "w"))
for key, val in top_bigrams_engine.items():
    w.writerow([key, val])

