from Solutions import read_file, calculate_percent_increase, get_eliminate, get_mutual_info_score, get_unique_count
import pytest
import pandas as pd
import random


###################### Test 1 ########################
def test_read_file():
    df = read_file()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (254, 255)
##################### End Test 1 ######################


##################### Test 2 ##########################

x = [{}, {}, {}, {}]

x[0]['C3) Funding FY2010'] = 3
x[0]['C1) Funding FY2008'] = 2

x[1]['C3) Funding FY2010'] = 3.44
x[1]['C1) Funding FY2008'] = 5.23

x[2]['C3) Funding FY2010'] = 2.3
x[2]['C1) Funding FY2008'] = 1.33

x[3]['C3) Funding FY2010'] = 2.34
x[3]['C1) Funding FY2008'] = 4.22

@pytest.mark.parametrize("inputs, expected_outputs",
                         [
                             (x[0], 50),
                             (x[1], -34.2256),
                             (x[2], 72.9323),
                             (x[3], -44.5498)
                         ]
                         )
def test_calculate_percent_increase(inputs, expected_outputs):
    res = calculate_percent_increase(inputs)
    res = round(res, 4)
    assert res == expected_outputs
##################### End Test 2 ######################

##################### Test 3 ##########################


df = pd.DataFrame({'Age': range(16, 32), 'Cars': [1, 2, 3, 4]*4, 'Target Variable': [0, 0, 1, 1]*4})


def test_get_eliminate():
    eliminate = get_eliminate(df)
    assert 'Age' in eliminate
    assert 'Cars' not in eliminate
    assert 'Target Variable' not in eliminate

##################### End Test 3 ######################

##################### Test 4 ##########################

df2 = pd.DataFrame({'Age': range(16, 32), 'Cars': [1, 1, 3, 3]*4, 'Target Variable': [1, 43, 2, 323]*4})

def test_get_mutual_info_score():
    ans = get_mutual_info_score(df2)
    assert round(ans['Mutual Info Score'][0], 4) == 1.3863
    assert round(ans['Mutual Info Score'][1], 4) == 0.6931

##################### End Test 4 ######################

def test_get_unique_count():
    count_df = get_unique_count(df)
    print(count_df)
    assert int(count_df[count_df['Column Name'] == 'Target Variable']['Unique Count'] == 2)
    assert int(count_df[count_df['Column Name'] == 'Cars']['Unique Count'] == 4)
    assert int(count_df[count_df['Column Name'] == 'Age']['Unique Count'] == 16)
