from os.path import exists
import re


# The data source directories
DATA_DIR = 'C:/Projects/PyNLPTools/datasources/'
COCA_RAW_DIR = DATA_DIR + 'raw/coca/'
COCA_EXTRACTED_DIR = DATA_DIR + 'extracted/coca/'

# Option to use existing aggregate file, which has been precomputed
USE_CACHED = True

# All documents output file
ALL_DOCUMENTS_OUTPUT_FILE = COCA_EXTRACTED_DIR + 'coca_extracted_normalized.txt'

# COCA core
COCA_CORE_DIR = COCA_RAW_DIR + 'coca-core-wordLemPoS/'
COCA_CORE_FILE_PREFIXES = ('wlp_acad_', 'wlp_fic_', 'wlp_mag_', 'wlp_news_', 'wlp_spok_')
COCA_CORE_START_YEAR = 1990
COCA_CORE_END_YEAR = 2012

# COCA glowbe
COCA_GLOWBE_DIR = COCA_RAW_DIR + 'coca-glowbe-wordLemPoS/'

# COCA now
COCA_NOW_DIR = COCA_RAW_DIR + 'coca-now-wordLemPoS/'

# COCA wikipedia
COCA_WIKIPEDIA_DIR = COCA_RAW_DIR + 'coca-wikipedia-wordLemPoS/'

# Punctuation, special characters, and "'s"
IGNORED_PARTS_OF_SPEECH = ('y', 'x', 'ge')
NUMBER_PART_OF_SPEECH = 'mc'
NUMBER_PLACEHOLDER = '<NUMBER>'
ONE_PART_OF_SPEECH = 'mc1'
ONE_PLACEHOLDER = '<ONE>'
TIME_PERIOD_PART_OF_SPEECH = 'mc2'
TIME_PERIOD_PLACE_HOLDER = '<TIMEPERIOD>'


def extract_all():
    """
    Extracts the documents from each of the COCA test corpora and saves them into an aggregate file.
    If USE_CACHED is specified and the file already exists, then the precomputed aggregate file will be used.

    :return: the list of documents from the COCA corpora, where a document is just a list of words
    """
    if not USE_CACHED or not exists(ALL_DOCUMENTS_OUTPUT_FILE):
        all_documents = []
        all_documents += get_core_documents()
        all_documents += get_glowbe_documents()
        all_documents += get_now_documents()
        all_documents += get_wikipedia_documents()
        save_documents(ALL_DOCUMENTS_OUTPUT_FILE, all_documents)
        return all_documents
    else:
        return get_docs_from_aggregate_file()


def get_core_documents():
    """
    Extract the core COCA documents.

    :return: the list of core COCA documents
    """
    core_documents = []
    for prefix in COCA_CORE_FILE_PREFIXES:
        for year in range(COCA_CORE_START_YEAR, COCA_CORE_END_YEAR + 1):
            print(prefix + str(year))
            core_documents += get_docs_from_file(COCA_CORE_DIR + prefix + str(year) + '.txt')
    return core_documents


def get_glowbe_documents():
    """
    Extract the GloWbe COCA documents.

    :return: the list of GloWbe COCA documents
    """
    return []


def get_now_documents():
    """
    Extract the NOW COCA documents.

    :return: the list of NOW COCA documents
    """
    return []


def get_wikipedia_documents():
    """
    Extract the Wikipedia COCA documents.

    :return: the list of Wikipedia COCA documents
    """
    return []


def get_docs_from_file(filename):
    """
    Extracts the documents from a COCA file.

    :param filename: containing documents to extract
    :return: the list of documents from the file
    """
    f = open(filename)
    file_docs = []
    current_doc = []
    for line in f:
        # The document identifier
        if re.match(r'^##\d*', line):
            if len(current_doc) != 0:
                file_docs.append(current_doc)
            current_doc = []
        else:
            # Replace certain parts of speech with placeholders, retrieve lemma
            word_lem_pos = line.split()
            if len(word_lem_pos) == 3 and word_lem_pos[2] not in IGNORED_PARTS_OF_SPEECH:
                if word_lem_pos[2] == NUMBER_PART_OF_SPEECH:
                    current_doc.append(NUMBER_PLACEHOLDER)
                elif word_lem_pos[2] == ONE_PART_OF_SPEECH:
                    current_doc.append(ONE_PLACEHOLDER)
                elif word_lem_pos[2] == TIME_PERIOD_PART_OF_SPEECH:
                    current_doc.append(TIME_PERIOD_PLACE_HOLDER)
                else:
                    current_doc.append(word_lem_pos[1])
    return file_docs


def get_docs_from_aggregate_file():
    """
    Extracts the documents of the COCA corpus from the precomputed aggregate file.

    :return: the list of COCA documents
    """
    f = open(ALL_DOCUMENTS_OUTPUT_FILE)
    file_docs = []
    for line in f:
        file_docs.append(line.split())
    return file_docs


def save_documents(filename, documents):
    """
    Saves the extracted documents into an aggregate file.

    :param filename: to save to
    :param documents: to save
    """
    f = open(filename, 'w')
    for document in documents:
        token_num = 1
        for token in document:
            f.write(token)
            # Write a space if it's not the last token
            if token_num != len(document):
                f.write(' ')
            token_num += 1
        f.write('\n')
    f.close()


if __name__ == '__main__':
    print(len(extract_all()))
