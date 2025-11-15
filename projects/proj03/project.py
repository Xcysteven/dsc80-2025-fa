# project.py


import pandas as pd
import numpy as np
from pathlib import Path
import re
import requests
import time


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_book(url):
    response =  requests.get(url).text.replace('\r\n', '\n')
    start = response.find('*** START OF THE PROJECT GUTENBERG EBOOK')
    start_content_index = response.find('\n', start)
    end = response.find('*** END OF THE PROJECT GUTENBERG EBOOK', start_content_index)

    return response[start_content_index:end]


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def tokenize(book_string):
    temp_str = re.sub(r'\n{2,}', '\x03 \x02', book_string).replace('\n', ' ')
    temp_str = re.sub(r'([^A-Za-z0-9_\s])', r' \1 ', temp_str).split()
    if temp_str[-1] == '\x02':
        temp_str = temp_str[:-1]
    if temp_str[-1] != '\x03':
        temp_str = temp_str + ['\x03']
    if temp_str[0] == '\x03':
        temp_str = temp_str[1:]
    if temp_str[0] != '\x02':
        temp_str = ['\x02'] + temp_str
    return temp_str


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


class UniformLM(object):


    def __init__(self, tokens):
        self.mdl = self.train(tokens)
        self.tokens = tokens
        
    def train(self, tokens):
        unique_token_list = set(tokens)
        return pd.Series(index=unique_token_list, data=(np.zeros(len(unique_token_list))+ 1 / len(unique_token_list)))
    
    def probability(self, words):
        if not set(words).issubset(self.mdl.index):
            return 0
        return self.mdl.values[0] ** len(words)
        
    def sample(self, M):
        return " ".join(np.random.choice(list(set(self.tokens)), M, replace = True))


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


class UnigramLM(object):
    
    def __init__(self, tokens):
        self.mdl = self.train(tokens)
        self.tokens = tokens
    
    def train(self, tokens):
        tokens_with_prob = pd.Series(tokens).value_counts() / len(tokens)
        return tokens_with_prob
    
    def probability(self, words):
        if not set(words).issubset(self.mdl.index):
            return 0
        prob = 1
        for i in words:
            prob = prob * self.mdl.loc[i]
        return prob
        
    def sample(self, M):
         return " ".join(np.random.choice(self.mdl.index, p = self.mdl.values, size=M))


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


class NGramLM(object):
    
    def __init__(self, N, tokens):
        # You don't need to edit the constructor,
        # but you should understand how it works!
        
        self.N = N

        ngrams = self.create_ngrams(tokens)
        
        self.ngrams = ngrams
        self.mdl = self.train(ngrams)
        self.mdl_dict = pd.Series(self.mdl.prob.values, index=self.mdl.ngram).to_dict()

        if N < 2:
            raise Exception('N must be greater than 1')
        elif N == 2:
            self.prev_mdl = UnigramLM(tokens)
        else:
            self.prev_mdl = NGramLM(N-1, tokens)

    def create_ngrams(self, tokens):
        return [tuple([tokens[i+k] for k in np.arange(self.N)]) for i in np.arange(len(tokens) - self.N + 1)]
        
    def train(self, ngrams):
        n1grams = [i[:-1] for i in ngrams]
        n1grams_counts = pd.Series(n1grams).value_counts()
        ngram_counts = pd.Series(ngrams).value_counts()
        
        df = ngram_counts.reset_index()
        df = df.rename(columns={'index': 'ngram'})

        df['n1gram'] = df['ngram'].apply(lambda x: x[:-1])
        df['c_n1gram'] = df['n1gram'].map(n1grams_counts)
        df['prob'] = df['count'] / df['c_n1gram']
        df = df.get(['ngram', 'n1gram', 'prob'])
        return df
    
    def probability(self, words):
        if len(words) < self.N:
            return self.prev_mdl.probability(words)
        else:
            curr_n = tuple(words[-self.N:])
            curr_prob = self.mdl_dict.get(curr_n, 0)
            if curr_prob == 0:
                return 0

            next_words = words[:-1]
            next_prob = self.probability(next_words)

            return curr_prob * next_prob

    

    def sample(self, M):
        start = ['\x02']
        for i in np.arange(1, M):
            start.append(self.helper(start))
        start.append('\x03')
        return " ".join(start)
                
    
    def helper(self, curr_list):
        if self.N > 2:
            if len(curr_list) < self.N - 1:
                return self.prev_mdl.helper(curr_list)
            else:
                curr_info = tuple(curr_list[-(self.N - 1):])
                curr_options = self.mdl[self.mdl['n1gram'] == curr_info]
                
                if curr_options.empty:
                    return '\x03'
                next_words = curr_options['ngram'].apply(lambda x: x[-1]).values
                probs = curr_options['prob'].values
                return np.random.choice(next_words, p=probs)

        else: 
            curr_info = tuple(curr_list[-(self.N - 1):]) 
            curr_options = self.mdl[self.mdl['n1gram'] == curr_info]

            if curr_options.empty:
                return '\x03'
            next_words = curr_options['ngram'].apply(lambda x: x[-1]).values
            probs = curr_options['prob'].values
            return np.random.choice(next_words, p=probs)
 

 
