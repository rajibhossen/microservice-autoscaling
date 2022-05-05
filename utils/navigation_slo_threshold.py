import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from utils.db_utils import QValueDB

"""
ranges are 0-100, 100-300, 300-600, 600-900, 900-1200
1. Collect some response time for different RPS for a fixed configuration and a fixed range. e.g. 300, 280, 150, 120, 200, 220
2. Make a line equation / linear regression based on RPS and Response Time
3. Find response time for minimum difference of a range. e.g. find response time for 200 difference of 100-300 rps
    3a. find response time for max rps of the range e.g. 300
    3b. find response time for min rps of that range. e.g. 100
4. We assumed P is the threshold to stop iterating at maximum RPS. P = 5%, for maximum rps of any range
5. we need to calculate Q. Q = P x SLO - (3a - 3b)
6. to find percentage for Q, (Q * 100) / SLO
7. store Q value for range and slo
8. calculate y using the Q value
"""


def save_q_value(slo, range_id, q_value, q_value_db):
    q_value_db.save_q_value(slo, range_id, q_value)


def get_q_value(slo, range_id, q_value_db):
    data = q_value_db.get_q_value(slo, range_id)
    print("Q Table for this configs: ", len(data))
    if len(data) >= 1:
        return data[0][2]
    else:
        return -1


def build_linear_regression(slo, range_id, data, ranges):
    request_per_secs = []
    response = []
    print("**********BEGIN REGRESSION***********")
    for row in data:
        request_per_secs.append(row[5])
        response.append(row[7])

    print(request_per_secs)
    print(response)
    request_per_secs = np.array(request_per_secs)
    request_per_secs = request_per_secs.reshape(-1, 1)
    response = np.array(response)
    response = response.reshape(-1, 1)
    regression_model = LinearRegression()
    regression_model.fit(request_per_secs, response)
    print("Coefficients: ", regression_model.coef_)
    print("Intercepts: ", regression_model.intercept_)
    # print("Params: ", regression_model.get_params())
    print("Score: ", regression_model.score(request_per_secs, response))
    # print(response)

    range_min_y = regression_model.predict(np.array(ranges["min"]).reshape(1, -1))
    range_max_y = regression_model.predict(np.array(ranges["max"]).reshape(1, -1))
    print(range_min_y, range_max_y)
    filename = str(slo) + "_" +str(range_id) + "_sock_shop_regression.model"
    # pickle.dump(regression_model, open(filename), 'wb')
    print("*********END REGRESSION***********")
    return [range_min_y, range_max_y]


def get_stopping_threshold(slo, range_id, range, history, P_value):
    q_value_db = QValueDB()
    q_value = get_q_value(slo, range_id, q_value_db)
    if q_value == -1:
        responses = history.select_response_regression(slo, range_id)
        print("Length of responses from db: ", len(responses))
        if len(responses) >= 10:
            range_values = build_linear_regression(slo, range_id, responses, range)
            Q_value = P_value * slo - (range_values[1][0][0] - range_values[0][0][0])
            # print("Q value is: ", Q_value)
            save_q_value(slo, range_id, Q_value, q_value_db)
            return Q_value
        else:
            return -1
    else:
        return q_value
