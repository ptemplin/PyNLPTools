def word_frequency(document, word_to_frequency = {}):
    """
    Computes the frequencies of words in a given document adding to the existing mapping.

    :param document: to compute word frequencies for
    :param word_to_frequency: existing mapping of words to frequencies from other documents
    :return: the modified word_to_frequency map and the total count of words in the document
    """
    count = 0
    for word in document:
        count += 1
        if word in word_to_frequency:
            word_to_frequency[word] += 1
        else:
            word_to_frequency[word] = 1
    return word_to_frequency, count


def word_frequency_documents(documents):
    """
    Computes the frequencies of words in a list of documents.

    :param documents: list to use
    :return: mapping of words to their frequencies and the total word count
    """
    word_to_frequency = {}
    count = 0
    for document in documents:
        w2f, doc_count = word_frequency(document, word_to_frequency)
        count += doc_count
    return word_to_frequency, count
