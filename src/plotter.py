import plotly.graph_objects as go
import streamlit as st
from src.colors import qualitive_color_dict

def demanded_plot(data, t_demanded, speed_round):

    test_plot = go.Figure()
    test_plot.add_trace	(go.Scattergl (  
                                x       		= data[speed_round],
                                y       		= data[t_demanded],
                                name 			= t_demanded + " : " + speed_round,
                                mode            = 'markers',

                                        )
                        )
    test_plot.update_layout    (   
                                title       = 'Demanded Test Points',
                                xaxis_title = speed_round,
                                yaxis_title = t_demanded
                                )
    return test_plot

def transient_removal_plot(transient_sample, Step_index, Stop_index, df, test_dict, t_demanded, t_estimated, t_measured):
    transient_plot = go.Figure()

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample[t_demanded], 
                                        name    = t_demanded,
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )
    if t_estimated != None:
        transient_plot.add_trace(go.Scatter (  
                                            x       = transient_sample.index.values, 
                                            y       = transient_sample[t_estimated],
                                            name    = t_estimated,
                                            hovertemplate = '%{y:.2f} Nm'
                                )           )

    transient_plot.add_trace(go.Scatter (  
                                        x       = transient_sample.index.values, 
                                        y       = transient_sample[t_measured], 
                                        name    = t_measured,
                                        hovertemplate = '%{y:.2f} Nm'
                            )           )

    transient_plot.update_layout    (   
                                    title       = 'Transient Removal Example',
                                    xaxis_title = 'Sample [N]',
                                    yaxis_title = 'Torque [Nm]'
                                    )
    transient_plot.add_annotation   (
                                    x           = Step_index[test_dict["Sample"]],
                                    y           = df[t_demanded][Step_index[test_dict["Sample"]]],
                                    xref        = "x",
                                    yref        = "y",
                                    text        = "Start of removal",
                                    showarrow   = True,
                                    font        = dict   (
                                                        family  = "Arial, monospace",
                                                        size    = 14,
                                                        color   = "#ffffff"
                                                        ),
                                    align       = "center",
                                    arrowhead   = 2,
                                    arrowsize   = 1,
                                    arrowwidth  = 2,
                                    arrowcolor  = "#636363",
                                    bordercolor = "#c7c7c7",
                                    borderwidth = 2,
                                    borderpad   = 4,
                                    bgcolor     = "#ff7f0e",
                                    )

    transient_plot.add_annotation   (
                                    x           = Stop_index[test_dict["Sample"]],
                                    y           = df[t_demanded][Stop_index[test_dict["Sample"]]],
                                    xref        = "x",
                                    yref        = "y",
                                    text        = "End of removal",
                                    showarrow   = True,
                                    font        = dict   (
                                                        family  = "Arial, monospace",
                                                        size    = 14,
                                                        color   = "#ffffff"
                                                        ),
                                    align       = "center",
                                    arrowhead   = 2,
                                    arrowsize   = 1,
                                    arrowwidth  = 2,
                                    arrowcolor  = "#636363",
                                    bordercolor = "#c7c7c7",
                                    borderwidth = 2,
                                    borderpad   = 4,
                                    bgcolor     = "#ff7f0e",
                                    )

    transient_plot.update_layout    (
                                    hovermode="x unified",
                                    
                                    )
    return transient_plot

@st.cache
def plot_3D(df, x_string, y_string, z_string, x, y, z, chart_type, color_palette, overlay, overlay_alpha, overlay_color):
    with st.spinner("Generating 3D Plot"):
        label_dict = dict()
        trace_dict = dict()

        plot_3D = go.Figure()

        if chart_type == 'Contour':
            plot_3D.add_trace(go.Contour    (
                                            z           = z,
                                            x           = x, 
                                            y           = y,
                                            #colorscale  = color_palette,
                                            hovertemplate = x_string + ': %{x:.2f}' + 
                                                            '<br>' + y_string + ': %{y:.2f}</br>' +
                                                            z_string + ': %{z:.2f}',

                                            contours    = dict  (
                                                                coloring    ='heatmap',
                                                                showlabels  = True,
                                                                labelfont   = dict  (
                                                                                    size = 10,
                                                                                    color = 'white',
                                                                                    )
                                                                ), 

                                            colorbar    = dict  (
                                                                title       = z_string,
                                                                titleside   = 'right',
                                                                titlefont   = dict  (
                                                                                    size=12,
                                                                                    family='Arial, sans'
                                                                                    )
                                                                
                                                                )
                                            
                                            
                                    )       )
            label_dict["title"]         = z_string
            label_dict["xaxis"]         = dict(title=x_string)
            label_dict["yaxis"]         = dict(title=y_string)
            trace_dict["zmid"]          = 0
            trace_dict["colorscale"]    = color_palette

        if chart_type == 'Surface':
            plot_3D.add_trace(go.Surface  (
                                z           = z,
                                x           = x, 
                                y           = y,

                                contours =  {
                                            "x": {"show": True},
                                            "z": {"show": True}
                                            },

                                colorscale  = color_palette,
                         
                
                                hovertemplate = x_string + ': %{x:.2f}' + 
                                                '<br>' + y_string + ': %{y:.2f}</br>' +
                                                z_string + ': %{z:.2f}',

                                colorbar    = dict  (
                                                    title       = z_string,
                                                    titleside   = 'right',
                                                    titlefont   = dict  (
                                                                        size=12,
                                                                        family='Arial, sans'
                                                                        ),
                                                                        
                                                    )
                                )           )
            label_dict["title"]         = z_string
            label_dict["xaxis"]         = dict(title=x_string)
            label_dict["yaxis"]         = dict(title=y_string)
            trace_dict["cmid"]          = 0
            trace_dict["colorscale"]    = color_palette

        if chart_type == 'Heatmap':
            plot_3D.add_trace(go.Heatmap  (
                                z           = z,
                                x           = x, 
                                y           = y,

                                colorscale  = color_palette,

                                hovertemplate = x_string + ': %{x:.2f}' + 
                                                '<br>' + y_string + ': %{y:.2f}</br>' +
                                                z_string + ': %{z:.2f}',

                                colorbar    = dict  (
                                                    title       = z_string,
                                                    titleside   = 'right',
                                                    titlefont   = dict  (
                                                                        size=12,
                                                                        family='Arial, sans'
                                                                        ),
                                                    
                                                    
                                                    )
                                )           )
            label_dict["title"]         = z_string
            label_dict["xaxis"]         = dict(title=x_string)
            label_dict["yaxis"]         = dict(title=y_string)
            trace_dict["zmid"]          = 0
            trace_dict["colorscale"]    = color_palette

        if chart_type == '3D Scatter':
            plot_3D.add_trace(go.Scatter3d  (
                                            z           = z,
                                            x           = x, 
                                            y           = y,
                                            mode        = 'markers',
                                            marker      = dict(
                                                        color       = z,
                                                        colorscale  = "Jet",
                                                        
                                                        opacity     = 0.7,
                                                        colorbar    = dict  (
                                                                            title       = z_string,
                                                                            titleside   = 'right',
                                                                            titlefont   = dict  (
                                                                                                size=12,
                                                                                                family='Arial, sans'
                                                                                                )
                                                                            )  
                                                                ),

                                            hovertemplate = x_string + ': %{x:.2f}' + 
                                                            '<br>' + y_string + ': %{y:.2f}</br>' +
                                                            z_string + ': %{z:.2f}',

          

                                            )           )
            label_dict["title"]         = z_string
            label_dict["xaxis"]         = dict(title=x_string)
            label_dict["yaxis"]         = dict(title=y_string)
            #trace_dict["cmid"]          = 0
            #trace_dict["colorscale"]    = color_palette
    
        plot_3D.update_layout(label_dict)              
        plot_3D.update_traces(trace_dict)

        if (overlay == True) and (chart_type != "3D Scatter" or "Surface") :
            plot_3D.add_trace	(go.Scattergl (  
                            x       		= df[x_string],
                            y       		= df[y_string],
                            name 			= "X: "  + x_string + "</br>Y: "  + y_string,
                            mode            = 'markers',
                            opacity         = overlay_alpha,
                            marker          = dict  (
                                                    color   = overlay_color, 
                                                    symbol  = "circle"
                                                    ),
                            ),     
                )
        
        return plot_3D

def plot_pie(df, err_nm, err_pc, limit_nm, limit_pc):

    Pass = len( df[(abs(err_nm) <= limit_nm) & (abs(err_pc) <= limit_pc)] )
    Fail = len( df[(abs(err_nm) > limit_nm) & (abs(err_pc) > limit_pc)] )


    plot = go.Figure   (
                                    go.Pie  (
                                            labels=['Pass','Fail'], 
                                            values=[Pass, Fail],
                                            marker_colors=["Green","Red"]
                                            )   
                                    )

    return plot

def plot_bowtie(df, t_in, t_in_error_nm, t_in_error_pc, t_measured,speed_rpm_round, limit_nm, limit_pc):

    qual_colors = qualitive_color_dict()

    plot_pc = 0
    plot_pc = df[ (abs(df[t_in]) >= limit_nm/(limit_pc/100)) ]

    plot_nm = 0
    plot_nm = df[ (abs(df[t_in]) < limit_nm/(limit_pc/100)) ]

    plot = go.Figure()

    plot.add_trace(go.Scatter   (  
                                            x               = plot_pc[t_in], 
                                            y               = plot_pc[t_in_error_pc],
                                            name            = t_in_error_pc,
                                            customdata      = plot_pc[t_measured],
                                            text            = plot_pc[speed_rpm_round],
                                            hovertemplate   = 'Torque Measured: %{customdata:.2f} Nm' + 
                                                              '<br>Torque Demanded: %{x:.2f} Nm' +
                                                              '<br>Torque Demanded Error: %{y:.2f} %' +
                                                              '<br>Speed: %{text:.2f} rpm',
                                            mode            = "markers",
                                            marker_symbol   = 'circle-dot',
                                            marker          = dict  (
                                                                    color = qual_colors["Plotly"][1],
                                                                    opacity=0.5,
                                                                    line=dict(
                                                                                color='black',
                                                                                width=1
                                                                                )
                                                                    )
                                )           )


    plot.add_trace(go.Scatter   (  
                                            x               = plot_nm[t_in], 
                                            y               = plot_nm[t_in_error_nm],
                                            name            = "Torque Demanded Error (Nm)",
                                            customdata      = plot_nm[t_measured],
                                            text            = plot_nm[speed_rpm_round],
                                            hovertemplate   = 'Torque Measured: %{customdata:.2f} Nm' + 
                                                              '<br>Torque Demanded: %{x:.2f} Nm' +
                                                              '<br>Torque Demanded Error: %{y:.2f} Nm' +
                                                              '<br>Speed: %{text:.2f} rpm',
                                            mode            = "markers",
                                            marker_symbol   = 'circle-dot',
                                            marker          = dict  (
                                                                    color = qual_colors["Plotly"][0],
                                                                    opacity=0.5,
                                                                    line=dict(
                                                                                color='black',
                                                                                width=1
                                                                                )
                                                                    )
                                )           )

    plot.add_shape(
                                    type = "line",
                                    x0   = 0, 
                                    y0   = limit_nm, 
                                    x1   = limit_nm/(limit_pc/100), 
                                    y1   = limit_nm,
                                    line = dict
                                             (
                                                color=qual_colors["Plotly"][0],
                                                width=2,
                                                dash="dot",
                                            )
                                    )

    plot.add_shape(
                                    type = "line",
                                    x0   = 0, 
                                    y0   = -1* limit_nm, 
                                    x1   = limit_nm/(limit_pc/100), 
                                    y1   = -1* limit_nm,
                                    line = dict
                                             (
                                                color=qual_colors["Plotly"][0],
                                                width=2,
                                                dash="dot",
                                            )
                                    )

    plot.add_shape(
                                    type = "line",
                                    x0   = 0, 
                                    y0   = limit_nm, 
                                    x1   = -limit_nm/(limit_pc/100), 
                                    y1   = limit_nm,
                                    line = dict
                                             (
                                                color=qual_colors["Plotly"][0],
                                                width=2,
                                                dash="dot",
                                            )
                                    )

    plot.add_shape(
                                    type = "line",
                                    x0   = 0, 
                                    y0   = -1* limit_nm, 
                                    x1   = -limit_nm/(limit_pc/100), 
                                    y1   = -1* limit_nm,
                                    line = dict
                                             (
                                                color=qual_colors["Plotly"][0],
                                                width=2,
                                                dash="dot",
                                            )
                                    )

    plot.add_shape(
                                type = "line",
                                x0   = limit_nm/(limit_pc/100), 
                                y0   = min(abs(plot_pc[t_in]))*limit_pc/100, 
                                x1   = max(abs(plot_pc[t_in])), 
                                y1   = max(abs(plot_pc[t_in]))*limit_pc/100,
                                line = dict
                                            (
                                            color=qual_colors["Plotly"][1],
                                            width=2,
                                            dash="dot",
                                        )
                                )

    plot.add_shape(
                                type = "line",
                                x0   = limit_nm/(limit_pc/100), 
                                y0   = min(abs(plot_pc[t_in]))*-limit_pc/100, 
                                x1   = max(abs(plot_pc[t_in])), 
                                y1   = max(abs(plot_pc[t_in]))*-limit_pc/100,
                                line = dict
                                            (
                                            color=qual_colors["Plotly"][1],
                                            width=2,
                                            dash="dot",
                                        )
                                )

    plot.add_shape(
                                type = "line",
                                x0   = -1*limit_nm/(limit_pc/100), 
                                y0   = -1*min(abs(plot_pc[t_in]))*limit_pc/100, 
                                x1   = -1*max(abs(plot_pc[t_in])), 
                                y1   = -1*max(abs(plot_pc[t_in]))*limit_pc/100,
                                line = dict
                                            (
                                            color=qual_colors["Plotly"][1],
                                            width=2,
                                            dash="dot",
                                        )
                                )

    plot.add_shape(
                            type = "line",
                            x0   = -1*limit_nm/(limit_pc/100), 
                            y0   = min(abs(plot_pc[t_in]))*limit_pc/100, 
                            x1   = -1*max(abs(plot_pc[t_in])), 
                            y1   = max(abs(plot_pc[t_in]))*limit_pc/100,
                            line = dict
                                        (
                                        color=qual_colors["Plotly"][1],
                                        width=2,
                                        dash="dot",
                                    )
                            )

    plot.update_layout  (   
                                    title       =str(t_in) + ' & [%] Bowtie',
                                    xaxis_title = t_in,
                                    yaxis_title ='Torque Error',
                                    xaxis       = dict  (
                                                        tickmode = 'linear',
                                                        tick0 = 0, 
                                                        dtick = 50
                                                        )
                                    )

    return plot

def plot_losses(df, loss_mtr, loss_mtr_comp, loss_inv, loss_inv_comp, loss_sys):
    plot = go.Figure()

    plot.add_trace(go.Scatter  (  
                                    x       = df.index.values, 
                                    y       = df[loss_mtr], 
                                    name    = loss_mtr,
                                    hovertemplate = '%{y:.2f} W'
                        )           )

    plot.add_trace(go.Scatter  (  
                                    x       = df.index.values, 
                                    y       = df[loss_mtr_comp], 
                                    name    = loss_mtr_comp,
                                    hovertemplate = '%{y:.2f} W'
                        )           )

    plot.add_trace(go.Scatter  (  
                                    x       = df.index.values, 
                                    y       = df[loss_inv], 
                                    name    = loss_inv,
                                    hovertemplate = '%{y:.2f} W'
                        )           )

    plot.add_trace(go.Scatter  (  
                                    x       = df.index.values, 
                                    y       = df[loss_inv_comp], 
                                    name    = loss_inv_comp,
                                    hovertemplate = '%{y:.2f} W'
                        )           )

    plot.add_trace(go.Scatter  (  
                                    x       = df.index.values, 
                                    y       = df[loss_sys], 
                                    name    = loss_sys,
                                    hovertemplate = '%{y:.2f} W'
                        )           )

    plot.update_layout (   
                            title       ='Losses',
                            xaxis_title ='Sample (N)',
                            yaxis_title ='Losses (W)',
                            hovermode   ="x",
                            hoverlabel_align = 'right',
                            )
    return plot

def plot_powers(df, pwr_mech, pwr_dc, pwr_ac):
    plot = go.Figure()

    plot.add_trace(go.Scatter    (  
                                        x       = df.index.values, 
                                        y       = df[pwr_dc], 
                                        name    = pwr_dc,
                                        hovertemplate = '%{y:.2f} W'
                            )           )

    plot.add_trace(go.Scatter    (  
                                        x       = df.index.values, 
                                        y       = df[pwr_ac],
                                        name    = pwr_ac,
                                        hovertemplate = '%{y:.2f} W' 
                            )           )

    plot.add_trace(go.Scatter    (  
                                        x       = df.index.values, 
                                        y       = df[pwr_mech], 
                                        name    = pwr_mech,
                                        hovertemplate = '%{y:.2f} W'
                            )           )

    plot.update_layout   (   
                                title       ='Powers',
                                xaxis_title ='Sample (N)',
                                yaxis_title ='Power (W)',
                                hovermode   ="x unified",
                                template="plotly_white"
                                )

    return plot