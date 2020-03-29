from django.shortcuts import render
from .plot import line, map_plot
# Create your views here.


def index(request):
    """"""
    map_plt = map_plot()
    line_plot, _ = line()

    return render(request, 'tracker/index.html', {'line_plot': line_plot, 'map_plot': map_plt})
