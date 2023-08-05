"""
RSA 17/03/23
This helper function makes it easier to plot for demonstrations and examples, paritclarly on the colab page


"""
from leuci_xyz import spacetransform as space
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib

#####################################################################
class MapPlotHelp(object):
    def __init__(self,filename):
        # PUBLIC INTERFACE        
        self.filename = filename                
        self.plots_2d = []
        self.plots_3d = []                
    
    def add_plot_slice_2d(self,vals,tag):
        self.plots_2d.append((vals,tag))
    
    def add_plot_slice_3d(self,vals,tag):
        self.plots_3d.append((vals,tag))
                    
    def make_plot_slice_3d(self,vals,min_percent=1, max_percent=1,hue="GBR",centre=True,title="Leucippus Plot 3d"):
        #https://plotly.com/python/3d-isosurface-plots/
        #turn data into scatter for iso_surface
        xs = []
        ys = []
        zs = []
        values = []

        #fig = make_subplots(rows=1, cols=1,subplot_titles=[title],horizontal_spacing=0.05,vertical_spacing=0.05)
        
        minv = 1000
        maxv = -1000

        a,b,c = vals.shape()
        for i in range(a):
            for j in range(b):
                for k in range(a):
                    val = 0
                    if k < c:
                        val = vals.get(i,j,k)
                        minv = min(minv,val)
                        maxv = max(maxv,val)
                    xs.append(i)
                    ys.append(j)
                    zs.append(k)
                    values.append(val)

                            
        
        if minv == maxv or minv >- 0:
            d0 = 0.5
        else:
            d0 = (0 - minv) / (maxv - minv)
        
        d1 = (1-d0)/3
        d2 = 2*(1-d0)/3
        #colorscale=[(0, "grey"), (d0, "snow"), (d0+0.2, "cornflowerblue"),(0.9, "crimson"),(1.0, "rgb(100,0,0)")],
        c0 = "rgba(119,136,153,1)"
        c1 = "rgba(240,248,255,0)"
        c2 = "rgba(100,149,237,0.5)"
        c3 = "rgba(220,20,60,0.9)"
        c4 = "rgba(100,0,0,1)"


        colorscale=[
            (0, c0),
            (d0, c1),
            (d0+0.2, c2),
            (0.9, c3),
            (1, c4)]

        fig= go.Figure(data=go.Isosurface(
        x=xs,
        y=ys,
        z=zs,
        value=values,        
        colorscale=colorscale,
        showscale=True,
        showlegend=False,        
        opacity=0.6,
        surface_count=20,
        caps=dict(x_show=False, y_show=False),
        isomin=minv * min_percent,
        isomax=maxv * max_percent,
        ))
        
        fig.update_xaxes(showticklabels=False,visible=False) # hide all the xticks
        fig.update_yaxes(showticklabels=False,visible=False) # hide all the xticks
        fig.update_yaxes(scaleanchor="x",scaleratio=1)    
        fig.update_xaxes(scaleanchor="y",scaleratio=1)

        fig.update_layout(title=dict(text=title))

                        
        #print(values)
        if self.filename == "SHOW":
            fig.show()
        elif ".html" in self.filename:
            fig.write_html(self.filename)
        else:
            fig.write_image(self.filename,width=2000,height=2000)

    def make_plot_slice_2d(self,vals,min_percent=1, max_percent=1,hue="GBR",centre=True,title="Leucippus Plot 2d"):
        #https://plotly.com/python/3d-isosurface-plots/
        #turn data into scatter for iso_surface        
        minv = 1000
        maxv = -1000

        fig = make_subplots(rows=1, cols=1,subplot_titles=[title],horizontal_spacing=0.05,vertical_spacing=0.05)

        mind,maxd = 1000,-1000    
        for i in range(len(vals)):
            for j in range(len(vals[0])):        
                mind = min(vals[i][j],mind)
                maxd = max(vals[i][j],maxd)
        if maxd == mind:
            d0 = 0.5
        else:
            d0 = (0 - mind) / (maxd - mind)            
        absmin = mind*min_percent
        absmax = maxd*max_percent   

        data_vals = go.Contour(z=vals,showscale=False, 
                                colorscale=[(0, "grey"), (d0, "snow"), (d0+0.2, "cornflowerblue"),(0.9, "crimson"),(1.0, "rgb(100,0,0)")],
                                contours=dict(start=absmin,end=absmax,size=(absmax-absmin)/20),
                                line=dict(width=0.5,color="gray"),
                                zmin=absmin,zmax=absmax) 
        
        fig.add_trace(data_vals,row=1,col=1)    
        fig.update_xaxes(showticklabels=False,visible=False) # hide all the xticks
        fig.update_yaxes(showticklabels=False,visible=False) # hide all the xticks
        fig.update_yaxes(scaleanchor="x",scaleratio=1)    
        fig.update_xaxes(scaleanchor="y",scaleratio=1)
                        
        #print(values)
        if self.filename == "SHOW":
            fig.show()
        elif ".html" in self.filename:
            fig.write_html(self.filename)
        else:
            fig.write_image(self.filename,width=2000,height=2000)


                    