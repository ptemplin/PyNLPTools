import math

from extraction import wordfrequency
from extraction.coca import extractor
from semantics.distributed import cooccurrence


def ppmi_similarity(target_word, context_word, co_occurrences, word_id, word_frequency, count):
    """
    Compute PPMI as log2(P(word1,word2)/(P(word1)*P(word2)))

    :param target_word: the target word
    :param context_word: the context word
    :param co_occurrences: the number of co-occurrences between each pair of words in the corpus
    :param word_id: the word to wordID mapping used in co_occurrences
    :param word_frequency: the frequency of each word in the corpus
    :param count: the number of word occurrences in the corpus
    :return:
    """
    target_id = word_id[target_word]
    context_id = word_id[context_word]
    target_occurrences = word_frequency[target_word]
    context_occurrences = word_frequency[context_word]
    if context_id not in co_occurrences[target_id]:
        return 0
    cooccurrence_prob = co_occurrences[target_id][context_id]/target_occurrences
    target_occurrence_prob = target_occurrences/count
    context_occurrence_prob = context_occurrences/count
    pmi = math.log2(cooccurrence_prob/(target_occurrence_prob*context_occurrence_prob))
    if pmi < 0:
        return 0
    else:
        return pmi


def cosine_similarity(v1, v2):
    """
    Computes the cosine similarity measure of v1 and v2. Len(v1) must equal len(v2).

    :param v1: co-occurrence matrix of word 1
    :param v2: co-occurrence matrix of word 2
    :return: the cosine similarity of the two words
    """
    v1_len = 0
    v2_len = 0
    dot_product = 0

    for context_id, count in v1.items():
        v1_len += count ** 2
        if context_id in v2:
            dot_product += count*v2[context_id]
    for count in v2.values():
        v2_len += count ** 2

    v1_len = math.sqrt(v1_len)
    v2_len = math.sqrt(v2_len)
    return dot_product/(v1_len * v2_len)

if __name__ == '__main__':
    documents = extractor.extract_all()
    co_occurrences, word_id, id_word = cooccurrence.word_to_word_cooccurrence(documents)
    word_freq, full_count = wordfrequency.word_frequency_documents(documents)
    while True:
        user_input = input('Enter two words. \'q\' to quit\n')
        if user_input == 'q':
            break
        else:
            words = user_input.split()
            if words[0] in word_id and words[1] in word_id:
                v1 = co_occurrences[word_id[words[0]]]
                v2 = co_occurrences[word_id[words[1]]]
                print('Cosine:', cosine_similarity(v1, v2))
                print('PPMI:', ppmi_similarity(words[0], words[1], co_occurrences, word_id, word_freq, full_count))
            else:
                print('Unknown word')