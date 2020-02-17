# import PredictiveAnalytics.models
import json,urllib.request
import datetime, locale
from statsmodels.tsa.arima_model import ARIMA
import dateutil.parser
import dateutil.relativedelta
from pmdarima.arima import auto_arima
from fbprophet import Prophet
import pandas as pd




# HELP-FUNCTIONS



def decode_utf8(input_iterator):
    for l in input_iterator:
        yield l.decode('utf-8')




# get the values of csv data
def get_values(csv_list, value_name):
    values = []
    for element in csv_list:
        values.append(float(element[value_name]))
    return values





# detects csv date_format with dateutil.parser.parse and transforms in dateformat ("%Y, %m, %d") and returns the dates as list
def get_dates_in_right_format(csv_list, date_name):
    reverse = False;
    try:
        list_of_dates = []
        date1 = dateutil.parser.parse(csv_list[0][date_name])
        date2 = dateutil.parser.parse(csv_list[1][date_name])

        if(date1 > date2):
            reverse = True;

        for elements in csv_list:
            str = elements[date_name]
            date = dateutil.parser.parse(str).strftime("%Y, %m, %d")
            list_of_dates.append(date)
        if(reverse):
            list_of_dates.reverse();

        dict = {
            "list_of_dates": list_of_dates
            }
        return dict
    except:
        print("false")




# returns the date frequence: daily, monthly or yearly
def get_date_freq (dates):
    try:
        freq = 'D'
        date1 = datetime.datetime.strptime(dates['list_of_dates'][0], "%Y, %m, %d")
        date2 = datetime.datetime.strptime(dates['list_of_dates'][1], "%Y, %m, %d")
        date3 = datetime.datetime.strptime(dates['list_of_dates'][2], "%Y, %m, %d")
        delta12 = date2 - date1
        delta23 = date3 - date2
        if (delta12.days > 363 and delta23.days > 363):
            freq = 'Y'
        elif (delta12.days > 28 and delta23.days > 28):
            freq = 'M'
        return freq
    except:
        return




#return difference between two dates, depending on freq: yearly, monthly or daily
def getDiffStart_End_date(freq, date1, date2):
    date_start = datetime.datetime.strptime(date1, "%Y, %m, %d")
    date_end = datetime.datetime.strptime(date2, "%Y, %m, %d")
    if(freq == 'Y'):
        difference_in_years = dateutil.relativedelta.relativedelta(date_end, date_start).years
        print(difference_in_years)
        return difference_in_years
    elif(freq == 'M'):
        dif= dateutil.relativedelta.relativedelta(date_end, date_start)
        difference_in_months = (dif.years * 12) + dif.months
        return difference_in_months

    else:
        delta_dif = date_end - date_start
        return delta_dif.days





# FORECASTING-MODELS


def model_arima(dates, values):

    #try auto_arima else with given parameters
    try:
        train_percentage_of_data = 0.90
        X = values
        Y = dates
        size = int(len(X) * train_percentage_of_data)
        train, test = X[0:size], X[size:len(X)]
        result_ARIMA = []
        history = [x for x in train]
        result_ARIMA_dates = Y['list_of_dates'][size:len(Y['list_of_dates'])]
        result_predictions = []

        auto_model = auto_arima(train)

        p = auto_model.order[0]
        d = auto_model.order[1]
        q = auto_model.order[2]

        # p = 2
        # d = 1
        # q = 0

        for t in range(len(test)+20):

            model = ARIMA(history, order=(p, d, q))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            predictionValue = output[0]
            history.append(predictionValue)
            if (t >= len(test)):
                result_predictions.append(float("{0:.2f}".format(predictionValue[0])))
            else:
                obs = test[t]
                result_ARIMA.append(float("{0:.2f}".format(predictionValue[0])))

            dict = {
                'list_of_results_model_dates' : result_ARIMA_dates,
                'list_of_results_predictions' : result_predictions,
                'list_of_resutls_model' : result_ARIMA
            }
        return dict

    except:
        train_percentage_of_data = 0.90     #10% Train
        X = values
        Y = dates
        size = int(len(X) * train_percentage_of_data)
        train, test = X[0:size], X[size:len(X)]
        result_ARIMA = []
        history = [x for x in train]
        result_ARIMA_dates = Y['list_of_dates'][size:len(Y['list_of_dates'])]

        result_predictions = []


        p = 2
        d = 1
        q = 0

        for t in range(len(test) + 20):

            model = ARIMA(history, order=(p, d, q))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            predictionValue = output[0]
            history.append(predictionValue)
            if (t >= len(test)):
                result_predictions.append(float("{0:.2f}".format(predictionValue[0])))
            else:
                obs = test[t]
                result_ARIMA.append(float("{0:.2f}".format(predictionValue[0])))

            dict = {
                'list_of_results_model_dates': result_ARIMA_dates,
                'list_of_results_predictions': result_predictions,
                'list_of_resutls_model': result_ARIMA
            }
        return dict





def model_prophet(dates, values):
    train_percentage_of_data = 0.90  #10% Test
    freq = get_date_freq(dates)
    X = values
    Y = dates
    size = int(len(X) * train_percentage_of_data)
    print(len(X) * train_percentage_of_data)
    train_value, test_value = X[0:size], X[size:len(X)]
    train_date, test_date = Y['list_of_dates'][0:size], Y['list_of_dates'][size:len(X)]
    len_test = getDiffStart_End_date(freq, dates['list_of_dates'][size], dates['list_of_dates'][-1])
    # len_test = len(test_value)
    result_PROPHET = []
    predictions = list()
    result_PROPHET_dates = Y['list_of_dates'][size:len(X)]
    result_predictions = []


    model = Prophet()
    dict = {'ds': train_date, 'y': train_value}
    df = pd.DataFrame(dict)
    model.fit(df)
    future = model.make_future_dataframe(periods=len_test + 20, freq=freq)
    forecast_frame = model.predict(future)
    forecast_frame['ds'] = forecast_frame['ds'].apply(str)
    forecast_frame_date= pd.DataFrame(forecast_frame, columns= ['ds'])
    forecast_frame_value = pd.DataFrame(forecast_frame, columns=['yhat'])
    forecast_frame_date.apply(str)
    forecast_frame_value.apply(str)
    forecast_list_dates = forecast_frame_date.values.tolist()
    forecast_list_values = forecast_frame_value.values.tolist()
    forecast_list_dates_right_format = []
    forecast_list_values_right_format = []

    for date_wrong_format in forecast_list_dates:
        date = dateutil.parser.parse(date_wrong_format[0]).strftime("%Y, %m, %d")
        forecast_list_dates_right_format.append(date)
    for value_wrong_format in forecast_list_values:
        value = float("{0:.2f}".format(value_wrong_format[0]))
        forecast_list_values_right_format.append(value)

# ToDo: check correct size or 1-2 elements lost
    print(train_value[size-1])
    print(test_value[0])
    print(train_date[size-1])
    print(test_date[0])
    print(forecast_list_dates_right_format[0])
    print(forecast_list_dates_right_format[len_test + size])
    result_PROPHET_dates = forecast_list_dates_right_format[size:-20]
    result_predictions = forecast_list_values_right_format [len_test+size:-1]
    print(result_PROPHET_dates)

    result_PROPHET = forecast_list_values_right_format[size:-20]


    dict = {
        'list_of_results_model_dates': result_PROPHET_dates,
        'list_of_results_predictions': result_predictions,
        'list_of_resutls_model': result_PROPHET
    }
    return dict

    
