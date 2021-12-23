"""
  MUKALMA - A Knowledge-Powered Conversational Agent
  Project Id: F21-20-R-KBCAgent

  partsOfSpeech Function Suite
    - A utility file that provides a lot of simple NLP Functions
    - Primarily includes basic POS Tagging functions
    - Has functions for cleaning and truecasing text spans
    - Uses Python's NLTK and Regex
"""

# Importing NLTK and Downloading wordnet model
import nltk
nltk.download('wordnet')

# Imports
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from pattern.text.en import singularize
import re

# Function to return a set of english nltk stopwords
def get_stopwords():
    return set(stopwords.words('english'))

# Function to perform POS tagging on a given sentence
def tag_sentence(sentence):
    wordsList = word_tokenize(sentence)
    tagged = nltk.pos_tag(wordsList)
    return tagged

# Function to retrieve all the nouns from the raw_text
def get_nouns(raw_text):
    tokenized = sent_tokenize(raw_text)
    nouns = []

    # Looping over the sentences
    for sentence in tokenized:
        tagged = tag_sentence(sentence)

        # Looping over sentence tokens
        for tag in tagged:
            if tag[1][:2] == 'NN':
                nouns.append(tag[0])
            # End if
        # End for
    # End for
    return nouns
# End of function

# Function to get a list of nltk noun tags
def get_noun_pos_list():
    return ['NN', 'NNS', 'NNP', 'NNPS']

# Function to get a list of nltk verbs
def get_verb_pos_list():
    return ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

# Function to get a set of pos entities
# from the given raw_text
def get_pos(raw_text, pos_list):
    tokenized = sent_tokenize(raw_text)
    nouns = []

    # Looping over the sentences
    for sentence in tokenized:
        tagged = tag_sentence(sentence)

        # Looping over the sentence tokens
        for tag in tagged:
            if tag[1] in pos_list:
                nouns.append(tag[0])
            # End if
        # End for
    # End for

    return nouns
# End of function

def match_words(word1, word2):
    t1 = singularize(word1.lower())
    t2 = singularize(word2.lower())
    return t1 == t2

def match_questions(message, questions, knowledge_sent):
    ls = get_noun_pos_list()
    ls.extend(get_verb_pos_list())

    print(f"USING POS:\n{ls}\n\n")

    message_nouns = get_pos(message, ls)
    print(f"MESSAGE POS: {message_nouns}")

    sentence_nouns = get_pos(knowledge_sent, ls)
    print(f"KNOWLEDGE POS: {sentence_nouns}\n")

    match_counts = []
    for question in questions:
        question_nouns = get_pos(question, ls)

        match_count = 0
        # Matching nouns
        for message_noun in message_nouns:
            # Match with question nouns
            for question_noun in question_nouns:
                if match_words(message_noun, question_noun):
                    match_count += 1

            # Match with Sentence nouns
            for sentence_noun in sentence_nouns:
                if match_words(message_noun, sentence_noun):
                    match_count += 0.5

        # End for

        match_counts.append(match_count)
        print(f"QUESTION: {question}\nQUESTION POS: {question_nouns}\nMATCH COUNT: {match_count}")

    arg_sort_match_counts = sorted(range(len(match_counts)), key=match_counts.__getitem__, reverse=True)
    sorted_questions = []

    for count_id in arg_sort_match_counts:
        if match_counts[count_id] == 0:
            break
        sorted_questions.append(questions[count_id])
    # End for

    print(f"SORTED QUESTIONS:\n{sorted_questions}")

    return sorted_questions

def match_message_and_answer(message, answer):
    ls = get_noun_pos_list()
    ls.extend(get_verb_pos_list())

    message_nouns = get_pos(message, ls)
    print(f"\n\n[CHITCHAT CHECK]: MESSAGE POS: {message_nouns}")

    sentence_nouns = get_pos(answer, ls)
    print(f"\n\n[CHITCHAT CHECK]: ANSWER POS: {sentence_nouns}\n")

    match_counts = 0

    for message_noun in message_nouns:
        for sentence_noun in sentence_nouns:
            if match_words(message_noun, sentence_noun):
                match_counts += 1
        # End for
    # End for

    print(f"\n[CHITCHAT CHECK]: total matches: {match_counts}")
    return match_counts

def match_nouns_from_set(message, setOfNouns):
    message_nouns = get_nouns(message)
    print(f"\n\n[CHITCHAT CHECK]: MESSAGE POS: {message_nouns}")

    matches = 0
    for message_noun in message_nouns:
        for noun in setOfNouns:
            if match_words(message_noun, noun):
                matches += 1

    print(f"\n[CHITCHAT CHECK]: total matches: {matches}")
    return matches

# Function to truscase the response text
def truecasing_by_pos(input_text):
    # tokenize the text into words
    words = word_tokenize(input_text)
    # apply POS-tagging on words
    tagged_words = pos_tag([word.lower() for word in words])
    # apply capitalization based on POS tags
    capitalized_words = [w.capitalize() if t in ["NN","NNS"] else w for (w,t) in tagged_words]
    # capitalize first word in sentence
    capitalized_words[0] = capitalized_words[0].capitalize()
    # join capitalized words
    text_truecase = re.sub(" (?=[\.,'!?:;])", "", ' '.join(capitalized_words))
    return text_truecase

# Regex function to fix and clean Sentences
def fix_sentence(str):
    if str == "":  # Don't change empty strings.
        return str
    if str[-1] in ["?", ".", "!"]:  # Don't change if already okay.
        return str
    if str[-1] == ",":  # Change trailing ',' to '.'.
        return str[:-1] + "."
    return str + "."  # Otherwise, add '.'.
