import operator
from extraction.coca import extractor

WINDOW_SIZE = 4
MIN_COUNT = 2


def word_to_word_cooccurrence(documents):
    """
    Builds the word-word cooccurrence 'matrix' for the documents.

    The result represents an NxN matrix, where N is the size vocabulary of all the documents. The implementation is
    a dictionary of target words to a dictionary of context words and their frequencies. If target word t and
    context word c never occur together, co_occurrences[t][c] will not exist. Otherwise, the entry will be the count
    of times that they appeared together in the window.

    Assumes documents are tokenized and any additonal preprocessing, such as lemmatization has already been done on
    the tokens.
    :param documents: the documents to build the co-occurrence matrix from
    :return the wordId-to-wordId co-occurrence matrix for the documents, the word-id mapping, and the id-word mapping
    """
    word_id, id_word = _word_id_map(documents)
    print("Total vocabulary:", str(len(word_id)))
    print("Total documents:", str(len(documents)))
    co_occurrences = {}
    doc_count = 0
    for document in documents:
        doc_count += 1
        if doc_count % 10 == 0:
            print(str(doc_count) + 'th document')
        compute_occurrences_for_document(co_occurrences, word_id, document)
    return co_occurrences, word_id, id_word


def _word_id_map(documents):
    """
    Build a word to id mapping for the vocabulary in the given documents.

    :param documents: to get the vocabulary from
    :return: word-id and id-word mapping
    """
    word_id = {}
    id_word = []
    words = _filter_to_min_count(documents)
    for i in range(len(words)):
        word_id[words[i][0]] = i
        id_word.append(words[i][0])
    return word_id, id_word


def _filter_to_min_count(documents):
    """
    Count the frequency of each word in the documents. Filter to words that meet the minimum frequency.

    :param documents: to filter the words from
    :return: a list of the unique words that exceed the minimum frequency count
    """
    word_freq = {}
    for document in documents:
        for token in document:
            if token in word_freq:
                word_freq[token] += 1
            else:
                word_freq[token] = 1
    sorted_freqs = sorted(word_freq.items(), key=operator.itemgetter(1))
    for i in range(len(sorted_freqs)):
        if sorted_freqs[i][1] >= MIN_COUNT:
            return sorted_freqs[i:]
    # Shouldn't happen if we're choosing the min count properly
    return sorted_freqs


def compute_occurrences_for_document(cooccurrences, word_id, document):
    """
    Computes the co-occurrences for the document, adding the counts to the existing cooccurrences mapping.

    :param cooccurrences: the cooccurence matrix to add to
    :param word_id: the word to wordId mapping
    :param document: the document to compute for
    """
    for i in range(len(document)):
        for c in range(i - WINDOW_SIZE, i + WINDOW_SIZE + 1):
            if c < 0 or c >= len(document) or i == c:
                continue
            else:
                if document[i] in word_id and document[c] in word_id:
                    target_id = word_id[document[i]]
                    context_id = word_id[document[c]]
                    if target_id not in cooccurrences:
                        cooccurrences[target_id] = {}
                    if context_id in cooccurrences[target_id]:
                        cooccurrences[target_id][context_id] += 1
                    else:
                        cooccurrences[target_id][context_id] = 1

if __name__ == '__main__':
    co_occurrences, word_id, id_word = word_to_word_cooccurrence(extractor.extract_all())
    i = 0
    for target_id, contexts in co_occurrences.items():
        if i >= 10:
            break
        else:
            i += 1
        print('--', id_word[target_id], '--')
        for context_id, count in contexts.items():
            print(id_word[context_id], ':', str(count))
