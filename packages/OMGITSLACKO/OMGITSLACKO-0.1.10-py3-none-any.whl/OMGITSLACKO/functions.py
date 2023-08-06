

def correlation(df, x_variable=None):
    import pandas as pd
    from IPython.core.display import HTML
    if x_variable:
        corr = df.corr()[x_variable].sort_values(ascending=False).drop(x_variable)
    else:
        corr = df.corr().stack().reset_index()
        corr.columns = ['var1', 'var2', 'corr']
        corr = corr[(corr['corr'] != 1.0) & (corr['corr'] != -1.0)]
        corr = corr[corr['var1'] < corr['var2']]
        corr.sort_values(by=['corr'], ascending=False, inplace=True)

    html_table = '<table><thead><tr><th>Variable 1</th><th>Variable 2</th><th>Correlation</th></tr></thead>'
    html_table += '<tbody>'
    
    if x_variable:
        for index, row in corr.iteritems():
            html_table += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(x_variable, index, round(row, 2))
    else:
        for index, row in corr.iterrows():
            html_table += '<tr><td>{}</td><td>{}</td><td>{}</td></tr>'.format(row['var1'], row['var2'], round(row['corr'], 2))
            
    html_table += '</tbody></table>'
    
    return HTML('<div style="max-height:300px; overflow-y:auto;">{}</div>'.format(html_table))

def plot_side_by_side(data, columns):
    import pandas as pd
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(len(columns), 2, figsize=(12, len(columns) * 4))

    for i, col in enumerate(columns):
        axs[i, 0].plot(data[col].values)
        axs[i, 0].set_title(f"{col} - Time Series")
        axs[i, 0].set_xlabel("Index")
        axs[i, 0].set_ylabel("Value")

        axs[i, 1].hist(data[col], bins=20)
        axs[i, 1].set_title(f"{col} - Histogram")
        axs[i, 1].set_xlabel("Value")
        axs[i, 1].set_ylabel("Frequency")

    plt.tight_layout()

    plt.figure(figsize=(12, 6))
    for col in columns:
        plt.plot(data[col].values, label=col)
    plt.title("Time Series Comparison")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.legend()

    plt.show()




def plot_target_vs_others(data, target_variable):
    import pandas as pd
    import matplotlib.pyplot as plt
    target = data[target_variable]
    other_variables = data.drop(columns=target_variable).columns
    
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(target)), target, label=target_variable)
    plt.title(f"{target_variable} - Time Series")
    plt.xlabel("Data Point")
    plt.ylabel("Value")
    plt.legend()
    plt.show()
    
    for variable in other_variables:
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(target)), target, label=target_variable)
        plt.plot(range(len(data[variable])), data[variable], label=variable)
        plt.title(f"{target_variable} vs {variable} - Time Series")
        plt.xlabel("Data Point")
        plt.ylabel("Value")
        plt.legend()
        plt.show()


def plot_target_vs_others_normalized(data, target_variable):
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import MinMaxScaler
    target = data[target_variable]
    other_variables = data.drop(columns=target_variable).columns
    
    data_without_target = data.drop(columns=target_variable)
    
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(data_without_target)
    
    target_scaler = MinMaxScaler()
    normalized_target = target_scaler.fit_transform(target.values.reshape(-1, 1))
    
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(normalized_target)), normalized_target, label=target_variable)
    plt.title(f"{target_variable} - Time Series (Normalized)")
    plt.xlabel("Data Point")
    plt.ylabel("Normalized Value")
    plt.legend()
    plt.show()
    
    for variable in other_variables:
        variable_index = data.columns.get_loc(variable)
        normalized_variable = normalized_data[:, variable_index]
        
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(normalized_target)), normalized_target, label=target_variable)
        plt.plot(range(len(data)), normalized_variable, label=variable)
        plt.title(f"{target_variable} vs {variable} - Time Series (Normalized)")
        plt.xlabel("Data Point")
        plt.ylabel("Normalized Value")
        plt.legend()
        plt.show()


    
def find_best_model_classification(df_X_train, df_X_test, df_y_train, df_y_test):
    
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LogisticRegression, RidgeClassifier, PassiveAggressiveClassifier, Perceptron
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier, ExtraTreesClassifier, BaggingClassifier, IsolationForest, StackingClassifier
    from sklearn.svm import SVC, OneClassSVM
    from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
    from sklearn.naive_bayes import GaussianNB, BernoulliNB
    from sklearn.neural_network import MLPClassifier
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
    from sklearn.cluster import KMeans
    from xgboost import XGBClassifier
    from lightgbm import LGBMClassifier
    from catboost import CatBoostClassifier
    from imblearn.ensemble import BalancedRandomForestClassifier
    from sklearn import metrics
    
    models = [
        ("Logistic Regression", LogisticRegression(max_iter=1000)),
        ("Decision Tree", DecisionTreeClassifier()),
        ("Random Forest", RandomForestClassifier()),
        ("Gradient Boosting", GradientBoostingClassifier()),
        ("XGBoost", XGBClassifier(eval_metric="logloss")),
        ("LightGBM", LGBMClassifier()),
        ("Support Vector Machine", SVC()),
        ("K-Nearest Neighbors", KNeighborsClassifier()),
        ("Naive Bayes", GaussianNB()),
        ("Multi-layer Perceptron", MLPClassifier(max_iter=1000)),
        ("AdaBoost", AdaBoostClassifier()),
        ("Extra Trees", ExtraTreesClassifier()),
        ("Ridge Classifier", RidgeClassifier()),
        ("Quadratic Discriminant Analysis", QuadraticDiscriminantAnalysis()),
        ("CatBoost", CatBoostClassifier(verbose=0, random_seed=42)),
        ("Balanced Random Forest", BalancedRandomForestClassifier()),
        ("Linear Discriminant Analysis", LinearDiscriminantAnalysis()),
        ("Nearest Centroid Classifier", NearestCentroid()),
        ("Passive Aggressive Classifier", PassiveAggressiveClassifier()),
        ("Perceptron", Perceptron()),
        ("Bernoulli Naive Bayes", BernoulliNB()),
        ("Bagging Classifier", BaggingClassifier()),
        # Add a base estimator for StackingClassifier
        ("Stacking Classifier", StackingClassifier(estimators=[('lr', LogisticRegression()), ('dt', DecisionTreeClassifier())])),
    ]


    best_model = None
    best_accuracy = -1
    best_model_instance = None

    for name, model in models:
        model.fit(df_X_train, df_y_train)
        y_pred_binary = model.predict(df_X_test)

        if name in ["Isolation Forest", "One-Class SVM", "K-Means"]:
            y_pred_binary = np.where(y_pred_binary == -1, 0, y_pred_binary)

        print(name + " Model:")
        confusion_matrix = metrics.confusion_matrix(df_y_test, y_pred_binary)
        print("Confusion Matrix:")
        print(confusion_matrix)

        accuracy = metrics.accuracy_score(df_y_test, y_pred_binary)
        precision = metrics.precision_score(df_y_test, y_pred_binary)
        recall = metrics.recall_score(df_y_test, y_pred_binary)
        classification_report = metrics.classification_report(df_y_test, y_pred_binary)

        print("Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print(classification_report)

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = name
            best_model_instance = model

    print("The best model is:", best_model, "with an accuracy of", best_accuracy)

    # Print the confusion matrix for the best model
    y_pred_best = best_model_instance.predict(df_X_test)
    if best_model in ["Isolation Forest", "One-Class SVM", "K-Means"]:
        y_pred_best = np.where(y_pred_best == -1, 0, y_pred_best)
    print("Confusion Matrix of the best model:")
    print(metrics.confusion_matrix(df_y_test, y_pred_best))
    
    
def find_best_model_regression(df_X_train, df_X_test, df_y_train, df_y_test):
    
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, BayesianRidge, SGDRegressor
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, ExtraTreesRegressor, BaggingRegressor
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.neural_network import MLPRegressor
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor
    from catboost import CatBoostRegressor
    from sklearn import metrics

    models = [
        ("Linear Regression", LinearRegression()),
        ("Ridge Regression", Ridge()),
        ("Lasso Regression", Lasso()),
        ("ElasticNet Regression", ElasticNet()),
        ("Bayesian Ridge Regression", BayesianRidge()),
        ("Decision Tree Regressor", DecisionTreeRegressor()),
        ("Random Forest Regressor", RandomForestRegressor()),
        ("Gradient Boosting Regressor", GradientBoostingRegressor()),
        ("XGBoost Regressor", XGBRegressor(eval_metric="rmse")),
        ("LightGBM Regressor", LGBMRegressor()),
        ("Support Vector Regressor", SVR()),
        ("K-Nearest Neighbors Regressor", KNeighborsRegressor()),
        ("Multi-layer Perceptron Regressor", MLPRegressor(max_iter=1000)),
        ("AdaBoost Regressor", AdaBoostRegressor()),
        ("Extra Trees Regressor", ExtraTreesRegressor()),
        ("Stochastic Gradient Descent Regressor", SGDRegressor()),
        ("Bagging Regressor", BaggingRegressor()),
        ("CatBoost Regressor", CatBoostRegressor(verbose=0, random_seed=42)),
    ]

    best_model = None
    best_mse = float("inf")
    best_model_instance = None

    for name, model in models:
        model.fit(df_X_train, df_y_train)
        y_pred = model.predict(df_X_test)

        print(name + " Model:")
        mse = metrics.mean_squared_error(df_y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = metrics.r2_score(df_y_test, y_pred)

        print("Mean Squared Error:", mse)
        print("Root Mean Squared Error:", rmse)
        print("R-squared:", r2)
        print()

        if mse < best_mse:
            best_mse = mse
            best_model = name
            best_model_instance = model

    print("The best model is:", best_model, "with a Mean Squared Error of", best_mse)

    # Print the metrics for the best model
    y_pred_best = best_model_instance.predict(df_X_test)
    best_rmse = np.sqrt(best_mse)
    best_r2 = metrics.r2_score(df_y_test, y_pred_best)
    print("Metrics of the best model:")
    print("Mean Squared Error:", best_mse)
    print("Root Mean Squared Error:", best_rmse)
    print("R-squared:", best_r2)



def find_best_clustering_algorithm(data, scaling=True, n_clusters=None, visualize=True, test_feature_combinations=False):
    import numpy as np
    import itertools
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans, MiniBatchKMeans, AffinityPropagation, MeanShift, estimate_bandwidth
    from sklearn.cluster import SpectralClustering, AgglomerativeClustering, DBSCAN, OPTICS, Birch
    from sklearn.mixture import GaussianMixture
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score
    import matplotlib.pyplot as plt

    if scaling:
        scaler = StandardScaler()
        data = scaler.fit_transform(data)

    if test_feature_combinations:
        print("\nTesting different feature combinations:")
        for num_features in range(1, data.shape[1] + 1):
            for feature_combination in itertools.combinations(range(data.shape[1]), num_features):
                reduced_data = data[:, feature_combination]
                _, _, score = find_best_clustering_algorithm(reduced_data, scaling=False, n_clusters=n_clusters, visualize=False)
                print(f"Silhouette score for features {feature_combination}: {score}")

    clustering_algorithms = [
        ("KMeans", KMeans(n_clusters=n_clusters) if n_clusters else KMeans()),
        ("MiniBatchKMeans", MiniBatchKMeans(n_clusters=n_clusters) if n_clusters else MiniBatchKMeans()),
        ("AffinityPropagation", AffinityPropagation()),
        ("MeanShift", MeanShift(bandwidth=estimate_bandwidth(data, n_samples=n_clusters)) if n_clusters else MeanShift()),
        ("SpectralClustering", SpectralClustering(n_clusters=n_clusters) if n_clusters else SpectralClustering()),
        ("AgglomerativeClustering", AgglomerativeClustering(n_clusters=n_clusters) if n_clusters else AgglomerativeClustering()),
        ("DBSCAN", DBSCAN()),
        ("OPTICS", OPTICS()),
        ("Birch", Birch(n_clusters=n_clusters) if n_clusters else Birch()),
        ("GaussianMixture", GaussianMixture(n_components=n_clusters) if n_clusters else GaussianMixture())
    ]

    best_algorithm = None
    best_algorithm_name = ""
    best_score = -np.inf

    for name, algorithm in clustering_algorithms:
        try:
            if isinstance(algorithm, GaussianMixture):
                algorithm.fit(data)
                labels = algorithm.predict(data)
            else:
                labels = algorithm.fit_predict(data)

            if len(np.unique(labels)) > 1:
                score = silhouette_score(data, labels)
                print(f"{name} Algorithm:")
                print("Silhouette Score:", score)
                if score > best_score:
                    best_score = score
                    best_algorithm = algorithm
                    best_algorithm_name = name
        except Exception as e:
            print(f"An error occurred while processing {name}: {e}")

    print("The best clustering algorithm is:", best_algorithm_name, "with a silhouette score of", best_score)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(data)

    if isinstance(best_algorithm, GaussianMixture):
        best_algorithm.fit(data)
        cluster_labels = best_algorithm.predict(data)
    else:
        cluster_labels = best_algorithm.fit_predict(data)

    plt.figure(figsize=(10, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, cmap='viridis', edgecolors='k', s=50)
    
    plt.title('Scatter Plot for the Best Clustering Model: ' + best_algorithm_name)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.show()
    return best_algorithm_name, best_algorithm, best_score


def find_best_model_regression_2(X, y, test_size=0.2, random_state=42, cv=5):
    
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, BayesianRidge, SGDRegressor
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, ExtraTreesRegressor, BaggingRegressor
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.neural_network import MLPRegressor
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor
    from catboost import CatBoostRegressor
    from sklearn import metrics
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
    import matplotlib.pyplot as plt

    models = [
        ("Linear Regression", LinearRegression()),
        ("Ridge Regression", Ridge()),
        ("Lasso Regression", Lasso()),
        ("ElasticNet Regression", ElasticNet()),
        ("Bayesian Ridge Regression", BayesianRidge()),
        ("Decision Tree Regressor", DecisionTreeRegressor()),
        ("Random Forest Regressor", RandomForestRegressor()),
        ("Gradient Boosting Regressor", GradientBoostingRegressor()),
        ("XGBoost Regressor", XGBRegressor(eval_metric="rmse")),
        ("LightGBM Regressor", LGBMRegressor()),
        ("Support Vector Regressor", SVR()),
        ("K-Nearest Neighbors Regressor", KNeighborsRegressor()),
        ("Multi-layer Perceptron Regressor", MLPRegressor(max_iter=1000)),
        ("AdaBoost Regressor", AdaBoostRegressor()),
        ("Extra Trees Regressor", ExtraTreesRegressor()),
        ("Stochastic Gradient Descent Regressor", SGDRegressor()),
        ("Bagging Regressor", BaggingRegressor()),
        ("CatBoost Regressor", CatBoostRegressor(verbose=0, random_seed=42)),
    ]

    n_samples = X.shape[0]
    adjusted_test_size = int(test_size * n_samples)

    best_model = None
    best_mse = float("inf")
    best_model_instance = None

    for name, model in models:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=test_size, random_state=random_state)
        model.fit(X_train, y_train)
        
        print(name + " Model:")
        evaluate_model(model, X, y, test_size=adjusted_test_size, random_state=random_state, cv=cv)
        print()

        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        if mse < best_mse:
            best_mse = mse
            best_model = name
            best_model_instance = model

    print("The best model is:", best_model, "with a Mean Squared Error of", best_mse)

    # Print the metrics for the best model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=test_size, random_state=random_state)
    # Fit the best model on the training data
    best_model_instance.fit(X_train, y_train)

    # Predictions
    y_pred_best = best_model_instance.predict(X_test)
    best_rmse = np.sqrt(best_mse)
    best_r2 = r2_score(y_test, y_pred_best)

    print("Metrics of the best model:")
    print("Mean Squared Error:", best_mse)
    print("Root Mean Squared Error:", best_rmse)
    print("R-squared:", best_r2)

    # Learning curve for the best model
    train_sizes, train_scores, val_scores = learning_curve(best_model_instance, X_train, y_train, cv=cv, scoring='neg_mean_squared_error')
    train_scores = np.sqrt(-train_scores).mean(axis=1)
    val_scores = np.sqrt(-val_scores).mean(axis=1)

    plt.plot(train_sizes, train_scores, 'o-', label="Training score")
    plt.plot(train_sizes, val_scores, 'o-', label="Validation score")
    plt.xlabel("Training set size")
    plt.ylabel("RMSE")
    plt.legend()
    plt.show()

    return best_model_instance


def evaluate_model(model, X, y, test_size=0.2, random_state=42, cv=5):
    
    import numpy as np
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split, cross_val_score, learning_curve
    import matplotlib.pyplot as plt
    
    # Train/validation/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=test_size, random_state=random_state)
    
    # Fit the model on the training data
    model.fit(X_train, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    y_test_pred = model.predict(X_test)
    
    # Performance metrics
    mse_train = mean_squared_error(y_train, y_train_pred)
    mse_val = mean_squared_error(y_val, y_val_pred)
    mse_test = mean_squared_error(y_test, y_test_pred)
    
    r2_train = r2_score(y_train, y_train_pred)
    r2_val = r2_score(y_val, y_val_pred)
    r2_test = r2_score(y_test, y_test_pred)
    
    print(f"Mean Squared Error (train/val/test): {mse_train:.4f} / {mse_val:.4f} / {mse_test:.4f}")
    print(f"R-squared (train/val/test): {r2_train:.4f} / {r2_val:.4f} / {r2_test:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='neg_mean_squared_error')
    cv_scores = np.sqrt(-cv_scores)
    print(f"Cross-validation RMSE scores: {cv_scores}")
    print(f"Mean CV RMSE: {np.mean(cv_scores):.4f}, Std. Dev. CV RMSE: {np.std(cv_scores):.4f}")
    
    # Learning curve
    train_sizes, train_scores, val_scores = learning_curve(model, X_train, y_train, cv=cv, scoring='neg_mean_squared_error')
    train_scores = np.sqrt(-train_scores).mean(axis=1)
    val_scores = np.sqrt(-val_scores).mean(axis=1)
    
    plt.plot(train_sizes, train_scores, 'o-', label="Training score")
    plt.plot(train_sizes, val_scores, 'o-', label="Validation score")
    plt.xlabel("Training set size")
    plt.ylabel("RMSE")
    plt.legend()
    plt.show()
    
    return model




def tune_MLPc_parameters(X_train, X_test, y_train, y_test, params_to_try=None, num_combinations=None, random_state=1, optimization_target='accuracy'):
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
    from itertools import product
    import numpy as np

    if params_to_try is None:
        params_to_try = {
            'solver': ['lbfgs', 'adam'],
            'activation': ['relu', 'tanh', 'logistic'],
            'alpha': [0.0001, 0.001, 0.01],
            'learning_rate_init': [0.0001, 0.0005, 0.001],
            'max_iter': [5000, 10000, 15000]
        }

    param_combinations = list(product(*params_to_try.values()))

    if num_combinations is None:
        num_combinations = 10
    elif num_combinations == 'max':
        num_combinations = len(param_combinations)

    best_model = None
    best_params = None
    best_score = -np.inf if optimization_target == 'accuracy' else np.inf

    for i in range(num_combinations):
        chosen_params = dict(zip(params_to_try.keys(), param_combinations[np.random.choice(len(param_combinations))]))

        mlp = MLPClassifier(random_state=random_state, **chosen_params)
        mlp.fit(X_train, y_train)

        y_pred = mlp.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        false_negatives = cm[1][0]
        accuracy = accuracy_score(y_test, y_pred)

        if optimization_target == 'accuracy':
            score = accuracy
            better = score > best_score
        elif optimization_target == 'minimize_false_negatives':
            score = false_negatives
            better = score < best_score
        else:
            raise ValueError("Invalid optimization_target. Choose 'accuracy' or 'minimize_false_negatives'.")

        if better:
            best_model = mlp
            best_params = chosen_params
            best_score = score

    print("Best hyperparameters:")
    print(best_params)
    print(best_model)
    best_model_str = f"MLP = MLPClassifier(activation='{best_params['activation']}', alpha={best_params['alpha']}, " \
                     f"learning_rate_init={best_params['learning_rate_init']}, max_iter={best_params['max_iter']}, " \
                     f"solver='{best_params['solver']}', random_state=1)"
    print(best_model_str)

    y_pred = best_model.predict(X_test)

    print(f"Accuracy for best model: {accuracy_score(y_test, y_pred)}")
    print(f"Confusion matrix for best model:\n{confusion_matrix(y_test, y_pred)}")
    print(f"Precision for best model: {precision_score(y_test, y_pred)}")
    print(f"Recall for best model: {recall_score(y_test, y_pred)}")

    return best_model, best_params







def tune_MLPr_parameters(X_train, X_test, y_train, y_test, params_to_try=None, num_combinations=None, random_state=1):
    from sklearn.neural_network import MLPRegressor
    from sklearn.metrics import mean_squared_error, r2_score
    from itertools import product
    import numpy as np

    if params_to_try is None:
        params_to_try = {
            'solver': ['lbfgs', 'adam'],
            'activation': ['relu', 'tanh', 'logistic'],
            'alpha': [0.0001, 0.001, 0.01],
            'learning_rate_init': [0.0001, 0.0005, 0.001],
            'max_iter': [5000, 10000, 15000]
        }

    param_combinations = list(product(*params_to_try.values()))

    if num_combinations is None:
        num_combinations = 10
    elif num_combinations == 'max':
        num_combinations = len(param_combinations)

    best_model = None
    best_params = None
    best_mse = np.inf

    for i in range(num_combinations):
        chosen_params = dict(zip(params_to_try.keys(), param_combinations[np.random.choice(len(param_combinations))]))

        mlp = MLPRegressor(random_state=random_state, **chosen_params)
        mlp.fit(X_train, y_train)

        y_pred = mlp.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Mean squared error for parameters {chosen_params}: {mse}")

        if mse < best_mse:
            best_model = mlp
            best_params = chosen_params
            best_mse = mse

    print("Best hyperparameters:")
    print(best_params)
    print(best_model)
    best_model_str = f"MLP = MLPRegressor(activation='{best_params['activation']}', alpha={best_params['alpha']}, " \
                     f"learning_rate_init={best_params['learning_rate_init']}, max_iter={best_params['max_iter']}, " \
                     f"solver='{best_params['solver']}', random_state=1)"
    print(best_model_str)

    y_pred = best_model.predict(X_test)
    
    print(f"Mean squared error for best model: {mean_squared_error(y_test, y_pred)}")
    print(f"R2 score for best model: {r2_score(y_test, y_pred)}")
    print(f"RMSE score for best model: {np.sqrt(mean_squared_error(y_test, y_pred))}")

    return best_model, best_params



