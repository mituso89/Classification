from nltk.corpus import stopwords
import re
#from bs4 import BeautifulSoup


class Common():


    def clean_text(text):
        REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;-]')
        BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
        STOPWORDS = set(stopwords.words('english'))
        """
            text: a string
            
            return: modified initial string
        """
        
        text = text.lower() # lowercase text
        text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
        text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
        text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
        return text