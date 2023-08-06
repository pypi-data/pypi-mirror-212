# Importing Libraries
import pathlib
import pickle
import os
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize

# Getting the file path
HERE = pathlib.Path(__file__).parent.resolve()



# Loading the list of past tense verbs
with open(HERE/"past_tense_verbs", "rb") as pkl:
    list_of_past_verbs = pickle.load(pkl)
    
    
    
########### Code ###########


# Decontracting strings

def decontract_strings(string: str)-> str:
    """Decontracting strings.
    
    :param num: Input str
    """ 
    
    # Doing for ' symbol
    # specific
    string = re.sub(r"won't", "will not", string)
    string = re.sub(r"can\'t", "can not", string)

    # general
    string = re.sub(r"n\'t", " not", string)
    string = re.sub(r"\'re", " are", string)
    string = re.sub(r"\'s", " is", string)
    string = re.sub(r"\'d", " would", string)
    string = re.sub(r"\'ll", " will", string)
    string = re.sub(r"\'t", " not", string)
    string = re.sub(r"\'ve", " have", string)
    string = re.sub(r"\'m", " am", string)
    
    # Doing similar for ’ symbol
    string = re.sub(r"won’t", "will not", string)
    string = re.sub(r"can\’t", "can not", string)

    # general
    string = re.sub(r"n\’t", " not", string)
    string = re.sub(r"\’re", " are", string)
    string = re.sub(r"\’s", " is", string)
    string = re.sub(r"\’d", " would", string)
    string = re.sub(r"\’ll", " will", string)
    string = re.sub(r"\’t", " not", string)
    string = re.sub(r"\’ve", " have", string)
    string = re.sub(r"\’m", " am", string)
    return string


def get_tense_each_sent(sentence:str)-> str:
    """
    This function takes a sentence as input and returns its tense. If multiple sentences are there inside the input text it returns the tense based on the frist sentence.
    """
    sen_ = decontract_strings(sentence)
    tokens = word_tokenize(sen_)
    tense = None
    
    for i in range(len(tokens)):
        if tokens[i].lower() in ['will', 'shall', 'may be','would','might','can','could','should','must']:
            tense = 'future'
            break
        elif tokens[i].lower() in list_of_past_verbs:
            tense = 'past'
            break
        else:
            tense = 'present'
    return tense

# Extract tense for each sentence of an article
def get_tense(article:str)-> list:
    """_summary_

    This function takes a article/sentences as input and returns the tense for each sentence.
    
    
    Args:
        sentence (str): Article/ sentense
        
    Returns:
        list: list of dictionary of each sentences as keys and tense as values.
    """
    
    output = []
    sentences = sent_tokenize(article)
    for sentence in sentences:
        tense = get_tense_each_sent(sentence)
        res = {sentence:tense}
        output.append(res)
    return output


# Extract tense for each sentence of an article with tense as key

def tense(article:str, tenses:str):
    """_summary_

    This function takes a article/sentences as input and returns the tense for each sentence.
    
    
    Args:
        sentence (str): Article/ sentense
    Returns:
        list: list of dictionary of each sentences as keys and tense as values.
    """
    
    t = str(tenses).lower()
    output_dict = {}
    sentences = sent_tokenize(article)
    for sentence in sentences:
        output = get_tense_each_sent(sentence)
        key = output
        if key not in output_dict:
            output_dict[key] = [sentence]
        else:
            output_dict[key].append(sentence)
    try:
        if t == '':  
            return output_dict
        else:
            return output_dict[t]
    except:
        print('No sentences of the tense',t.upper())






