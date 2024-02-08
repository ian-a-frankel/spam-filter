import pandas as pd
import numpy as np
import re

def clean(string):
    return re.sub("\W", " ", string)

def clean_msgs(df):
    new_df = df.copy()
    new_df['SMS'] = new_df['SMS'].apply(lambda x: clean(x)).str.lower()
    return new_df

messages = pd.read_csv('SMSSpamCollection', sep='\t', header=None, names=['Label','SMS'])

np.random.seed(1)
test_rows = np.random.choice(messages.shape[0], size = 1144, replace=False)
test_mask = np.isin(messages.index, test_rows)
train_mask = ~test_mask

cleaned_data = clean_msgs(messages)
train_data = cleaned_data[train_mask]

vocabulary = []

for msg in train_data['SMS']:
    wrds = msg.split(' ')
    words = [word for word in wrds if word != '']
    for word in words:
        vocabulary.append(word)

vocabulary = list(set(vocabulary))

word_counts_per_sms = {}

for word in vocabulary:
    word_counts_per_sms[word] = [0] * len(cleaned_data['SMS'])

ham_words = 0
spam_words = 0

for index,msg in enumerate(cleaned_data['SMS']):
    wrds = msg.split(' ')
    

for index, row in cleaned_data.iterrows():
    wrds = row['SMS'].split(' ')
    words = [word for word in wrds if word != '']
    
    for _ in words:
        if index not in test_rows:
            if row['Label'] == 'ham':
                 ham_words +=1
            else:
                 spam_words += 1
            word_counts_per_sms[_][index] +=1

mixed_chart = pd.concat([cleaned_data, pd.DataFrame(word_counts_per_sms)], axis=1)

trained_chart = mixed_chart[train_mask]

test_chart = mixed_chart[test_mask]

training_spam = trained_chart[trained_chart['Label'] == 'spam']
training_ham = trained_chart[trained_chart['Label'] == 'ham']

p_ham = training_ham.shape[0]
p_spam = training_spam.shape[0]

alpha = 0.1
ham_default = alpha / (ham_words + alpha * len(vocabulary))
spam_default = alpha / (spam_words + alpha * len(vocabulary))

p_w_given_ham_dict = {}
p_w_given_spam_dict = {}

def p_w_given_spam(w):
    has_w = (w in trained_chart.columns)
    if has_w:
         numerator = training_spam[w].sum() + alpha
    else:
         numerator = alpha
    denominator = alpha * len(vocabulary) + spam_words
    return numerator / denominator

def p_w_given_ham(w):
    has_w = (w in trained_chart.columns)
    if has_w:
         numerator = training_ham[w].sum() + alpha
    else:
         numerator = alpha
    denominator = alpha * len(vocabulary) + ham_words
    return numerator / denominator

for word in vocabulary:
     p_w_given_ham_dict[word] = p_w_given_ham(word)
     p_w_given_spam_dict[word] = p_w_given_spam(word)

def p_spam_given_msg(m):
    m_lis = clean(m).lower().split(' ')
    m_list = [word for word in m_lis if word != '']
    s = p_spam
    for word in m_list:
        factor = p_w_given_spam_dict.get(word, spam_default)
        s *= factor
    return s

def p_ham_given_msg(m):
    m_lis = clean(m).lower().split(' ')
    m_list = [word for word in m_lis if word != '']
    h = p_ham
    for word in m_list:
        factor = p_w_given_ham_dict.get(word, ham_default)
        h *= factor
    return h

correctly_classified = 0
incorrectly_classified = 0
spams = 0
hams = 0
for index, row in mixed_chart.iterrows():
    if index in test_rows:
        msg = row['SMS']
        lbl = row['Label']
        if p_spam_given_msg(msg) > p_ham_given_msg(msg) and lbl == 'spam':
            correctly_classified += 1
            spams +=1
        elif p_spam_given_msg(msg) < p_ham_given_msg(msg) and lbl == 'ham':
            correctly_classified +=1
            hams += 1
        else:
            incorrectly_classified += 1

print('Correctly classified:')
print(correctly_classified)
print('Incorrectly_classified:')
print(incorrectly_classified)