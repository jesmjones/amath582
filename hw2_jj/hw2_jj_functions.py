# -*- coding: utf-8 -*-
"""hw2_jj_functions

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-OaTzxUxidzUqzH6sWEswNhV1Cb_slST
"""

def grabDigits(X_data, y_data, digits=None):
# write a function that extracts the features and labels of the digits 1 and 8 from the training dataset
    digit_locations = np.where(np.isin(y_data, digits))[0] # Find rows of matching entries
    y_new = y_data[digit_locations] ; X_new = X_data[digit_locations, :] # data
    
    return X_new, y_new

def reduceData(X, N):
# project X(1,8) on the first 16 PCA modes of 𝑋train computed in step 1
    pca_model = PCA(); pca_model.fit(X)
    all_comp = np.copy(pca_model.components_) # copies components
    X_pca = pca_model.transform(X) # transforms data
    X_reduced = np.dot(X - pca_model.mean_, pca_model.components_[:N].T) # reduce data to n components
    pca_model.components_[N:] = 0 ; pca_model.components_ = all_comp # only save n components and resets them
    
    return X_reduced

def ridgeModel(train_X, test_X, train_Y, test_Y, N, alpha=None, digits=None):
    # make training and test datasets
    redX_train = reduceData(train_X,N); redX_test = reduceData(test_X, N);
    A_train, y_train = grabDigits(redX_train, train_Y,  digits=digits); b_train = np.where(y_train == digits[0], -1, 1) # assign -1 to first digit and +1 to second
    A_test, y_test = grabDigits(redX_test, test_Y,  digits=digits); b_test = np.where(y_test == digits[0], -1, 1)
    # ridge regression model
    ridge = Ridge(alpha=alpha, random_state=None); ridge.fit(A_train, b_train) # Fit on training data
    A_train, b_train = shuffle(A_train, b_train, random_state=None) # Shuffle after fitting
    # predict on train and test data
    y_train_pred = ridge.predict(A_train) ; y_test_pred = ridge.predict(A_test)
    # do MSE calcs
    train_mse = mean_squared_error(y_train_pred, b_train) # train MSE
    test_mse = mean_squared_error(y_test_pred, b_test) # test MSE
    y_train_pred_binary = np.where(y_train_pred <= 0, -1, 1) # Convert to classes
    y_test_pred_binary = np.where(y_test_pred <= 0, -1, 1) # Convert to absolutes
    train_correct = np.count_nonzero(y_train_pred_binary == b_train) / len(y_train_pred) # % correct train
    test_correct = np.count_nonzero(y_test_pred_binary == b_test) / len(y_test_pred) # % correct test

    return train_mse, train_correct,  test_mse, test_correct, A_test, y_test, y_test_pred, A_test, b_test

def numMisclassified(rr):
    # how many misclassified samples in the test set.
    sel = rr[6] != rr[8]; n_mc = np.sum(sel) # number misclassified
    X_mc = rr[4][sel,:]; y_mc = rr[8][sel]; yp_mc = rr[6][sel]
    idx = np.argsort(y_mc); X_mc = X_mc[idx,:]; y_mc = y_mc[idx]; yp_mc = yp_mc[idx]
    rows = math.ceil(n_mc / 6)

    return n_mc