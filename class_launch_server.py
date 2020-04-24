import pandas as pd; import numpy as np; import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvas
import panel as pn
import panel.widgets as pnw
import param

#window_slide  = pnw.IntSlider(name='window', value=10, start=1, end=60)
#sigma_slide  = pnw.IntSlider(name='sigma', value=10, start=1, end=20)
pn.extension()

def mpl_plot(avg, highlight):
        fig = Figure()
        FigureCanvas(fig) # not needed in mpl >= 3.1
        ax = fig.add_subplot()
        avg.plot(ax=ax)
        if len(highlight): 
            highlight.plot(style='o', ax=ax)
            return fig

#def hvplot(avg, highlight):
#        #line = avg.hvplot(height=300, width=500)
#        #outliers = highlight.hvplot.scatter(color='orange', padding=0.1)
#        #tap.source = line
#        #return (line * outliers).opts(legend_position='top_right')
#        return avg.hvplot(height=200) * highlight.hvplot.scatter(color='orange', padding=0.1)

def find_outliers(variable='Temperature', window=20, sigma=10, view_fn=mpl_plot):
        avg = data[variable].rolling(window=window).mean()
        residual = data[variable] - avg
        std = residual.rolling(window=window).std()
        outliers = (np.abs(residual) > std * sigma)
        return view_fn(avg, avg[outliers])


data = pd.read_csv('./datatest.csv')
data['date'] = data.date.astype('datetime64[ns]')
data = data.set_index('date')

#### Assembly of stuff
#variable  = pnw.RadioButtonGroup(name='variable', value='Temperature', 
#                                         options=list(data.columns))
#window  = pnw.IntSlider(name='window', value=10, start=1, end=60)
#sigma  = pnw.IntSlider(name='sigma', value=10, start=1, end=20)
#
#@pn.depends(variable, window, sigma)
#def reactive_outliers(variable, window, sigma):
#    return find_outliers(variable, window, sigma)
#
#widgets   = pn.Column("<br>\n# Room occupancy", variable, window, sigma)
#occupancy = pn.Row(reactive_outliers, widgets)
#occupancy.servable()
#### End of assembly stuff

### Via objects
class RoomOccupancy(param.Parameterized):
        data = pd.read_csv('./datatest.csv')
        data['date'] = data.date.astype('datetime64[ns]')
        data = data.set_index('date')
        variable  = param.Selector(objects=list(data.columns))
        window    = param.Integer(default=10, bounds=(1, 20))
        sigma     = param.Number(default=10, bounds=(0, 20))

        def view(self):
            return find_outliers(self.variable, self.window, self.sigma)
                                
obj = RoomOccupancy()
testobj = pn.Row(obj.param, obj.view)
testobj.servable()
#### End of via objects

#
#variable  = pnw.RadioButtonGroup(name='variable', value='Temperature', 
#                                         options=list(data.columns))
#window  = pnw.IntSlider(name='window', value=10, start=1, end=60)
#
#@pn.depends(variable, window)
#def reactive_outliers(variable, window):
#    return find_outliers(variable, window, 10)
#
#widgets   = pn.Column("<br>\n# Room occupancy", variable, window)
#occupancy = pn.Row(reactive_outliers, widgets)
#occupancy.servable()

#
##kw = dict(window=(1, 60), variable=sorted(list(data.columns)), sigma=(1, 20))
##@pn.depends(window, sigma)
##def reactive_outliers(window):
##        return find_outliers('Temperature', window, 10)
##
##widgets   = pn.Column("<br>\n# Room occupancy", window, sigma)
##rows   = pn.Row(reactive_outliers, widgets)
##rows   = pn.Row(find_outliers('Temperature',window,sigma), widgets)
#
#widgets   = pn.Column("<br>\n# Room occupancy", window_slide, sigma_slide)
#rows   = pn.Row(find_outliers,widgets)
#rows.servable()

#pn.extension()


#pn.show(threaded=True)

