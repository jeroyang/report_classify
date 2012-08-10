"""
do.py

Created by Jerome Yang on 2012-03-31.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import re

def sentence_counter(s):
    counter = 0
    sentences = re.split(r'[.!?][ \n]*[A-Z]', s)
    for sentence in sentences:
        if re.search(r'[a-z]{3,}', sentence, flags=re.I): # Ignore the sentences shorter than 3 characters
            counter = counter + 1
    return counter

def preprocess(s, has_header=True):
    if has_header == True:
        s = re.sub(r'^.*?(CT|MRI|IMP).*?[.:\n\r]', '', s) # Cut the head
        
    s = re.sub(r'.*imp(ression)?[: \n]+(.*)', r'\2', s, flags=re.I|re.S) # Keep the impression
    s = re.sub(r'^[\d.\-~ \\]+', '', s, flags=re.M) # Remove the leading numbers and bullets
    s = re.sub(r'\blt\b\.?', 'left', s, flags=re.I) # lt -> left
    s = re.sub(r'\brt\b\.?', 'right', s, flags=re.I) # rt -> right    
    s = re.sub(r'(\s)\1+', ' ', s, flags=re.S) # Remove redundant white spaces and line breaks
    s = re.sub(r'([a-z]) *\n *([a-z])', r'\1 \2', s, flags=re.S) # Glue the layout linebreaks
    s = re.sub(r'(.*?[.?]) +([A-Z])', r'\1 \n\2', s) # Segmentation of sentences
    return s

def feature_select(s):
    negative_sentences = re.findall(r'(^.*?(not|less) (consider|likely|favor).*?$|^.*?(no |free from|free of|unremarkable|negative|normal|clear|neither).*?$)', s, flags=re.M|re.I)
    positive_lexicons = re.findall(r'(right|left|bilateral|upper|lower|outer|inner|medial|lateral|superior|inferior|post|status|disease|disorder|syndrome|acute|chronic|tumor|cancer|malignan|benign|cm|mm|R\/O|rule out|consider|indicat|favor|suggest|compatible|suspicious|consist|due to) ', s, flags=re.S|re.I|re.U)
    s = re.sub(r'(^.*?(not|less) (consider|likely|favor).*?$|^.*?(no |free from|free of|unremarkable|negative|normal|clear|neither).*?$)', ' ', s, flags=re.M|re.I) # Remove negative sentences
    s = re.sub(r'(^((?!or).)*artifacts?((?!or).)*$)', ' ', s, flags=re.M|re.I) # Remove artifact sentences
    s = re.sub(r'(^.*?(please|recommend|correlat).*$)', ' ', s, flags=re.M|re.I) # Remove artifact sentences
    s = re.sub(r'(\s)\1+', ' ', s, flags=re.S) # Remove redundant white spaces and line breaks
    s = re.sub(r'\n$', '', s, flags=re.S) # Remove the last newline or whitespace
    return [sentence_counter(s), len(negative_sentences), len(positive_lexicons)]

def classify(features):
    if features[0]>0 or (features[1]>0 and features[2]>0):
        return 'Y'
    else:
        return 'N'

def do(report):
    print classify(feature_select(preprocess(report)))

def feature_select_all():
    re_for_non_positive_sentence = [r'(^.*?(not|less) (consider|likely|favor).*?$)',
                         r'(^.*?(no |free from|free of|unremarkable|negative|normal|clear|neither).*?$)',
                         r'(^.*?(please|recommend|correlat).*$)',
                         r'(^((?!or).)*artifacts?((?!or).)*$)', 
                         r'(^((?!or).)*(aging|physiologic(al)? change|variation|variant)((?!or).)*$)' ]
    re_for_positive_lexicon = r'(right|left|bilateral|upper|lower|outer|inner|medial|lateral|superior|inferior|post|status|disease|disorder|syndrome|acute|chronic|tumor|cancer|malignan|benign|cm|mm|R\/O|rule out|consider|indicat|favor|suggest|compatible|suspicious|consist|due to) '

    feature_rules = [re_for_non_positive_sentence[:3],
                     re_for_non_positive_sentence[:4],
                     re_for_non_positive_sentence,
                     re_for_non_positive_sentence,
                     re_for_non_positive_sentence,
                     ]

def main(argv):
    pass


if __name__ == '__main__':
    main(sys.argv[1:])

