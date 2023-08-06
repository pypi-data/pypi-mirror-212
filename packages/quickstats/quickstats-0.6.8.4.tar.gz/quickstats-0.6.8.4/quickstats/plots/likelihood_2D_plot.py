from typing import Dict, Optional, Union, List
import numpy as np
import pandas as pd

from quickstats.plots import AbstractPlot
from quickstats.plots.template import create_transform
from quickstats.utils.common_utils import combine_dict
from matplotlib.lines import Line2D


class Likelihood2DPlot(AbstractPlot):

    CONFIG = {
        'sigma_levels': ('1sigma', '2sigma', '3sigma'),
        'sigma_pos': 0.93,
        'sigma_names': ('1 $\sigma$', '2 $\sigma$', '3 $\sigma$'),
        'sigma_colors': ("hh:darkblue", "#F2385A", "#FDC536"),
        'highlight_styles': {
            'linewidth': 0,
            'marker': '*',
            'markersize': 20,
            'color': '#E9F1DF',
            'markeredgecolor': 'black'
        },
        'bestfit_styles':{
            'marker': 'P',
            'linewidth': 0,
            'markersize': 15
        },
        'bestfit_label': "Best fit ({x:.2f}, {y:.2f})",
        'cmap': 'GnBu',
        'interpolation': 'cubic',
        'num_grid_points': 500,
    }
    # https://pdg.lbl.gov/2018/reviews/rpp2018-rev-statistics.pdf#page=31
    likelihood_label_threshold = {
        '0.68': 2.30,
        '1sigma': 2.30, # 68.2%
        '0.90': 4.61,
        '0.95': 5.99,
        '2sigma': 6.18, # 95.45%
        '0.99': 9.21,
        '3sigma': 11.83, #  99.73%
    }

    def __init__(self, data_map: Union[pd.DataFrame, Dict[str, pd.DataFrame]],
                 label_map: Optional[Dict] = None,
                 styles_map: Optional[Dict] = None,
                 config_map: Optional[Dict] = None,
                 color_cycle=None,
                 styles: Optional[Union[Dict, str]] = None,
                 analysis_label_options: Optional[Dict] = None,
                 config: Optional[Dict] = None):

        self.data_map = data_map
        self.label_map = label_map
        self.styles_map = styles_map
        self.config_map = config_map
        self.highlight_data = []
        self.legend_order = []
        self.contours = None

        super().__init__(color_cycle=color_cycle,
                         styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)

    def get_default_legend_order(self):
        if not isinstance(self.data_map, dict):
            return self.legend_order
        else:
            return list(self.data_map)

    def draw_single_data(self, ax, data: pd.DataFrame,
                         xattrib: str, yattrib: str, zattrib: str = 'qmu',
                         styles: Optional[Dict] = None,
                         config: Optional[Dict] = None,
                         clabel_size=None, show_colormesh=False):
        if config is None:
            config = self.config
        colors = list(config['sigma_colors'])
        if 'sigma_linestyles' not in config:
            config['sigma_linestyles'] = ['solid'] * \
                len(list(config['sigma_colors']))
        linestyles = list(config['sigma_linestyles'])
        levels = [self.likelihood_label_threshold[key]
                        for key in config['sigma_levels']]
        if config['interpolation'] is not None:
            from scipy import interpolate
            x = data[xattrib]
            y = data[yattrib]
            z = data[zattrib]

            def get_grid(X_range, Y_range, num_grid_points):
                X_points = np.linspace(*X_range, num_grid_points)
                Y_points = np.linspace(*Y_range, num_grid_points)
                X_grid, Y_grid = np.meshgrid(X_points, Y_points)
                return X_grid, Y_grid
            X, Y = get_grid(X_range=(x.min(), x.max()), Y_range=(
                y.min(), y.max()), num_grid_points=config['num_grid_points'])
            Z = interpolate.griddata(
                np.stack((x, y), axis=1), z, (X, Y), method=config['interpolation'])
        else:  # buggy for [dict]
            X_unique = np.sort(self.data_map[xattrib].unique())
            Y_unique = np.sort(self.data_map[yattrib].unique())
            X, Y = np.meshgrid(X_unique, Y_unique)
            Z = self.data_map.pivot_table(
                index=xattrib, columns=yattrib, values=zattrib).T.values - self.data_map[zattrib].min()

        if show_colormesh:
            cmap = config['cmap']
            im = ax.pcolormesh(X, Y, Z, cmap=cmap, shading='auto')
            import matplotlib.pyplot as plt
            self.cbar = plt.colorbar(im, ax=ax, **config['colorbar'])
            self.cbar.set_label(**config['colorbar_label'])
        if levels:
            cp = ax.contour(X, Y, Z, levels=levels, colors=colors,
                        linestyles=linestyles, linewidths=3)
            if clabel_size is not None:
                ax.clabel(cp, inline=True, fontsize=clabel_size)
        custom_handles = [Line2D([0], [0], color=color, linestyle=linestyle, lw=3, label=label) \
                          for color, key, label, linestyle in \
                          zip(config['sigma_colors'], config['sigma_levels'], config['sigma_names'], config['sigma_linestyles'])]
        self.update_legend_handles(
            dict(zip(config['sigma_names'], custom_handles)))
        self.legend_order.extend(config['sigma_names'])
        return custom_handles

    def draw(self, xattrib: str, yattrib: str, zattrib: str = 'qmu', xlabel: Optional[str] = "",
             ylabel: Optional[str] = "", zlabel: Optional[str] = "$-2\Delta ln(L)$",
             ymax: float = 5, ymin: float = -5, xmin: Optional[float] = -10, xmax: Optional[float] = 10,
             clabel_size=None, draw_sm_line: bool = False, draw_bestfit:bool=True,
             show_colormesh=False, show_legend=True):
        ax = self.draw_frame()
        self.contours = {'keys': [], 'contours': [], 'levels': []}
        if isinstance(self.data_map, pd.DataFrame):
            self.draw_single_data(ax, self.data_map, xattrib=xattrib, yattrib=yattrib,
                                  zattrib=zattrib, styles=self.styles_map, config=self.config,
                                  clabel_size=clabel_size, show_colormesh=show_colormesh)
        elif isinstance(self.data_map, dict):
            if self.styles_map is None:
                styles_map = {k: None for k in self.data_map}
            else:
                styles_map = self.styles_map
            if self.label_map is None:
                label_map = {k: k for k in self.data_map}
            else:
                label_map = self.label_map
            if self.config_map is None:
                config_map = {k: k for k in self.data_map}
            else:
                config_map = self.config_map
                
            for key in self.data_map:
                self.contours['keys'].append(key)
                data = self.data_map[key]
                styles = styles_map.get(key, None)
                label = label_map.get(key, "")
                config = config_map.get(key, None)
                config = combine_dict(self.CONFIG, config)
                handle = self.draw_single_data(ax, data,
                                               xattrib=xattrib,
                                               yattrib=yattrib,
                                               zattrib=zattrib,
                                               styles=styles,
                                               config=config,
                                               show_colormesh=show_colormesh)
        else:
            raise ValueError("invalid data format")
        
        highlight_index = 0
        
        if draw_bestfit and isinstance(self.data_map, pd.DataFrame):
            bestfit_idx = np.argmin(self.data_map[zattrib].values)
            bestfit_x   = self.data_map.iloc[bestfit_idx][xattrib]
            bestfit_y   = self.data_map.iloc[bestfit_idx][yattrib]
            highlight_data = {
                'x': bestfit_x,
                'y': bestfit_y,
                'label': self.config["bestfit_label"].format(x=bestfit_x, y=bestfit_y),
                'styles': self.config["bestfit_styles"]
            }
            self.draw_highlight(ax, highlight_data, highlight_index)
            highlight_index += 1
        
        if self.highlight_data is not None:
            for i, h in enumerate(self.highlight_data):
                self.draw_highlight(ax, h, highlight_index + i)

        if draw_sm_line:
            sm_line_styles = self.config['sm_line_styles']
            sm_values = self.config['sm_values']
            transform = create_transform(
                transform_y="axis", transform_x="data")
            ax.vlines(sm_values[0], ymin=0, ymax=1, zorder=0, transform=transform,
                      **sm_line_styles)
            transform = create_transform(
                transform_x="axis", transform_y="data")
            ax.hlines(sm_values[1], xmin=0, xmax=1, zorder=0, transform=transform,
                      **sm_line_styles)

        if show_legend:
            handles, labels = self.get_legend_handles_labels()
            ax.legend(handles, labels, **self.styles['legend'])

        self.draw_axis_components(ax, xlabel=xlabel, ylabel=ylabel)
        self.set_axis_range(ax, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

        return ax

    def draw_highlight(self, ax, data, index=0):
        styles = data['styles']
        if styles is None:
            styles = self.config['highlight_styles']
        handle = ax.plot(data['x'], data['y'], label=data['label'], **styles)
        self.update_legend_handles({f'highlight_{index}': handle[0]})
        self.legend_order.append(f'highlight_{index}')

    def add_highlight(self, x: float, y: float, label: str = "SM prediction",
                      styles: Optional[Dict] = None):
        highlight_data = {
            'x': x,
            'y': y,
            'label': label,
            'styles': styles
        }
        self.highlight_data.append(highlight_data)
