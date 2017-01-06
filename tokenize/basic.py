def tokenize_document(doc):
    """
    Tokenize the document string.

    :param doc: string to tokenize
    :return: the list of tokenized sentences (in turn a list of words) from the document
    """
    sentences = extract_sentences(doc)
    tokens = []
    for sentence in sentences:
        tokens.append(tokenize_sentence(sentence))
    return tokens


def extract_sentences(doc):
    """
    Splits the document into sentences using end punctuation.

    :param doc: to split
    :return: the list of sentence strings from the document
    """
    sentences = []
    sentence_start = 0
    for i in range(len(doc)):
        if doc[i] in ('.', '?', '!'):
            sentences.append(doc[sentence_start:i])
            if i != len(doc) - 1 and doc[i+1] == ' ':
                sentence_start = i + 2
            else:
                sentence_start = i + 1
        else:
            if i == len(doc) - 1:
                sentences.append(doc[sentence_start:i + 1])
    return sentences


def tokenize_sentence(sentence):
    """
    Tokenize sentence into list of words.

    :param sentence: to tokenize
    :return: the list of words in the sentence
    """
    tokens = []
    token_start = 0
    for i in range(len(sentence)):
        if sentence[i] == ' ':
            tokens.append(sentence[token_start:i])
            token_start = i + 1
        if i == len(sentence) - 1:
            tokens.append(sentence[token_start:i+1])
    return tokens

if __name__ == '__main__':
    doc = 'Every good boy deserves fudge! All cows eat grass.'
    print(doc)
    print(tokenize_document(doc))

