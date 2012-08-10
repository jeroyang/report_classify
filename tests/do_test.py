from nose.tools import *
from report_classify.do import *
import csv

def test_preprocess():
    report1 = """Brain CT without contrast study shows :
    1. Cortical and subcortical low density of bilateral fronal lobes. 
    2. The ventricular system are normal in bilateral sides.
    3. No evidence of middle line shifting.
    4. The nasal and paranasal sinus show unremarkable.
    5. No evidence of skull bone fracture.
    6. Microangiopathic ischemic encephalopathy in periventricular white matter. 

    IMP: 
      Rule out infarcts or encephlomalacia of bilateral frontal lobes."""
      
    report2 = """Brain CT without contrast study shows :
      1. Symmetric appearance of bilateral hemisphere without abnormal hypo or hyper- densities.
      2. The ventricular system are normal in bilateral sides.
      3. No evidence of middle line shifting.
      4. The nasal and paranasal sinus show unremarkable.
      5. No evidence of skull bone fracture.

      IMP: 
        Unremarkable of this non-contrast enhanced brain CT study. Rule out infarcts or encephlomalacia of bilateral frontal lobes."""
    
    assert_equal("Rule out infarcts or encephlomalacia of bilateral frontal lobes.", preprocess(report1))
    assert_equal("Unremarkable of this non-contrast enhanced brain CT study. \nRule out infarcts or encephlomalacia of bilateral frontal lobes.", preprocess(report2))

def test_feature_select():
    impression1 = "Rule out infarcts or encephlomalacia of bilateral frontal lobes."
    impression2 = "Unremarkable of this non-contrast enhanced brain CT study. \nRule out infarcts or encephlomalacia of bilateral frontal lobes."
    assert_equal(feature_select(impression1), [1, 0, 2])
    assert_equal(feature_select(impression2), [1, 1, 2])

def test_classify():
    feature1 = [0, 0, 0]
    feature2 = [0, 0, 1]
    feature3 = [0, 1, 0]
    feature4 = [0, 1, 1]
    feature5 = [1, 0, 0]
    feature6 = [1, 0, 1]
    feature7 = [1, 1, 0]
    feature8 = [1, 1, 1]
    assert_equal(classify(feature1), 'N')
    assert_equal(classify(feature2), 'N')
    assert_equal(classify(feature3), 'N')
    assert_equal(classify(feature4), 'Y')
    assert_equal(classify(feature5), 'Y')
    assert_equal(classify(feature6), 'Y')
    assert_equal(classify(feature7), 'Y')
    assert_equal(classify(feature8), 'Y')

        
"""    
def test_others():
    test_filename = "tests/out_gold_smallSample.csv"
    test_file = csv.DictReader(open(test_filename))
    for row in test_file:
        assert_equal(classify(feature_select(row['text'])), row['yn'])
"""