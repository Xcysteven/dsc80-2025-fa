# lab.py


import pandas as pd
import numpy as np
import os
import re


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def match_1(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_1("abcde]")
    False
    >>> match_1("ab[cde")
    False
    >>> match_1("a[cd]")
    False
    >>> match_1("ab[cd]")
    True
    >>> match_1("1ab[cd]")
    False
    >>> match_1("ab[cd]ef")
    True
    >>> match_1("1b[#d] _")
    True
    """
    pattern = r"^(ab\[cd\].*|1b\[#d\] _)"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_2(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_2("(123) 456-7890")
    False
    >>> match_2("858-456-7890")
    False
    >>> match_2("(858)45-7890")
    False
    >>> match_2("(858) 456-7890")
    True
    >>> match_2("(858)456-789")
    False
    >>> match_2("(858)456-7890")
    False
    >>> match_2("a(858) 456-7890")
    False
    >>> match_2("(858) 456-7890b")
    False
    """
    pattern = r"^\(858\) \d{3}-\d{4}$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_3(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_3("qwertsd?")
    True
    >>> match_3("qw?ertsd?")
    True
    >>> match_3("ab c?")
    False
    >>> match_3("ab   c ?")
    True
    >>> match_3(" asdfqwes ?")
    False
    >>> match_3(" adfqwes ?")
    True
    >>> match_3(" adf!qes ?")
    False
    >>> match_3(" adf!qe? ")
    False
    """
    pattern = r"^[a-zA-Z0-9\s?]{5,9}\?$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_4(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_4("$$AaaaaBbbbc")
    True
    >>> match_4("$!@#$aABc")
    True
    >>> match_4("$a$aABc")
    False
    >>> match_4("$iiuABc")
    False
    >>> match_4("123$$$Abc")
    False
    >>> match_4("$$Abc")
    True
    >>> match_4("$qw345t$AAAc")
    False
    >>> match_4("$s$Bca")
    False
    >>> match_4("$!@$")
    False
    """
    pattern = r"^\$[^abc$]*\$[aA]+[bB]+[cC]+$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_5(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_5("dsc80.py")
    True
    >>> match_5("dsc80py")
    False
    >>> match_5("dsc80..py")
    False
    >>> match_5("dsc80+.py")
    False
    """
    pattern = r"^\w+\.py$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_6(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_6("aab_cbb_bc")
    False
    >>> match_6("aab_cbbbc")
    True
    >>> match_6("aab_Abbbc")
    False
    >>> match_6("abcdef")
    False
    >>> match_6("ABCDEF_ABCD")
    False
    """
    pattern = r"^[a-z]+_[a-z]+$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_7(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_7("_abc_")
    True
    >>> match_7("abd")
    False
    >>> match_7("bcd")
    False
    >>> match_7("_ncde")
    False
    """
    pattern = r"^_.*_$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_8(string):
    """
    DO NOT EDIT THE DOCSTRING!
    >>> match_8("ASJDKLFK10ASDO")
    False
    >>> match_8("ASJDKLFK0ASDo!!!!!!! !!!!!!!!!")
    True
    >>> match_8("JKLSDNM01IDKSL")
    False
    >>> match_8("ASDKJLdsi0SKLl")
    False
    >>> match_8("ASDJKL9380JKAL")
    True
    """
    pattern = r"^[^Oi1]+$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None



def match_9(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_9('NY-32-NYC-1232')
    True
    >>> match_9('ca-23-SAN-1231')
    False
    >>> match_9('MA-36-BOS-5465')
    False
    >>> match_9('CA-56-LAX-7895')
    True
    >>> match_9('NY-32-LAX-0000') # If the state is NY, the city can be any 3 letter code, including LAX or SAN!
    True
    >>> match_9('TX-32-SAN-4491')
    False
    '''
    pattern = r"^(CA-\d{2}-(SAN|LAX)-\d{4}|NY-\d{2}-[A-Z]{3}-\d{4})$"

    # Do not edit following code
    prog = re.compile(pattern)
    return prog.search(string) is not None


def match_10(string):
    '''
    DO NOT EDIT THE DOCSTRING!
    >>> match_10('ABCdef')
    ['bcd']
    >>> match_10(' DEFaabc !g ')
    ['def', 'bcg']
    >>> match_10('Come ti chiami?')
    ['com', 'eti', 'chi']
    >>> match_10('and')
    []
    >>> match_10('Ab..DEF')
    ['bde']
    
    '''
    s_low = string.lower()
    s_clean = re.sub(r"\W|a", "", s_low)
    return re.findall(r".{3}", s_clean)


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def extract_personal(data):
    
    email_pattern = r"([a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    emails = re.findall(email_pattern, data)

    ssn_pattern = r"(\d{3}-\d{2}-\d{4})"
    ssns = re.findall(ssn_pattern, data)

    btc_pattern = r"\b((?:1|3|bc1)[a-zA-Z0-9]{25,})\b"
    bitcoins = re.findall(btc_pattern, data)

    address_pattern = r"\b(\d+ [A-Z][a-zA-Z ]+)\b"
    addresses = re.findall(address_pattern, data)

    return (emails, ssns, bitcoins, addresses)


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def tfidf_data(reviews_ser, review):
    
    N = len(reviews_ser)
    
    all_words = re.findall(r"\b(\w+)\b", review.lower())
    total_words_in_review = len(all_words)
    unique_words = set(all_words)
    
    results = {}
    
    reviews_ser_lower = reviews_ser.str.lower()
    
    for word in unique_words:
        cnt = all_words.count(word)
        tf = cnt / total_words_in_review
        
        pattern = r"\b" + re.escape(word) + r"\b"
        df = reviews_ser_lower.str.contains(pattern).sum()
        
        idf = np.log(N / df)
        
        tfidf = tf * idf
        
        results[word] = [cnt, tf, idf, tfidf]
        
    out_df = pd.DataFrame.from_dict(results, orient='index', 
                                 columns=['cnt', 'tf', 'idf', 'tfidf'])
    return out_df

def relevant_word(tfidf_df):
    return tfidf_df['tfidf'].idxmax()


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def hashtag_list(tweets_ser):
    pattern = r"#(\S+)"
    return tweets_ser.str.findall(pattern)

def most_common_hashtag(hashtag_ser):
    all_counts = hashtag_ser.explode().value_counts()
    
    def find_most_common_helper(h_list):
        if not h_list:
            return np.nan
        
        unique_hashtags = list(set(h_list))
        
        if len(unique_hashtags) == 1:
            return unique_hashtags[0]
        
        local_counts = all_counts.loc[unique_hashtags]
        
        return local_counts.idxmax()

    return hashtag_ser.apply(find_most_common_helper)


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def most_common_hashtag(hashtag_ser):
    all_counts = hashtag_ser.explode().value_counts()
    
    def find_most_common_helper(h_list):
        if not h_list:
            return np.nan
        
        unique_hashtags = list(set(h_list))
        
        if len(unique_hashtags) == 1:
            return unique_hashtags[0]
        
        # Get the global counts for just the unique hashtags in this list
        local_counts = all_counts[all_counts.index.isin(unique_hashtags)]
        
        if local_counts.empty:
            return np.nan
            
        return local_counts.idxmax()

    return hashtag_ser.apply(find_most_common_helper)


def create_features(ira):
    
    out_df = pd.DataFrame(index=ira.index)
    hashtag_lists = ira['text'].str.findall(r"#(\S+)")
    out_df['num_hashtags'] = hashtag_lists.str.len()
    out_df['mc_hashtags'] = most_common_hashtag(hashtag_lists)
    out_df['num_tags'] = ira['text'].str.findall(r"@[a-zA-Z0-9]+").str.len()
    out_df['num_links'] = ira['text'].str.findall(r"https?://\S+").str.len()
    out_df['is_retweet'] = ira['text'].str.startswith("RT")
    meta_pattern = r"(^RT\b|#\S+|@[a-zA-Z0-9]+|https?://\S+)"
    cleaned = ira['text'].str.replace(meta_pattern, " ", regex=True)
    cleaned = cleaned.str.replace(r"[^a-zA-Z0-9 ]", " ", regex=True)
    cleaned = cleaned.str.lower()
    cleaned = cleaned.str.replace(r"\s+", " ", regex=True).str.strip()
    out_df['text'] = cleaned
    column_order = ['text', 'num_hashtags', 'mc_hashtags', 'num_tags', 'num_links', 'is_retweet']
    
    return out_df[column_order]