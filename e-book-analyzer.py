import requests,bs4,webbrowser,sys,time
import re
import nltk

from nltk.corpus import stopwords # For removing stopwords
nltk.download('stopwords') # If you did not download stopwords before, it will.
from nltk.tokenize import RegexpTokenizer # Just tokenizer for wide usage
import numpy as np
import pandas as pd

TEST = False  # This global variable exist for built-in tests or user based test.
# 0 for user based. 1 for built-in tests.

#   /$$   /$$           /$$                                  /$$$$$$                      /$$                 /$$
#  | $$  | $$          | $$                                 /$$__  $$                    | $$                | $$
#  | $$  | $$  /$$$$$$ | $$   /$$  /$$$$$$  /$$$$$$$       | $$  \__/  /$$$$$$  /$$$$$$$ | $$   /$$ /$$   /$$| $$
#  | $$$$$$$$ |____  $$| $$  /$$/ |____  $$| $$__  $$      | $$       |____  $$| $$__  $$| $$  /$$/| $$  | $$| $$
#  | $$__  $$  /$$$$$$$| $$$$$$/   /$$$$$$$| $$  \ $$      | $$        /$$$$$$$| $$  \ $$| $$$$$$/ | $$  | $$| $$
#  | $$  | $$ /$$__  $$| $$_  $$  /$$__  $$| $$  | $$      | $$    $$ /$$__  $$| $$  | $$| $$_  $$ | $$  | $$| $$
#  | $$  | $$|  $$$$$$$| $$ \  $$|  $$$$$$$| $$  | $$      |  $$$$$$/|  $$$$$$$| $$  | $$| $$ \  $$|  $$$$$$/| $$
#  |__/  |__/ \_______/|__/  \__/ \_______/|__/  |__/       \______/  \_______/|__/  |__/|__/  \__/ \______/ |__/

numberOfBook = int(input("How many books will you download (1 or 2): "))
# To choose how many books will I display.
print()
bookname1 = input("Book1: ")

# CAREFUL!! 
# The best way to find e-books on internet is basically surfing on google with spefic keywords
# Below keywords is for your searching query. In this homework just wikibook and wikisource.
# Assume you want to download Hamlet in wikibook, then you need to search wikibook hamlet in google.
searchKeywords = ['wikibook','wikisource']

# Below you search in google respectively in wikibook and wikisource. If the book is not find in wikibooks
# Then, it will try wikisource. 
for keyword in searchKeywords:
    # var: searching guery in google however, it directs you to re-direct page.
    var = requests.get(r'http://www.google.com/search?q='+keyword+' '+bookname1+'&btnI')
    # This page is about where to direct.
    redirect = var.url
    raw = requests.get(redirect)
    soup = bs4.BeautifulSoup(raw.text, "html.parser")
    # You basically parse all 'a' symbols because it shows html urls.
    # We use find because, first result would be most relevant link. 
    # Think of I'm feeling lucky button.
    lucky = soup.find('a').text

    # You lucky would be like https://en.wikibooks.org/wiki/hamlet
    # To test if it is in wikibook or not we simply use regex.
    # \.[\w]\. is finds all words between two dot. in this case only '.wikibooks.'
    # [1:-1] deletes first and last character .wikibooks. => wikibooks
    x = re.findall(r'\.[\w]+\.',lucky)[0][1:-1]
    # If the link in wikibooks then simply break. Otherwise, loop again for wikisource.
    if(x == 'wikibooks'):
        break

# After getting lucky link we need to parse the wikibook webpage.
# To find pdf page, we need to find pdf url. 

raw_page = requests.get(lucky)
wiki_page = raw_page.content

# urf-8 for just taking appoirate character. \x08 like chars is out of context
soup2 = bs4.BeautifulSoup(wiki_page.decode('utf-8'), "html.parser")

# I manually inspect the website and pdf link is within the html statement
#  <a class='internal' href='PDF_LINK' >PDF Version</a> 
book_url = soup2.find_all('a', {"class": "internal"})[0]['href'][2:]
book_url = 'https://' + book_url

# VOLAA ! We found pdf of book. Webscraping part is done.
print("The url of the book is:",book_url)

# The next thing to do, save the pdf as txt. Therefore, I used external library called pdftotext.
# It will take pdf from above url and save it with the same name that you queried above.
try:
    import pdftotext
    # Load your PDF
    with open(book_url, "rb") as f:
        pdf = pdftotext.PDF(f)

    # Save all text to a txt file.
    with open(bookname1 +'.txt', 'w') as f:
        f.write("\n\n".join(pdf))
except:
    # This is just an error message because I am aware of pdftotext is not widely used.
    # Therefore, I put links to download, if may take a while.
    # If you do not want to install and trust me, I provide extra 2 .txt file for built-in tests.
    # You can simply press 'n' to go manual tests otherwise, it will open download page.
    print()
    print("Looks like you did not download required library pdftotext. Please install it from below link")
    print("https://github.com/jalan/pdftotext")
    print("Installing can take a while.")
    print("Or in the below, you can try the tests with pre-installed books which the developer provides")
    x = input("To install please enter 'y', to forward tests please enter 'n': ")
    if(x == "y"):
        try:
            import webbrowser
            webbrowser.open("https://github.com/jalan/pdftotext")
            exit()
        except:
            exit()
    elif(x == "n"):
        TEST = True
        print('\nTEST STARTED...\n')
    else:
        print("Incorrect button. Shutting Down.")
        exit()


# If you choose 2 book and after first book all libraries are correctly installed.
# We can take second book with simply the same stradegy.
if(numberOfBook == "2"):
    bookname2 = input("Book2: ")
    searchKeywords = ['wikibook','wikisource']

    for keyword in searchKeywords:
        var = requests.get(r'http://www.google.com/search?q='+keyword+' '+bookname2+'&btnI')
        redirect = var.url
        raw = requests.get(redirect)
        soup = bs4.BeautifulSoup(raw.text, "html.parser")
        lucky = soup.find('a').text
        x = re.findall(r'\.[\w]+\.',lucky)[0][1:-1]
        if(x == 'wikibooks'):
            break
    raw_page = requests.get(lucky)
    wiki_page = raw_page.content
    soup2 = bs4.BeautifulSoup(wiki_page.decode('utf-8'), "html.parser")

    book_url = soup2.find_all('a', {"class": "internal"})[0]['href'][2:]
    book_url = 'https://' + book_url
    
    # Load your PDF
    with open(book_url, "rb") as f:
        pdf = pdftotext.PDF(f)

    # Save all text to a txt file.
    with open(bookname2 +'.txt', 'w') as f:
        f.write("\n\n".join(pdf))

# If you downloaded the books without trouble, in the current folder,
# there should be THEBOOKNAMEYOUENTERED.txt. Then we needed to parse all words.
if(TEST == False):
    if(numberOfBook == 1):
        # If only one book is selected... Simply open it in read mode utf-8.
        book1 = open(bookname1 + '.txt','r',encoding=('utf-8'))
        b1 = book1.readlines()
        book1.close()
        # First we stringfy all sentences in list array.
        # We need to lower all words and delete \n (new lines)
        # "Hello World!\n" => "hello world"
        bookstring1 = " ".join(b1).lower().replace("\n", "")
        text = bookstring1

        # we are using Regular Expression Tokenizer for personally, most accurate preprocesing
        # For comparing words we needed to eliminate signs (+, -, ') or numbers (3.6, 5) etc.
        # Also, we need to count each of cat, cat's, non-cat as one.
        # That is why we use regex with [A-Za-z]+ which will take each word.
        tokenizer = RegexpTokenizer(r'[A-Za-z]+')
        text_tokens = tokenizer.tokenize(text)

        # For performance, we cached stopwords one.
        cachedStopwords = stopwords.words('english') 
        # Below, we shrink all statement block in below, into one line.
        # tokens_without_sw = []
        # for word in text_tokens:
        #   if(word not in cachedStopwords):
        #       tokens_without_sw.append(word)
        tokens_without_sw = [word for word in text_tokens if not word in cachedStopwords]

        # Then we convert list to string and found frequency distributions
        text1 = " ".join(tokens_without_sw)
        fdist1 = nltk.FreqDist(tokens_without_sw)

        # we get how many words you want to display
        n = int(input("How many word you want to display: "))

        # Some manipulations for more aestatic table
        df = pd.DataFrame(fdist1.most_common(n))
        df = df.rename(columns={0: "WORD", 1: "FREQ_1"})

        df['NO'] = np.array(range(1,n+1))
        df = df[['NO','WORD','FREQ_1']]

        # VOLAA !!
        print(df.to_string(index=False))
    
    if(numberOfBook == 2):
        book1 = open(bookname1 + '.txt','r',encoding=('utf-8'))
        b1 = book1.readlines()
        book1.close()
        bookstring1 = " ".join(b1).lower().replace("\n", "")
        text = bookstring1
        tokenizer = RegexpTokenizer(r'[A-Za-z]+')
        text_tokens = tokenizer.tokenize(text)

        cachedStopwords = stopwords.words('english')
        tokens_without_sw = [word for word in text_tokens if not word in cachedStopwords]

        text1 = " ".join(tokens_without_sw)
        fdist1 = nltk.FreqDist(tokens_without_sw)
        book2 = open(bookname2 + '.txt','r',encoding=('utf-8'))
        b2 = book2.readlines()
        book2.close()
        
        bookstring2 = " ".join(b2).lower().replace("\n", "")
        
        text2 = bookstring2
        text_tokens2 = tokenizer.tokenize(text2)

        tokens_without_sw2 = [word for word in text_tokens2 if not word in cachedStopwords]
        text2 = " ".join(tokens_without_sw2)
        fdist2 = nltk.FreqDist(tokens_without_sw2)
        n = int(input("How many word you want to display: "))
        df = pd.DataFrame(fdist1.most_common(n))
        df2 = pd.DataFrame(fdist2.most_common(n))

        # Thanks to freqdist, If we have 2 booko to compare,
        # we can easily subsract or add them to find common or distinc words.
        df3 = pd.DataFrame((fdist1 + fdist2).most_common(n))
        df4 = pd.DataFrame((fdist1 - fdist2).most_common(n))
        df5 = pd.DataFrame((fdist2 - fdist1).most_common(n))

        # Rest of them is also table manipulation.
        df = pd.DataFrame(fdist1.most_common(n))
        df = df.rename(columns={0: "WORD", 1: "FREQ_1"})

        df['NO'] = np.array(range(1,n+1))
        df = df[['NO','WORD','FREQ_1']]
        print(df.to_string(index=False))
        
        print("\n")
        df2 = pd.DataFrame(fdist2.most_common(n))
        df2 = df2.rename(columns={0: "WORD", 1: "FREQ_2"})

        df2['NO'] = np.array(range(1,n+1))
        df2 = df2[['NO','WORD','FREQ_2']]
        print(df2.to_string(index=False))

        print("\n")

        df = pd.DataFrame(fdist1.most_common(n))
        df2 = pd.DataFrame(fdist2.most_common(n))
        df3 = pd.DataFrame((fdist1 + fdist2).most_common(n))
        
        
        d = pd.DataFrame()
        d['NO'] = np.array(range(1,n+1))
        d['WORD'] = df3[0]
        d['FREQ_1'] = df[1]
        d['FREQ_2'] = df2[1]
        d['FREQ_SUM'] = df3[1]
        print(d.to_string(index=False))
        print("\n")
    
        df4 = df4.rename(columns={0: "WORD", 1: "FREQ_1"})
        df4['NO'] = np.array(range(1,n+1))
        df4 = df4[['NO','WORD','FREQ_1']]
        print(df4.to_string(index=False))
        print("\n")

        df5 = df5.rename(columns={0: "WORD", 1: "FREQ_2"})
        df5['NO'] = np.array(range(1,n+1))
        df5 = df5[['NO','WORD','FREQ_2']]
        print(df5.to_string(index=False))
        print("\n")

#$$$$$$$$\ $$$$$$$$\  $$$$$$\ $$$$$$$$\ 
#\__$$  __|$$  _____|$$  __$$\\__$$  __|
#   $$ |   $$ |      $$ /  \__|  $$ |   
#   $$ |   $$$$$\    \$$$$$$\    $$ |   
#   $$ |   $$  __|    \____$$\   $$ |   
#   $$ |   $$ |      $$\   $$ |  $$ |   
#   $$ |   $$$$$$$$\ \$$$$$$  |  $$ |   
#   \__|   \________| \______/   \__|

## WARNING!! ##

# These part is identically same with above if statement so any more comment is not necessary.
# If you press n above, these statements will be executed.
if(TEST == True):
    if(numberOfBook == 1):
        print("BOOK 1: Non-Programmer's Tutorial for Python 2.6")
        book1 = open('Non-Programmer\'s_Tutorial_for_Python_2.6.txt','r',encoding=('utf-8'))
        b1 = book1.readlines()
        book1.close()
        bookstring1 = " ".join(b1).lower().replace("\n", "")
        text = bookstring1
        tokenizer = RegexpTokenizer(r'[A-Za-z]+')
        text_tokens = tokenizer.tokenize(text)

        cachedStopwords = stopwords.words('english')
        tokens_without_sw = [word for word in text_tokens if not word in cachedStopwords]

        text1 = " ".join(tokens_without_sw)
        fdist1 = nltk.FreqDist(tokens_without_sw)
        n = int(input("How many word you want to display: "))

        df = pd.DataFrame(fdist1.most_common(n))
        df = df.rename(columns={0: "WORD", 1: "FREQ_1"})

        df['NO'] = np.array(range(1,n+1))
        df = df[['NO','WORD','FREQ_1']]
        print(df.to_string(index=False))
    
    if(numberOfBook == 2):
        print("BOOK 1: Non-Programmer's Tutorial for Python 2.6")
        print("BOOK 2: Non-Programmer's Tutorial for Python 3")
        book1 = open('Non-Programmer\'s_Tutorial_for_Python_2.6.txt','r',encoding=('utf-8'))
        b1 = book1.readlines()
        book1.close()
        bookstring1 = " ".join(b1).lower().replace("\n", "")
        text = bookstring1
        tokenizer = RegexpTokenizer(r'[A-Za-z]+')
        text_tokens = tokenizer.tokenize(text)

        cachedStopwords = stopwords.words('english')
        tokens_without_sw = [word for word in text_tokens if not word in cachedStopwords]

        text1 = " ".join(tokens_without_sw)
        fdist1 = nltk.FreqDist(tokens_without_sw)

        book2 = open('Non-Programmer\'s_Tutorial_for_Python_3.txt','r',encoding=('utf-8'))
        b2 = book2.readlines()
        book2.close()
        
        bookstring2 = " ".join(b2).lower().replace("\n", "")
        
        text2 = bookstring2
        text_tokens2 = tokenizer.tokenize(text2)

        tokens_without_sw2 = [word for word in text_tokens2 if not word in cachedStopwords]
        text2 = " ".join(tokens_without_sw2)
        fdist2 = nltk.FreqDist(tokens_without_sw2)
        n = int(input("How many word you want to display: "))
        df = pd.DataFrame(fdist1.most_common(n))
        df2 = pd.DataFrame(fdist2.most_common(n))
        df3 = pd.DataFrame((fdist1 + fdist2).most_common(n))
        df4 = pd.DataFrame((fdist1 - fdist2).most_common(n))
        df5 = pd.DataFrame((fdist2 - fdist1).most_common(n))

        df = pd.DataFrame(fdist1.most_common(n))
        df = df.rename(columns={0: "WORD", 1: "FREQ_1"})

        df['NO'] = np.array(range(1,n+1))
        df = df[['NO','WORD','FREQ_1']]
        #print(df.to_string(index=False))
        
        print("\n")
        df2 = pd.DataFrame(fdist2.most_common(n))
        df2 = df2.rename(columns={0: "WORD", 1: "FREQ_2"})

        df2['NO'] = np.array(range(1,n+1))
        df2 = df2[['NO','WORD','FREQ_2']]
        #print(df2.to_string(index=False))

        print("\n")

        df = pd.DataFrame(fdist1.most_common(n))
        df2 = pd.DataFrame(fdist2.most_common(n))
        df3 = pd.DataFrame((fdist1 + fdist2).most_common(n))
        
        
        d = pd.DataFrame()
        d['NO'] = np.array(range(1,n+1))
        d['WORD'] = df3[0]
        d['FREQ_1'] = df[1]
        d['FREQ_2'] = df2[1]
        d['FREQ_SUM'] = df3[1]
        print("COMMON WORDS")
        print(d.to_string(index=False))
        print("\n")
    
        print("BOOK 1: Non-Programmer's Tutorial for Python 2.6")
        print("DISTINCT WORDS")
        df4 = df4.rename(columns={0: "WORD", 1: "FREQ_1"})
        df4['NO'] = np.array(range(1,n+1))
        df4 = df4[['NO','WORD','FREQ_1']]
        print(df4.to_string(index=False))
        print("\n")

        print("BOOK 2: Non-Programmer's Tutorial for Python 3")
        print("DISTINCT WORDS")
        df5 = df5.rename(columns={0: "WORD", 1: "FREQ_2"})
        df5['NO'] = np.array(range(1,n+1))
        df5 = df5[['NO','WORD','FREQ_2']]
        print(df5.to_string(index=False))


print("\n\nProgram Finished.")
