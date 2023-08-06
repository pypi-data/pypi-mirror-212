# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class WebVizContinuousLegend(Component):
    """A WebVizContinuousLegend component.


Keyword arguments:

- id (string; optional)

- colorName (string; required)

- colorTables (list; optional)

- cssLegendStyles (dict with strings as keys and values of type string; optional)

- horizontal (boolean; optional)

- isRangeShown (boolean; optional)

- legendFontSize (number; optional)

- legendScaleSize (number; optional)

- max (number; required)

- min (number; required)

- numberOfTicks (number; optional)

- tickFontSize (number; optional)

- title (string; optional)"""
    @_explicitize_args
    def __init__(self, min=Component.REQUIRED, max=Component.REQUIRED, title=Component.UNDEFINED, cssLegendStyles=Component.UNDEFINED, colorName=Component.REQUIRED, horizontal=Component.UNDEFINED, colorTables=Component.UNDEFINED, id=Component.UNDEFINED, isRangeShown=Component.UNDEFINED, legendFontSize=Component.UNDEFINED, tickFontSize=Component.UNDEFINED, numberOfTicks=Component.UNDEFINED, legendScaleSize=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'colorName', 'colorTables', 'cssLegendStyles', 'horizontal', 'isRangeShown', 'legendFontSize', 'legendScaleSize', 'max', 'min', 'numberOfTicks', 'tickFontSize', 'title']
        self._type = 'WebVizContinuousLegend'
        self._namespace = 'webviz_subsurface_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'colorName', 'colorTables', 'cssLegendStyles', 'horizontal', 'isRangeShown', 'legendFontSize', 'legendScaleSize', 'max', 'min', 'numberOfTicks', 'tickFontSize', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['colorName', 'max', 'min']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(WebVizContinuousLegend, self).__init__(**args)
