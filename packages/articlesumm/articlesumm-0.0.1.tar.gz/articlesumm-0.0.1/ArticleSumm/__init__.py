import requests
import nltk
from nltk.tokenize import RegexpTokenizer
import heapq
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

reader=''' To summarize, when it comes to calling a variable from another function in Python, there are
two viable options available: utilizing global variables or employing the return statement. The preferred 
approach between these two options is contingent on the requirements of the specific scenario. However, it's
 commonly accepted that using the return statement offers greater control over the values being transferred
 between functions and is thus considered a more optimal method. This approach is thought to be superior to
 utilizing global variables because it gives the user more control over the values transferred between 
 functions and lowers the possibility of unintentional modifications to the variables.
'''

def purge(read):
    global task_words, task_sentences
    tokenizer = RegexpTokenizer('\w+')
    task_words = tokenizer.tokenize(read)
    task_sentences = nltk.sent_tokenize(read)
    return task_words, task_sentences

def summarizer(content, words, sentence_list, summary_length):
    #task_words=purge(reader)[0]
    #sentences=task_sentences
    sentences=sentence_list
    frequency = nltk.FreqDist(words)
    max_frequency = max(frequency.values())

    for word in frequency.keys():
        frequency[word] = frequency[word]/max_frequency
    sentence_scores = {}
    for x in sentences:
        m = re.search(r'https?:|\(|\[',x)
        if not m:
            if len(x.split(' ')) < 30:
                for word in nltk.word_tokenize(x.lower()):
                    if word in frequency.keys():
                        if x not in sentence_scores.keys():
                            sentence_scores[x] = frequency[word]
                        else:
                            sentence_scores[x] += frequency[word]

    summary_sentences = heapq.nlargest(summary_length, sentence_scores, key=sentence_scores.get)
    summary=''.join(summary_sentences)
    return summary
    
summarizer(reader, words=purge(reader)[0],sentence_list=purge(reader)[1],summary_length=2)
