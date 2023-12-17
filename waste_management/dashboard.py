from dateutil.relativedelta import relativedelta
from datetime import datetime

from .models import HSEAccidentReport #, WasteBatchAcceptanceAtOrigin, WasteBatchAcceptanceAtDestination, WasteBatchStorageEnter
#from .models import WasteBatchStorageExit, WasteBatchTreatment, WasteBatchLandfilling, Contract, Payment

from django.db.models import Count #, Sum
import plotly.graph_objects as go
from django.shortcuts import render
#from django.db.models.functions import Coalesce
#from django.db.models import Q
# from django.http import HttpResponse
import json
import plotly
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& HSE dashboard &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

# Quary database

def get_combined_accident_data(start_date, end_date, interval):
    if interval == 'days':
        delta = relativedelta(days=1)
    elif interval == 'weeks':
        delta = relativedelta(weeks=1)
    elif interval == 'months':
        delta = relativedelta(months=1)
    else:
        raise ValueError(f"Unsupported interval: {interval}")

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    current_date = start_date
    data_array = []
    all_accident_count = 0

    while current_date <= end_date:
        next_date = current_date + delta
        interval_data = {'date': current_date.strftime('%Y-%m-%d')}

        for severity in range(1, 6):
            accident_count = HSEAccidentReport.objects.filter(
                date__gte=current_date,
                date__lt=next_date,
                severity=severity
            ).count()
            interval_data[f'severity_{severity}_count'] = accident_count

        all_accident_count += HSEAccidentReport.objects.filter(
            date__gte=current_date,
            date__lt=next_date
        ).count()

        data_array.append(interval_data)

        current_date = next_date

    total_accidents_by_type = HSEAccidentReport.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).values('type').annotate(total_accidents=Count('id_code'))

    return data_array, all_accident_count, list(total_accidents_by_type)


# Plot Charts

def accident_report_data_stacked_bar_chart(data_array, x_axis_title, y_axis_title, legend_titles):
    dates = [entry['date'] for entry in data_array]
    values_severity_1 = [entry['severity_1_count'] for entry in data_array]
    values_severity_2 = [entry['severity_2_count'] for entry in data_array]
    values_severity_3 = [entry['severity_3_count'] for entry in data_array]
    values_severity_4 = [entry['severity_4_count'] for entry in data_array]
    values_severity_5 = [entry['severity_5_count'] for entry in data_array]

    fig = go.Figure()

    fig.add_trace(go.Bar(x=dates, y=values_severity_1, name=legend_titles[0]))
    fig.add_trace(go.Bar(x=dates, y=values_severity_2, name=legend_titles[1]))
    fig.add_trace(go.Bar(x=dates, y=values_severity_3, name=legend_titles[2]))
    fig.add_trace(go.Bar(x=dates, y=values_severity_4, name=legend_titles[3]))
    fig.add_trace(go.Bar(x=dates, y=values_severity_5, name=legend_titles[4]))

    fig.update_layout(
        barmode='stack',                 # Stacking the bars
        xaxis=dict(title=x_axis_title),  # Set x-axis title
        yaxis=dict(title=y_axis_title),  # Set y-axis title
        showlegend=True,                 # Show legend
        legend=dict(title="Legend")      # Set legend title
    )

    return fig

# Sample function call: png_image = accident_report_data_stacked_bar_chart(data_array, x_axis_title, y_axis_title, legend_titles)

def total_accidents_by_type_pie_chart(variable_names, variable_values):
    # Creating a pie chart using Plotly with percentages and a legend
    fig = go.Figure(data=[go.Pie(labels=variable_names,
                                  values=variable_values,
                                  textinfo='percent',
                                  showlegend=True)])

    # Customize the layout
    fig.update_layout(title="Pie Chart")

    # Return the pie chart as a PNG image without writing it to storage
    return fig

# Views



def accident_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        interval = request.POST.get('interval')

        data_array, all_accident_count, total_accidents_by_type = get_combined_accident_data(
            start_date, end_date, interval
        )

        # Generate the stacked bar chart
        stacked_bar_chart_fig = accident_report_data_stacked_bar_chart(
            data_array, 'Date', 'Count', ['Severity 1', 'Severity 2', 'Severity 3', 'Severity 4', 'Severity 5']
        )
        stacked_bar_chart_json = json.dumps(stacked_bar_chart_fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Generate the pie chart
        pie_chart_fig = total_accidents_by_type_pie_chart(
            [entry['accident_type'] for entry in total_accidents_by_type],  # Assuming 'accident_type' is the correct key
            [entry['total_accidents'] for entry in total_accidents_by_type]
        )
        pie_chart_json = json.dumps(pie_chart_fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render(request, 'accident_report.html', {
            'data_array': data_array,
            'all_accident_count': all_accident_count,
            'stacked_bar_chart_json': stacked_bar_chart_json,
            'pie_chart_json': pie_chart_json,
        })

    return render(request, 'accident_report.html')
