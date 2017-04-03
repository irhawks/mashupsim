# coding:utf-8
from bokeh.charts import TimeSeries, show, output_file

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib


import json

from itertools import cycle

## 在这里设置好字体等因素
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Adobe Heiti Std'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
mpl.rcParams['savefig.dpi'] = 300

class Visualizer :

    def __init__(self, pandas=[]) :

        self.pandas = pandas

    def scale_axis(self, tuple_range, scale) :
        middle = (tuple_range[0] + tuple_range[1]) / 2.0
        return (middle + scale* (i - middle) for i in tuple_range)

    def data_middle(self, tuple_range, *args, **kwargs) :
        a = max(tuple_range)
        return (-0.1*a, 1.2*a)

    def show_3_variables(self, var_list) : 

        #self.pandas.plot(x=self.pandas.time); 
        """
        依次是红绿蓝的样式，使用各自的配色。其中第三个主要是参考线
        观察前两个随着时间的变化的关系。
        """

        slices = self.pandas[var_list]

        fig, ax1 = plt.subplots()
        ax2, ax3 = ax1.twinx(), ax1.twinx()

        ax1.set_xlabel("simulation time")
        ax1.set_ylabel(var_list[0])
        ax2.set_ylabel(var_list[1])
        ax3.set_ylabel(var_list[2])

        rspine = ax3.spines['right']
        rspine.set_position(('axes', 1.20))
        ax3.set_frame_on(True)
        ax3.patch.set_visible(False)

        fig.subplots_adjust(right=0.75)

        ## 注意在画legend的时候的特殊技巧
        styles = ['r-', 'g-', 'b--']
        ax1.plot(slices[var_list[0]], styles[0],label=var_list[0])
        ax1.plot(0,0, styles[1],label=var_list[1])
        ax1.plot(0,0, styles[2],label=var_list[2])

        ## 注意坐标轴$(min,max)$的放缩变换是$(min+max)/2 + k*(x - (min+max)/2)
        print(ax2.get_ylim())
        ax2.plot(slices[var_list[1]], styles[1],label=var_list[1])
        ax2.set_ylim( self.scale_axis(ax2.get_ylim(),1.2) )
        ax3.plot(slices[var_list[2]], styles[2],label=var_list[2])
        ax3.set_ylim( self.scale_axis(ax3.get_ylim(),1.4) )
        #slices[var_list[1]].plot(ax=ax2, style='r-',label=var_list[0], secondary_y=True)
        #slices[var_list[2]].plot(ax=ax3, style='g-',label=var_list[0])

        ax1.legend(loc='upper left') ## lower/upper/center left/right
        #plt.legend(loc='best')
        plt.show()

    # d = Pandas Dataframe, 
    # ys = [ [cols in the same y], [cols in the same y], [cols in the same y], .. ] 
    # any different y axis <http://stackoverflow.com/questions/7733693/matplotlib-overlay-plots-with-different-scales>
    def show_n_vars_on_right(self, var_list_group
            , line_styles = cycle(['-','-','-', '-.', '-.', ':', '.', ',', 'o', 'v', '^', '<', '>',
                   '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_'])
            , markers = cycle(['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_'])
            ) :

        d = self.pandas
        ys = var_list_group
        #from itertools import cycle
        fig, ax = plt.subplots()

        axes = [ax]
        for y in ys[1:]:
            # Twin the x-axis twice to make independent y-axes.
            axes.append(ax.twinx())

        extra_ys =  len(axes[2:])

        # Make some space on the right side for the extra y-axes.
        if extra_ys>0:
            temp = 0.85
            if extra_ys<=2:
                temp = 0.75
            elif extra_ys<=4:
                temp = 0.6
            if extra_ys>5:
                raise Exception('you are being ridiculous, too more axes')
            fig.subplots_adjust(right=temp)
            right_additive = (0.98-temp)/float(extra_ys)
        # Move the last y-axis spine over to the right by x% of the width of the axes
        i = 1.
        for ax in axes[2:]:
            ax.spines['right'].set_position(('axes', 1.+right_additive*i))
            ax.set_frame_on(True)
            ax.patch.set_visible(False)
            ax.yaxis.set_major_formatter(matplotlib.ticker.OldScalarFormatter())
            i +=1.
        # To make the border of the right-most axis visible, we need to turn the frame
        # on. This hides the other plots, however, so we need to turn its fill off.

        cols = []
        lines = []
        #line_styles = cycle(['-','-','-', '-.', '-.', ':', '.', ',', 'o', 'v', '^', '<', '>',
        #           '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_'])
        #markers = cycle(['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_'])
        colors = cycle(matplotlib.rcParams['axes.color_cycle'])
        for ax,y in zip(axes,ys):
            ls=next(line_styles)
            ms=next(markers)
            if len(y)==1:
                col = y[0]
                cols.append(col)
                color = next(colors)
                lines.append(ax.plot(d[col],linestyle =ls, marker=ms, label = col,color=color))
                ax.set_ylabel(col,color=color)
                #ax.tick_params(axis='y', colors=color)
                ax.spines['right'].set_color(color)
                ax.set_ylim( self.data_middle(ax.get_ylim(), 1.2+0.5*np.random.random()) )
            else:
                for col in y:
                    color = next(colors)
                    lines.append(ax.plot(d[col],linestyle =ls,marker=ms, label = col,color=color))
                    cols.append(col)
                ax.set_ylabel(', '.join(y))
                ax.set_ylim( self.data_middle(ax.get_ylim(), 1.2+0.5*np.random.random()) )
                #ax.tick_params(axis='y')
        axes[0].set_xlabel(d.index.name)
        lns = lines[0]
        for l in lines[1:]:
            lns +=l
        labs = [l.get_label() for l in lns]
        axes[0].legend(lns, labs, loc="upper left")

        #axes[0].set_xlabel("simulation time")
        #for i in range(0,len(ys[0])) : 
        axes[0].set_xlabel("simulation time")
        plt.show()
    

    def show_n_var_on_left (self, var_list) :
        # Twin the x-axis twice to make independent y-axes.
        axes = [ax, ax.twinx(), ax.twinx()]
        
        # Make some space on the right side for the extra y-axis.
        fig.subplots_adjust(right=0.75)
        
        # Move the last y-axis spine over to the right by 20% of the width of the axes
        axes[1].spines['right'].set_position(('axes', -0.25))
        axes[2].spines['right'].set_position(('axes', -0.5))
        
        # To make the border of the right-most axis visible, we need to turn the frame
        # on. This hides the other plots, however, so we need to turn its fill off.
        axes[-1].set_frame_on(True)
        axes[-1].patch.set_visible(False)
        
        # And finally we get to plot things...
        colors = ('Green', 'Red', 'Blue')
        intAxNo = 0
        for ax, color in zip(axes, colors):
            intAxNo += 1
            data = np.random.random(1) * np.random.random(10)
            ax.plot(data, marker='o', linestyle='none', color=color)
            if (intAxNo > 1):
                if (intAxNo == 2):
                    ax.set_ylabel('%s Thing' % color, color=color, labelpad = -40 )
                elif (intAxNo == 3):
                    ax.set_ylabel('%s Thing' % color, color=color, labelpad = -45 )
                ax.get_yaxis().set_tick_params(direction='out')
            else:
                ax.set_ylabel('%s Thing' % color, color=color, labelpad = +0 )
        
            ax.tick_params(axis='y', colors=color)
        axes[0].set_xlabel('X-axis')
        
        
        plt.show()


    def bokeh_show(self) :

        df= pd.DataFrame(self.pandas)
        df.consumer_payments = df.consumer_payments.cumsum()
        df.cost_for_consumer = df.cost_for_consumer.cumsum()
        df.plot(x=df.start_time); 
        #df.to_csv(open("data.csv", 'w'))
        obvalues = pd.DataFrame(dict(r_q=df['r_q'],pay=df['consumer_payments'],sf_q=df['sf_q']))
        #p = TimeSeries(obvalues, legend=True, title="Stocks", ylabel='Stock Prices') 
        show(p)


    def merged_show(self) :

        a = []

        df= pd.DataFrame(self.pandas)
        df.benefit= df.benefit.cumsum()
        df.cost_for_customer = df.cost_for_customer.cumsum()
        a.append(df.benefit)
        #df = pd.DataFrame(a)
        #print(a)
        df = pd.concat(a, axis=1)
        #print(df)
        df.plot()
        plt.legend(loc='best')
        plt.show()
