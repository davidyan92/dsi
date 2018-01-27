# sample data
spam = 'Hello,\nI saw your contact information on LinkedIn. I have carefully read through your profile and you seem to have an outstanding personality. This is one major reason why I am in contact with you. My name is Mr. Valery Grayfer Chairman of the Board of Directors of PJSC "LUKOIL". I am 86 years old and I was diagnosed with cancer 2 years ago. I will be going in for an operation later this week. I decided to WILL/Donate the sum of 8,750,000.00 Euros(Eight Million Seven Hundred And Fifty Thousand Euros Only etc. etc.'

ham = 'Hello,\nI am writing in regards to your application to the position of Data Scientist at Hooli X. We are pleased to inform you that you passed the first round of interviews and we would like to invite you for an on-site interview with our Senior Data Scientist Mr. John Smith. You will find attached to this message further information on date, time and location of the interview. Please let me know if I can be of any further assistance. Best Regards.'

print spam
print
print ham


# try a counter
from collections import Counter
print Counter(spam.lower().split())
print
print Counter(ham.lower().split())

# count vectorizer
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer

cvec = CountVectorizer()
cvec.fit([spam])

# create dataframe on cvec
df  = pd.DataFrame(cvec.transform([spam]).todense(),
             columns=cvec.get_feature_names())
#show the df
df.transpose().sort_values(0, ascending=False).head(10).transpose()

# hashing vectorizer (your turn)
hvec = HashingVectorizer()

df  = pd.DataFrame(hvec.transform([spam]).todense())
df.transpose().sort_values(0, ascending=False).head(10).transpose()


# td idf vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
tvec = TfidfVectorizer(stop_words='english')
tvec.fit([spam, ham])

df  = pd.DataFrame(tvec.transform([spam, ham]).todense(),
                   columns=tvec.get_feature_names(),
                   index=['spam', 'ham'])
df
# see dfs
df.transpose().sort_values('spam', ascending=False).head(10).transpose()

#see dfs
df.transpose().sort_values('ham', ascending=False).head(10).transpose()
