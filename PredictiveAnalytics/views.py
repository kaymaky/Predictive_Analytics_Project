from django.shortcuts import render
from PredictiveAnalytics.utils import decode_utf8, get_dates_in_right_format, get_values, model_arima, model_prophet
import csv




#view for start view, render home view
def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})









#all about csv view (1. csv_view: upload; 2.csv_view: select date, value and model; 3. csv_view visualization
def csv_view(request, *args, **kwargs):
    try:

        # second and third csv view, submit button after csv uploaded
        if request.method=='POST':

            #third csv view after selected date_column, value_column and model for forecasting
            if 'submit_setup_csv' in request.POST:
                #get selected data and csv_data from saved session
                selected_date_name = request.POST.get('dropdown_date_csv')
                selected_value_name = request.POST.get('dropdown_value_csv')
                csv_list = request.session['csv_list']
                selected_model = request.POST['dropdown_models']

                #get dates and in right format for forecasting model
                dates = get_dates_in_right_format(csv_list, selected_date_name)
                values = get_values(csv_list, selected_value_name)

                #forecasting
                print("bündan")
                if (selected_model == "arima"):
                    forecastings_dict = model_arima(dates,values)
                if (selected_model == "prophet"):
                    forecastings_dict = model_prophet(dates,values)
                print("degil")
                #init csv view by any mistake
                if not dates or not values:
                    return render(request, 'csv.html', {})
                else:
                    # visualization with forecastings
                    return render(request, 'visualization_csv.html', {'dates' : dates, 'values' : values, 'forecast_dict' : forecastings_dict,  'selected_model' : selected_model})
            else:
                #second view csv
                csv_file = request.FILES["csv_file"]

                #check if csv data is right
                if csv_file.name.endswith('.csv'):
                    csv_file = csv.DictReader(decode_utf8(request.FILES['csv_file']))
                    csv_list = []
                    for row in csv_file:
                        csv_list.append(row)

                    #save csv data in session
                    request.session['csv_list'] = csv_list

                    #render third csv view
                    return render(request, 'visualization_setup_csv.html', {'csv_file': csv_file})

                else:
                    return render(request, 'csv.html', {})
                # return render(request, 'csv.html', {})

            # init csv, first view: /csv/
        else:
            return render(request, 'csv.html', {})

        # by any error init csv view
    except: return render(request, 'csv.html', {})




#ToDo URL-View
# Vissight is URL too --> so many similiar processes
def url_view(request, *args, **kwargs):
    if request.method=='POST':
        print("ToDo")
    return render(request, 'url.html', {})


# Create your views here.


