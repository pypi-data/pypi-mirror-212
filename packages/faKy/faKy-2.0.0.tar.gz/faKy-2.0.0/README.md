# faKy
We introduce faKy, a feature extraction library in the scope of fake news. It includes functions for calculating the readability scores, Information complexity, sentiment analysis using VADER,  Named Entities, and part-of-speech tags. With these functions, relevant features for fake news detection can be computed. Furthermore, we provide a Dunn test function which can be used to test the significance between multiple independent variables. 

With the development of faKy, we hope to contribute to more sophisticated and interpretable ML models and better comprehend the phenomenon of fake news by understanding these objects’ underlying different linguistic features.

## Installation
FaKy can be installed through pip install faKy; the NLTK and spaCy's web_core_web_md are automatically installed within the faKy library

## faKy 101
The use case of faKy is the computation of features based on text objects; the faKy library can be used to compute the features for all the text objects in the data frame. See the example code block.

Import the faky library and the corresponding function:
    from faKy.faKy import process_text_readability

Apply process_text_readability to the data frame
    dummy_df['readability'] = dummy_df['text-object'].apply(process_text_readability)

# faKy functionality
| Function Name             | Usage                                                                                                                                                            |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| readability_computation   | Computes the Flesch-Kincaid Reading Ease score for a spaCy document using the Readability class. Returns the original document object.                           |
| process_text_readability  | Takes a text string as input, processes it with spaCy's NLP pipeline, and computes the Flesch-Kincaid Reading Ease score. Returns the score.                       |
| compress_doc              | Compresses the serialized form of a spaCy Doc object using gzip, calculates the compressed size, and sets the compressed size to the custom "compressed_size" attribute of the Doc object. Returns the Doc object. |
| process_text_complexity   | Takes a text string as input, processes it with spaCy's custom NLP pipeline, and computes the compressed size. Returns the compressed size of the string in bits. |
| VADER_score               | Takes a text input and calculates the sentiment scores using the VADER sentiment analysis tool. Returns a dictionary of sentiment scores.                          |
| process_text_vader        | Takes a text input, applies the VADER sentiment analysis model, and returns the negative, neutral, positive, and compound sentiment scores as separate variables.  |
| count_named_entities      | Takes a text input, identifies named entities using spaCy, and returns the count of named entities in the text.                                                 |
| count_ner_labels          | Takes a text input, identifies named entities using spaCy, and returns a dictionary of named entity label counts.                                               |
| create_input_vector_NER   | Takes a dictionary of named entity recognition (NER) label counts and creates an input vector with the count for each NER label. Returns the input vector.         |
| count_pos                 | Counts the number of parts of speech (POS) in a given text. Returns a dictionary with the count of each POS.                                                    |
| create_input_vector_pos   | Takes a dictionary of POS tag counts and creates an input vector of zeros. Returns the input vector.                                                             |
| values_by_label           | Takes a DataFrame, a feature, a list of labels, and a label column name. Returns a list of lists containing the values of the feature for each label.             |
| dunn_table                | Takes a DataFrame of Dunn's test results and creates a new DataFrame with pairwise comparisons between groups. Returns the new DataFrame.                           |
    