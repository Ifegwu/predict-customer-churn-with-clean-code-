'''
Module contains test for churn customer analysis

Author: Ifegwu Daniel Agbanyim

Date: 28th October 2022
'''

# Import libaries
import os
import logging
import time
from math import ceil
import churn_library as clib

# logging configuration
logging.basicConfig(
    filename=f"./logs/churn_library_{time.strftime('%b_%d_%Y_%H_%M_%S')}.log",
    level=logging.INFO,
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s")


def test_import():
    '''
    test data import - this example is completed for you to assist with the other test functions
    '''
    try:
        dataframe = clib.import_data("./data/bank_data.csv")
        logging.info("Testing import_data: SUCCESS")
    except FileNotFoundError as err:
        logging.error("Testing import_eda: The file wasn't found")
        raise err

    try:
        assert dataframe.shape[0] > 0
        assert dataframe.shape[1] > 0
        logging.info('Rows: %d\tColumns: %d',
                     dataframe.shape[0], dataframe.shape[1])
    except AssertionError as err:
        logging.error(
            "Testing import_data: The file doesn't appear to have rows and columns")
        raise err


def test_eda():
    '''
    test perform eda function
    '''

    dataframe = clib.import_data("./data/bank_data.csv")

    try:
        clib.perform_eda(dataframe=dataframe)
        logging.info("Testing perform_eda: SUCCESS")
    except KeyError as err:
        logging.error('Column "%s" not found', err.args[0])
        raise err

    # Assert that `churn_dist.png` is created
    try:
        assert os.path.isfile("./images/eda/churn_dist.png") is True
        logging.info('File %s was found', 'churn_dist.png')
    except AssertionError as err:
        logging.error('No such file on the disk')
        raise err

    # Assert that `customer_age_dist.png` is created
    try:
        assert os.path.isfile("./images/eda/customer_age_dist.png") is True
        logging.info('File %s was found', 'customer_age_dist.png')
    except AssertionError as err:
        logging.error('No such file on the disk')
        raise err

    # Assert that `dataframe.png` is created
    try:
        assert os.path.isfile("./images/eda/dataframe.png") is True
        logging.info('File %s was found', 'dataframe.png')
    except AssertionError as err:
        logging.error('No such file on the disk')
        raise err

    # Assert that `heatmap.png` is created
    try:
        assert os.path.isfile("./images/eda/heatmap.png") is True
        logging.info('File %s was found', 'heatmap.png')
    except AssertionError as err:
        logging.error("No such file on the disk")
        raise err

    # Assert that `marital_status_dist.png` is created
    try:
        assert os.path.isfile("./images/eda/marital_status_dist.png") is True
        logging.info('File %s was found', 'marital_status_dist.png')
    except AssertionError as err:
        logging.error('No such file on the disk')
        raise err

    # Assert that `total_transaction_dist.png` is created
    try:
        assert os.path.isfile(
            "./images/eda/total_transaction_dist.png") is True
        logging.info("File %s was found", "total_transaction_dist.png")
    except AssertionError as err:
        logging.error("No such file found on the disk")
        raise err


def test_encoder_helper():
    '''
    test encoder helper
    '''
    # Load Dataframe
    dataframe = clib.import_data("./data/bank_data.csv")

    # Create `Churn` feature
    dataframe['Churn'] = dataframe['Attrition_Flag'].apply(
        lambda val: 0 if val == "Existing Customer" else 1)

    # Group categorical features
    cat_columns = ['Gender', 'Education_Level',
                   'Marital_Status', 'Income_Category', 'Card_Category']

    # Assert data should be thesame
    try:
        encoded_df = clib.encoder_helper(
            dataframe=dataframe, category_lst=[], response=None)

        # Data should be thesame
        assert encoded_df.equals(dataframe) is True
        logging.info(
            "Testing encoder_helper(data_frame, category_lst=[]): SUCCESS")
    except AssertionError as err:
        logging.error(
            "Testing encoder_helper(data_frame, category_lst=[]): ERROR")
        raise err

    # Assert that column names should be thesame and data should be different
    try:
        encoded_df = clib.encoder_helper(
            dataframe=dataframe, category_lst=cat_columns, response=None)

        # Column names should be thesame
        assert encoded_df.columns.equals(dataframe.columns) is True

        # Data should be different
        assert encoded_df.equals(dataframe) is False
        logging.info(
            "Testing encoder_helper(data_frame, category_lst=cat_columns, response=None): SUCCESS")

    except AssertionError as err:
        logging.error(
            "Testing encoder_helper(data_frame, category_lst=cat_columns, response=None): ERROR")
        raise err

    # Assert that columns names should be different,
    # data should be different, and Number of columns in encoded_df is
    # the sum of columns in data_frame and the newly created columns from
    # cat_columns

    try:
        encoded_df = clib.encoder_helper(
            dataframe=dataframe, category_lst=cat_columns, response='Churn')

        # Column names should be different
        assert encoded_df.columns.equals(dataframe.columns) is False

        # Data should be different
        assert encoded_df.equals(dataframe) is False

        # Number of columns in encoded_df is the sum of columns
        # in data_frame and the newly created columns from cat_columns
        assert len(encoded_df.columns) == len(
            dataframe.columns) + len(cat_columns)
        logging.info(
            "Testing encoder_helper(data_frame, category_lst=cat_columns, response='Churn'): SUCCESS")
    except AssertionError as err:
        logging.error(
            "Testing encoder_helper(data_frame, category_lst=cat_columns, response='Churn'): ERROR")
        raise err


def test_perform_feature_engineering():
    '''
    test perform_feature_engineering function from churn_library module
    '''

    # Load the dataframe
    dataframe = clib.import_data("./data/bank_data.csv")

    # Churn feature
    dataframe['Churn'] = dataframe['Attrition_Flag'].apply(
        lambda val: 0 if val == "Existing Customer" else 1)

    try:
        (_, X_test, _, _) = clib.perform_feature_engineering(
            dataframe=dataframe,
            response='Churn')

        # `Churn` must be present in `dataframe`
        assert 'Churn' in dataframe.columns
        logging.info(
            "Testing perform_feature_engineering. `Churn` column is present: SUCCESS")
    except KeyError as err:
        logging.error(
            'The `Churn` column is not present in the dataframe: ERROR')
        raise err

    try:
        # X_test size should be 30% of `dataframe`
        assert (X_test.shape[0] == ceil(dataframe.shape[0] * 0.3)) is True
        logging.info(
            'Testing perform_feature_engineering. DataFrame sizes are consistent: SUCCESS')
    except AssertionError as err:
        logging.error(
            'Testing perform_feature_engineering. DataFrame sizes are not correct: ERROR')
        raise err


def test_train_models():
    '''
    test train_models function from churn_library module
    '''
    # Load the dataframe
    dataframe = clib.import_data("./data/bank_data.csv")

    # Churn feature
    dataframe['Churn'] = dataframe['Attrition_Flag'].apply(
        lambda val: 0 if val == "Existing Customer" else 1
    )

    # Feature engineering
    (X_train, X_test, y_train, y_test) = clib.perform_feature_engineering(
        dataframe=dataframe,
        response='Churn')

    # Assert that `logistic_model.pkl` file exists
    try:
        clib.train_models(X_train, X_test, y_train, y_test)
        assert os.path.isfile("./models/logistic_model.pkl") is True
        logging.info('File %s was found', 'logistic_model.pkl')
    except AssertionError as err:
        logging.error('No such file on the disk')
        raise err

    # Assert that `rfc_model.pkl` file exist
    try:
        assert os.path.isfile("./models/rfc_model.pkl") is True
        logging.info('File %s was found', 'rfc_model.pkl')
    except AssertionError as err:
        logging.error('No such file on disk')
        raise err

    # Assert that `roc_curve_result.png` file is present
    try:
        assert os.path.isfile('./images/results/roc_curve_result.png') is True
        logging.info('File %s was found', 'roc_curve_result.png')
    except AssertionError as err:
        logging.error('No such file on disk')
        raise err

    # Assert that `rfc_results.png` file is present
    try:
        assert os.path.isfile('./images/results/rf_results.png') is True
        logging.info('File %s was found', 'rf_results.png')
    except AssertionError as err:
        logging.error('No such file on disk')
        raise err

    # Assert that `logistic_results.png` file is present
    try:
        assert os.path.isfile('./images/results/logistic_results.png') is True
        logging.info('File %s was found', 'logistic_results.png')
    except AssertionError as err:
        logging.error('No such file on disk')
        raise err

    # Assert that `feature_importances.png` file is present
    try:
        assert os.path.isfile(
            './images/results/feature_importances.png') is True
        logging.info('File %s was found', 'feature_importances.png')
    except AssertionError as err:
        logging.error('No such file on disk')
        raise err


if __name__ == "__main__":
    test_import()
    test_eda()
    test_encoder_helper()
    test_perform_feature_engineering()
    test_train_models()
