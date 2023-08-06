# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class WebVizColorLegend(Component):
    """A WebVizColorLegend component.


Keyword arguments:

- colorName (string; optional)

- colorTables (list; optional)

- cssLegendStyles (dict with strings as keys and values of type string; optional)

- discreteData (boolean | number | string | dict | list; optional)

- horizontal (boolean; optional)

- isModal (boolean; optional)

- isRangeShown (boolean; optional)

- legendFontSize (number; optional)

- legendScaleSize (number; optional)

- max (number; optional)

- min (number; optional)

- numberOfTicks (number; optional)

- openColorSelector (boolean; optional)

- reverseRange (boolean; optional)

- tickFontSize (number; optional)

- title (string; optional)"""
    @_explicitize_args
    def __init__(self, colorTables=Component.UNDEFINED, min=Component.UNDEFINED, max=Component.UNDEFINED, title=Component.UNDEFINED, colorName=Component.UNDEFINED, horizontal=Component.UNDEFINED, discreteData=Component.UNDEFINED, reverseRange=Component.UNDEFINED, isModal=Component.UNDEFINED, cssLegendStyles=Component.UNDEFINED, isRangeShown=Component.UNDEFINED, legendFontSize=Component.UNDEFINED, tickFontSize=Component.UNDEFINED, numberOfTicks=Component.UNDEFINED, legendScaleSize=Component.UNDEFINED, openColorSelector=Component.UNDEFINED, **kwargs):
        self._prop_names = ['colorName', 'colorTables', 'cssLegendStyles', 'discreteData', 'horizontal', 'isModal', 'isRangeShown', 'legendFontSize', 'legendScaleSize', 'max', 'min', 'numberOfTicks', 'openColorSelector', 'reverseRange', 'tickFontSize', 'title']
        self._type = 'WebVizColorLegend'
        self._namespace = 'webviz_subsurface_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['colorName', 'colorTables', 'cssLegendStyles', 'discreteData', 'horizontal', 'isModal', 'isRangeShown', 'legendFontSize', 'legendScaleSize', 'max', 'min', 'numberOfTicks', 'openColorSelector', 'reverseRange', 'tickFontSize', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(WebVizColorLegend, self).__init__(**args)
