from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import  classification_report, confusion_matrix, f1_score, make_scorer
import patsy
import itertools
import pandas as pd
import numpy as np


def pretty_coefficients(result, exog_train):

    '''Reformulates the summary function from a logistic model: removes confidence interval columns, z values
    add ads odd-ratio columns. Also cleans the variable names so they are more readable


    INPUTS

        - result (sklearn.linear_model._logistic.LogisticRegression): a fitted logistic regression model using the scikit-learn package
        - exog_df (DesignMatrix): matrix with the exogenous variables generated with the ptasy package

    RETURNS

        A DataFrame with the reformatted logistic model coefficients.
    '''

    # get the table from the summary obect
   # summary_df = pd.DataFrame(summary.tables[1].data[1:], columns = summary.tables[1].data[0])

    # Generate coeficients and feature names
    coef = result.coef_
    features = exog_train.design_info.column_names


    # transform into data frame
    summary_df = pd.DataFrame(data = {"Feature": features, "Coef": coef[0]})

    # clean variable names
    summary_df["Feature"] = summary_df.Feature.apply(lambda x: x.replace("C(offer_type, Treatment('Informational'))", ""))

    # generate Odds ratio measure
    summary_df["odds ratio"] = summary_df.Coef.apply(lambda x: np.exp(x))
    summary_df[["Coef", "odds ratio"]] = summary_df[["Coef", "odds ratio"]].round(3)

    return summary_df


def expand_grid(*args, var_names):

    """
    Takes any number of iterables as arguments
    and returns a data frame with the cartessian product.

    INPUTS

     - *args: a number of iterables from which values are crossed
     - var_names: the column names for the DataFrame generated

     RETURNS

         A DataFrame in which the rows contain every single combination of values resulting crossing the iterables in *args
    """

    return pd.DataFrame(columns = var_names, data = list(itertools.product(*args)))


def fit_logistic(offers, model_vars, interaction=False, param_grid=None):
    '''Fits a logistic regression for the offers dataframe, having "completed" as dependent variable and
    "offer_type" as one of its independent variables. It deals with the data preparation including
    separating training and test set, and write a formula for fitting the model.

    INPUTS

        - offers (DataFrame): data with the offers
        - model_vars (list): variable names from the offers dataset, excluding offer_type, that serve as the indep. variables
        - ineraction (bool): flag indicating if the model to be fit includes interaction terms for offer type
        - param_grid (list): list of strings specifying the hyperparameters to tune


    RETURNS

        - result : fitted logistic regression model for the offers dataset, fitted with the statsmodel package
        - forula: a string with the formula containing the independent variables from the model
        - exog_train: DesignMatrix from the pasty package with the data for the independent variables in the training set
        - exog_val: DesignMatrix from the patsy package with the data for the independent variables in the validation set
        - X_val: DataFrame for the independent variables from the validation set
        - y_val: array for the "completed" variable, our dependent variable in the model

    '''

    # sets Informational as base category for offer_type
    base_category = 'Informational'
    offer_base = "C(offer_type, Treatment('{0}'))".format(base_category)

    # construtio of the formula for the model
    join_string = [" + ", ":{0} + "][interaction * 1]
    formula = join_string.join(model_vars)

    if interaction:
        formula += ":{0}"

    else:
        formula = "{0} + " + formula

    formula = formula.format(offer_base)

    # inclusion of dependent and offer_type to create train and tests sets
    model_data = offers[["completed"] + ["offer_type"] + model_vars]

    train, val = train_test_split(model_data, test_size=0.2, random_state=123)

    # obtaining data for the model from formulas
    y_train = train["completed"]
    X_train = train.drop("completed", axis=1)

    y_val = val["completed"]
    X_val = val.drop("completed", axis=1)

    exog_train = patsy.dmatrix(formula, data=X_train)
    exog_val = patsy.dmatrix(formula, data=X_val)

    scoring = make_scorer(f1_score)

    # fit model

    lg = LogisticRegression(max_iter=2000)

    if param_grid is not None:

        # gris search
        lg = GridSearchCV(lg, param_grid=param_grid, scoring=scoring)
        lg.fit(exog_train, y_train)

        # reffit the beest stimator in the entire dataset
        lg = lg.best_estimator_

        result = lg.fit(exog_train, y_train)

    else:

        result = lg.fit(exog_train, y_train)

    return result, formula, exog_train, exog_val, X_val, y_val


def model_outcome(result, exog_val, y_val):
    '''Prints the outcome of the model based on the predictions in a validation set

    INPUTS

    - results: fitted regression model generated by fit_logistic
    - exog_val: DesignMatrix from the patsy package with the data form the independent variables
    - y_val: array for the "completed" variable, our dependent variable in the model

    RETURNS

    (none): the function prints the output in the form of a confusion matrix and the precision, recall and F score
    '''

    y_val_pred = (result.predict(exog_val) > 0.5).astype(int)
    accuracy = (y_val == y_val_pred).mean()

    print("Accuracy: ", accuracy)
    print("")
    print("Confusion matrix")
    print(confusion_matrix(y_val, y_val_pred))
    print("")
    print("Calssification report")
    print(classification_report(y_val, y_val_pred, digits=2))

