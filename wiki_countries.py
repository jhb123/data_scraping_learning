import urllib.request
from bs4 import BeautifulSoup
from collections import defaultdict
import random

#urllib.request is for opening and reading websites
#BeautifulSoup converts the html into a more easy to use format, as well as having
#lots of useful functions in it.
#defaultdict is useful for creating dictionaries where the key value pairs have
#lists as the value, and each time a none existant key is reference, a new list
#is started.


#this url contains the list of countries that will be used to make the game
url = "https://en.wikipedia.org/wiki/List_of_sovereign_states"

#This opens the page
page = urllib.request.urlopen(url)

#Convert the page object to a BeautifulSoup object, which makes the page easier
#to navigate through
soup = BeautifulSoup(page, "lxml")

#in the soup object, I beforehand found that the thing I was looking for was a
#table with the class 'sortable wikipedia'. The page only has one of these objects
#which makes this a bit easier
right_table = soup.find('table',{'class':"sortable wikitable"})

#titles = links.find('title')

#create a list for names of all the countries to be put in
names = []

#look for all the rows in table, these are identified by the html tage tr
#Use the beautful soup functions to look through the pages HTML, the inspect
#element functionality of chrome etc. adds extra things which aren't actually in
#the pages HTML.
rows = right_table.find_all('tr') #type(right_table)
for idx,row in enumerate(rows):
    #skip first three rows
    if(idx < 3):
        pass
    else:
        #each row has cells, some of the rows are used to format the page and
        #dont contain a coutries name.
        cells = row.find_all('td')
        if(cells is None):
            pass
        elif(len(cells) == 4):
            #if the row has 4 cells, its a country containing row. Find the link
            #in the first cell

            link = cells[0].find('a')

            # look out for the link not being a country
            try:
                title = link.get('title')
                if(title is None):
                    pass
                elif(title == 'Member states of the United Nations'):
                    pass
                else:
                    #print(title)
                    names.append(title)
            except:
                pass

#convert it all to lower case to prevent gaining information such as 'Eygpyt'
# starting with E, whereas Chad does not start with A.
# Remove the phrase country (e.g I think georgia has this in its wikipedia page)
# republic of ireland is not the real name of ireland.
# I haven't been through the list to check that all the countries there are correclty
# named e.g. is it 'the ukraine' or ukraine? I've heard both
for idx,phrase in enumerate(names):
    names[idx] = phrase.lower()
    if( '(country)' in phrase):
        names[idx] = phrase.replace('(country)','')
    if(phrase == 'republic of ireland'):
        names[idx] = 'ireland'

# create a dictionary where key = country name, value is the string of vowels
quiz_names = {}
vowels = 'aeiou'
for idx,phrase in enumerate(names):
    phrase_full = phrase
    #go through each character in the coutnries name, check if its a vowel. If
    # it is not a vowel, then replace it with no character
    for character in phrase:
        if(character not in vowels):
            phrase = phrase.replace(character,'')
    phrase_vowels = phrase
    quiz_names[phrase_full] = phrase_vowels


#create a dictionary where the key is the string of vowels, and the values is a
#list of countries. use defaultdict to do this, as the dictionary starts with
#empty lists that you can append.

quiz_names_grouped = defaultdict(list)
for key,value in quiz_names.items():
    quiz_names_grouped[value].append(key)


#after this point, the code just generates a game which has the properties I wanted
#so the choices here are kind of arbitrary.

#I want 6 types of questions in the question pool, and one object with the
# the randomly chosen questions in it. The structure of the dictionary is
# key,val = question,answer = voewls,country name.
quiz_questions_1 = {}
quiz_questions_2 = {}
quiz_questions_3 = {}
quiz_questions_4 = {}
quiz_questions_5 = {}
quiz_questions_long = {}
quiz_questions = {}


#go through each country and see what type of question it would be
for key,value in quiz_names_grouped.items():
    if(len(key) == 1):
        quiz_questions_1[key] = value
    elif(len(key) == 2):
        quiz_questions_2[key] = value
    elif(len(key) == 3):
        quiz_questions_3[key] = value
    elif(len(key) == 4):
        quiz_questions_4[key] = value
    elif(len(key) == 5):
        quiz_questions_5[key] = value
    else:
        quiz_questions_long[key] = value


#choose questions to add. random is seeded using the system time, so different
#questions are generated each time its played. Select a number of each type, based
#on the variable k
random_choice_1 = random.choices(list(quiz_questions_1.keys()), k = 1)
random_choice_2 = random.choices(list(quiz_questions_2.keys()), k = 3)
random_choice_3 = random.choices(list(quiz_questions_3.keys()), k = 5)
random_choice_4 = random.choices(list(quiz_questions_4.keys()), k = 3)
random_choice_5 = random.choices(list(quiz_questions_5.keys()), k = 1)
random_choice_long = random.choices(list(quiz_questions_long.keys()), k = 1)


#add each choice to the quiz_questions dictionary
for idx,word in enumerate(random_choice_1):
    quiz_questions[random_choice_1[idx]] = quiz_questions_1[random_choice_1[idx]]

for idx,word in enumerate(random_choice_2):
    quiz_questions[random_choice_2[idx]] = quiz_questions_2[random_choice_2[idx]]

for idx,word in enumerate(random_choice_3):
    quiz_questions[random_choice_3[idx]] = quiz_questions_3[random_choice_3[idx]]

for idx,word in enumerate(random_choice_4):
    quiz_questions[random_choice_4[idx]] = quiz_questions_4[random_choice_4[idx]]

for idx,word in enumerate(random_choice_5):
    quiz_questions[random_choice_5[idx]] = quiz_questions_5[random_choice_5[idx]]

for idx,word in enumerate(random_choice_long):
    quiz_questions[random_choice_long[idx]] = quiz_questions_long[random_choice_long[idx]]


#print the rules
print("""
Each country has had its consonants removed, leaving only the vowels \n
in the order they come in the original word. The list is randomly \n
generated each time, but each round has 1 question for countries with \n
one vowel, 3 with 2 vowels, 5 with 3 vowels, 3 with 4 vowels, 1 with \n
5 vowels, and then 1 with more than 5 vowels. There may be multiple \n
countries which have the same string of vowels when the consonants are \n
removed. Have fun!
""")
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~Questions~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print the key for each of the values of the dictionary of quiz questions.
q_num = 1
for key,val in quiz_questions.items():
    print(str(q_num) + '. ' + key)
    q_num = q_num + 1

#wait for the player to press enter before revealing the answers i.e. the
#values of each item in the dictionary of quiz questions
input('Press enter to reveal answers...')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~ Answers ~~~~~~~~~~~~~~~~~~~~~~~~~~~')
q_num = 1
for key,val in quiz_questions.items():
    print(str(q_num) + '. ' + str(val))
    q_num = q_num + 1
