#Import readability components
from .faKy import process_text_readability
#Import complexity components
from .faKy import process_text_complexity
#Import sentiment components
from .faKy import process_text_vader
#Import NER components
from .faKy import count_named_entities, count_ner_labels, create_input_vector_NER, ner_labels
#Import POS components
from .faKy import count_pos, create_input_vector_pos, pos_tags
#Import statistical components
from .faKy import values_by_label, dunn_table

'''
Users can only import these functions from the faKy libarary, the under the hood functions are not accessible to the user.
'''

__all__ = ['process_text_readability, process_text_complexity, process_text_vader, count_named_entities, count_ner_labels, create_input_vector_NER, ner_labels, count_pos, create_input_vector_pos, pos_tags, values_by_label, dunn_table']