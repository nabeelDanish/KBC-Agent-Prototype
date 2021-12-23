"""
  MUKALMA - A Knowledge-Powered Conversational Agent
  Project Id: F21-20-R-KBCAgent

  subjectVerbObject
    - Interface functions for the Subject-Verb/Adjective-Object extraction tools
    - from a Raw Text input using Spacy and NLTK
    - Used for extractions, matching, and filtering in texts and between texts
    - Uses the core functions from svo_utils.py file
"""

# Imports
from .svo_utils import *
import re


# Function to retrieve SVO triples from the tokens created using
# Spacy NLP Model
def findSubjectVerbObjects(tokens):
    svos = []
    passive = isPassive(tokens)
    verbs = findVerbs(tokens)
    visited = set()

    # Iterating over the verbs
    for verb in verbs:
        subjects, verbNegated = getAllSubjects(verb)

        # If there are subjects, we examine this verb
        if len(subjects) > 0:
            isConjuctiveVerb, conjuctiveVerb = rightOfVerbIsConjuctiveVerb(verb)

            # We explore the verb if it linked to a conjunction
            if isConjuctiveVerb:
                verb2, objects = getAllObjects(conjuctiveVerb, passive)

                # Iterating over the subjects and the objects to load the conjunctive
                # SVOs
                for subject in subjects:
                    for object in objects:
                        objectNegated = isNegated(object)

                        # Preparing the SVO Tuple
                        s1 = toString(expand(object, tokens, visited))
                        v1 = "!" + verb.lemma_ if verbNegated or objectNegated else verb.lemma_
                        v2 = "!" + verb2.lemma_ if verbNegated or objectNegated else verb2.lemma_
                        o1 = toString(expand(subject, tokens, visited))

                        # Switch based on the passive
                        if passive:
                            svos.append(cleanGenerateSVAOs(o1, v1, s1))
                            svos.append(cleanGenerateSVAOs(o1, v2, s1))
                        else:
                            svos.append(cleanGenerateSVAOs(s1, v1, o1))
                            svos.append(cleanGenerateSVAOs(s1, v2, o1))
                    # End for
                # End for
            # End if
            else:
                verb, objects = getAllObjects(verb, passive)

                # Iterating over the subjects
                for subject in subjects:
                    if len(objects) > 0:
                        for object in objects:
                            objectNegated = isNegated(object)

                            # Building the SVO Tuple
                            o1 = toString(expand(object, tokens, visited))
                            v1 = "!" + verb.lemma_ if verbNegated or objectNegated else verb.lemma_
                            s1 = toString(expand(subject, tokens, visited))

                            # Passive Switch Case
                            if passive:
                                svos.append(cleanGenerateSVAOs(o1, v1, s1))
                            else:
                                v1 = "!" + verb.lower_ if verbNegated or objectNegated else verb.lower_
                                svos.append(cleanGenerateSVAOs(s1, v1, o1))
                        # End for
                    # End if
                # End for
            # End else
        # End if
    # End for

    return svos
# End of function

# Function to find all the Subject - Verb/Adjective - Object tuples from the text
def findSubjectVerbAdjectiveObjects(tokens):
    svaos = []
    verbs = verbs = [tok for tok in tokens if tok.pos_ == VERB or tok.dep_ != aux]
    passive = isPassive(tokens)

    # Iterating over the verbs
    for verb in verbs:
        subjects, verbNegated = getAllSubjects(verb)

        # If we have subjects around the verb
        if len(subjects) > 0:
            verb, objects = getAllObjectsWithAdjectives(verb, passive)

            # Iterating over subject object pairs
            for subject in subjects:
                for object in objects:
                    objectNegated = isNegated(object)
                    objectDescTokens = generateLeftRightAdjectives(object)
                    subCompound = generateSubCompound(subject)

                    # Building the SVAO Tuple
                    s1 = " ".join(tok.lower_ for tok in subCompound)
                    v1 = "!" + verb.lower_ if verbNegated or objectNegated else verb.lower_
                    o1 = " ".join(tok.lower_ for tok in objectDescTokens)

                    # Appending the SVAO
                    svaos.append(cleanGenerateSVAOs(s1, v1, o1))

                # End for
            # End for
        # End if
    # End for

    return svaos


# End of function

# Function to retrieve SVAOs and SVOs combined from the raw text
def retrieve_SVAOs(text):
    # Tokenizing
    tokens = nlp(text)

    # Finding SVOs and SVAOs
    svos = findSubjectVerbObjects(tokens)
    svaos = findSubjectVerbAdjectiveObjects(tokens)

    # Removing the tuples with less then 2 items
    # and cleaning for \n objects/subjects
    svos = [svo for svo in svos if len(svo) >= 3 and svo[0] != "\n" and svo[2] != "\n"]
    svaos = [svao for svao in svaos if len(svaos) >= 3 and svao[0] != "\n" and svao[2] != "\n"]

    # Merging the two
    svao_total = svos + svaos

    return svao_total
# End of function

# Function to retrieve similar SVOs and SVAOs from the context and the source text
def match_similar_SVAOs(svaos_context, svaos_source):
    similar_svaos = []
    for svao_context in svaos_context:
        for svao_source in svaos_source:
            toMatch = svao_context[2].lower()
            toMatch2 = svao_context[1].lower()
            subject_candidate = svao_source[0].lower()
            object_candidate = svao_source[2].lower()

            # Using Regex to match both strings as substrings
            x1 = re.search(toMatch, subject_candidate)
            x2 = re.search(toMatch, object_candidate)

            if x1 is not None or x2 is not None:
                similar_svaos.append(svao_source)

            x1 = re.search(toMatch2, subject_candidate)
            x2 = re.search(toMatch2, object_candidate)
            if x1 is not None or x2 is not None:
                similar_svaos.append(svao_source)
        # End for
    # End for
    return similar_svaos
# End of function

# Main Function to work with single turn conversation and knowledge text 
# for SVAOs extraction
def extractSimilarSVAOs(dialogue, knowledge):
    svaos_dialogue = retrieve_SVAOs(dialogue)
    svaos_knowledge = retrieve_SVAOs(knowledge)
    print(f"\n\n{svaos_knowledge}\n")
    similarSVAOs = match_similar_SVAOs(svaos_dialogue, svaos_knowledge)
    print("SVAOS Dialogue : ", svaos_dialogue)
    return similarSVAOs
# End of function
