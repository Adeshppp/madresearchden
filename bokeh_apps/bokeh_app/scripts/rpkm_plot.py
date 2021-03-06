import numpy as np
import pandas as pd
from bokeh.layouts import column, gridplot, layout
from bokeh.models import ColorBar, HoverTool, Legend, LinearColorMapper, Panel, Whisker
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import TextInput
from bokeh.plotting import figure


def rpkm_plot(data, rpkm_data, rpkm_data_mean_stddev):
    def make_dataset(gene_filter_val):
        """Get data. Return a ColumnDataSource"""
        geness_data = ColumnDataSource(
            rpkm_data[rpkm_data["gene_id"] == gene_filter_val]
        )

        # Umap plot of samples data. Filtered for two sets for the treated/not.
        data.loc[:, "logRPKM"] = "-"
        source_xy_rapa = ColumnDataSource(
            data[data["rapa_treat"] == "yes"].sort_values(by=["stage"])
        )
        source_xy_norapa = ColumnDataSource(data[data["rapa_treat"] == "no"])
        return source_xy_rapa, source_xy_norapa, geness_data

    def make_dataset_time_plot(rpkm_data_mean_stddev, gene_filter_val):
        rapa_data = ColumnDataSource(
            rpkm_data_mean_stddev.loc[gene_filter_val, :, "Rapamycin"].reset_index()
        )
        no_rapa_data = ColumnDataSource(
            rpkm_data_mean_stddev.loc[gene_filter_val, :, "No Rapamycin"].reset_index()
        )

        return rapa_data, no_rapa_data

    def make_plot(xy_rapa, xy_no_rapa, gene_data):
        # needs to plot dependent of a gene ID filter. This needs to be from a text input.
        # Plot tools
        base_plot_options = dict(
            width=500, plot_height=500, tools=["pan, reset, wheel_zoom"], 
        )

        # This is supercede by the other  HoverTool - so set rpkm val to '-' above.
        hover_xy = HoverTool(
            tooltips=[("Rapamycin Treatment", "@rapa_treat"), ("Stage", "@stage")]
        )
        xy_plot_options = base_plot_options.copy()
        # xy_plot_options['tools'].append(hover_xy)

        hover_rpkm = HoverTool(
            tooltips=[
                ("Rapamycin Treatment", "@rapa_treat"),
                ("Stage", "@stage"),
                ("logRPKM", "@logRPKM"),
            ]
        )
        rpkm_plot_options = base_plot_options.copy()
        rpkm_plot_options["tools"].append(hover_rpkm)

        # Plotting the data - xy from umap
        xy_data = figure(**xy_plot_options, title="Samples")
        rapa_xy = xy_data.circle(
            "x",
            "y",
            size=12,
            source=xy_rapa,
            line_width=0,
            color="colours",
            legend="stage",
        )
        no_rapa_xy = xy_data.circle(
            "x",
            "y",
            size=12,
            source=xy_no_rapa,
            fill_alpha=0,
            line_width=2.5,
            color="colours",
        )

        # Mapping colours on logRPKM values.
        # Range the covers 5 - 95 %iles.
        max_c = 10
        min_c = -1
        mapper = LinearColorMapper(palette="Plasma256", low=min_c, high=max_c)

        rpkm_data_plot = figure(**rpkm_plot_options, title="logRPKM")
        rpkm_data_plot.circle(
            "x",
            "y",
            size=12,
            source=gene_data,
            line_color="grey",
            fill_color={"field": "logRPKM", "transform": mapper},
        )

        # Colour bar
        color_bar = ColorBar(color_mapper=mapper, width=8, location=(0, 0))
        rpkm_data_plot.add_layout(color_bar, "right")

        # Maybe have to make two sets of glyphs - not plot them and have these as a legend???

        # # Legend

        # legend = Legend(items=[
        #     ("Rapamycin"   , [rapa_xy], ),
        #     ("No Rapamycin" , [no_rapa_xy], ),

        #     ], location="center", orientation='horizontal')

        # xy_data.add_layout(legend, 'below')

        # Linking the ranges of the two charts so that panning is synced.
        xy_data.x_range = rpkm_data_plot.x_range
        xy_data.y_range = rpkm_data_plot.y_range

        xy_data.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
        xy_data.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
        xy_data.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
        xy_data.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
        xy_data.xaxis.major_label_text_font_size = (
            "0pt"
        )  # preferred method for removing tick labels
        xy_data.yaxis.major_label_text_font_size = (
            "0pt"
        )  # preferred method for removing tick labels

        rpkm_data_plot.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
        rpkm_data_plot.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
        rpkm_data_plot.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
        rpkm_data_plot.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
        rpkm_data_plot.xaxis.major_label_text_font_size = (
            "0pt"
        )  # preferred method for removing tick labels
        rpkm_data_plot.yaxis.major_label_text_font_size = (
            "0pt"
        )  # preferred method for removing tick labels

        # Final plot
        # final= layout([[xy_data, rpkm_data_plot]])
        return xy_data, rpkm_data_plot

    def make_plot_time_plot(rapa_data, no_rapa_data):

        p = figure(width=600, height=400, title="logRPKM Change Over Time")

        p.xaxis.axis_label = "Time (h)"
        p.yaxis.axis_label = "logRPKM"

        rapa_l = p.line(
            "stage", "logRPKM", line_width=2, color="#ea2b1f", source=rapa_data
        )
        rapa_c = p.circle(
            "stage",
            "logRPKM",
            fill_color="white",
            size=8,
            color="#ea2b1f",
            source=rapa_data,
        )
        no_rapa_l = p.line(
            "stage", "logRPKM", line_width=2, color="#5fa8d3", source=no_rapa_data
        )
        no_rapa_c = p.circle(
            "stage",
            "logRPKM",
            fill_color="white",
            size=8,
            color="#5fa8d3",
            source=no_rapa_data,
        )

        legend = Legend(
            items=[
                ("No Rapamycin", [no_rapa_l, no_rapa_c]),
                ("Rapamycin", [rapa_l, rapa_c]),
            ],
            location="center",
            orientation="horizontal",
        )

        p.add_layout(legend, "below")

        # Error bars - note the values are the absolution positions of the upper and lower values e.g. lower values = mean - std dev.
        # TODO not resetting when there is no value that matches in the search.
        w_r = Whisker(
            source=rapa_data,
            base="stage",
            upper="up_std",
            lower="low_std",
            line_color="#ea2b1f",
            line_alpha=0.6,
            line_width=1.5,
        )  # x_range_name='stage')
        w_r.upper_head.line_color = "#ea2b1f"
        w_r.lower_head.line_color = "#ea2b1f"

        w_n_r = Whisker(
            source=no_rapa_data,
            base="stage",
            upper="up_std",
            lower="low_std",
            line_color="#5fa8d3",
            line_alpha=0.6,
            line_width=1.5,
        )  # x_range_name='stage')
        w_n_r.upper_head.line_color = "#5fa8d3"
        w_n_r.lower_head.line_color = "#5fa8d3"

        p.add_layout(w_r)
        p.add_layout(w_n_r)

        return p

    text_input = TextInput(value="PBANKA_1106000", title="Gene ID:")
    source_xy_rapa, source_xy_norapa, geness_data = make_dataset(text_input.value)
    rapa_data, no_rapa_data = make_dataset_time_plot(
        rpkm_data_mean_stddev, text_input.value
    )

    def update(attr, old, new):
        # print(old)
        # print(text_input.value)
        # update_val = old
        if text_input.value in rpkm_data["gene_id"].unique().tolist():

            one, two, new_geness_data = make_dataset(text_input.value)
            geness_data.data.update(new_geness_data.data)

            rapa_data_new, no_rapa_data_new = make_dataset_time_plot(
                rpkm_data_mean_stddev, text_input.value
            )
            rapa_data.data.update(rapa_data_new.data)
            no_rapa_data.data.update(no_rapa_data_new.data)

        else:
            one, two, new_geness_data = make_dataset("")
            geness_data.data.update(new_geness_data.data)

            # rapa_data_new, no_rapa_data_new = make_dataset_time_plot(rpkm_data_mean_stddev, '')
            # rapa_data.data.update(rapa_data_new.data)
            # no_rapa_data.data.update(no_rapa_data_new.data)
            rapa_data.data["logRPKM"] = [0, 0, 0, 0, 0, 0]
            rapa_data.data["std"] = [0, 0, 0, 0, 0, 0]
            rapa_data.data["up_std"] = [0, 0, 0, 0, 0, 0]
            rapa_data.data["low_std"] = [0, 0, 0, 0, 0, 0]

            no_rapa_data.data["logRPKM"] = [0, 0, 0, 0, 0, 0]
            no_rapa_data.data["std"] = [0, 0, 0, 0, 0, 0]
            no_rapa_data.data["up_std"] = [0, 0, 0, 0, 0, 0]
            no_rapa_data.data["low_std"] = [0, 0, 0, 0, 0, 0]

        # print(geness_data.data.keys())
        # print('TEST')

        # text_input = TextInput(value="PBANKA_0000301", title="Gene ID:")
        # source_xy_rapa, source_xy_norapa, geness_data = make_dataset(text_input.value)

    p1, p2 = make_plot(source_xy_rapa, source_xy_norapa, geness_data)
    time_p = make_plot_time_plot(rapa_data, no_rapa_data)
    # final = layout([[text_input], [p], [time_p]])

    final = gridplot(
        children=[[text_input, None], [p1, p2,], [time_p, None]],
        toolbar_location="above",
        sizing_mode="fixed",
    )

    final_tab = Panel(child=final, title="Samples Plot")
    text_input.on_change("value", update)

    return final_tab
