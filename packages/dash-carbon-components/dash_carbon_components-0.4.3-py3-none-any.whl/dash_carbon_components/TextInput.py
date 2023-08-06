# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TextInput(Component):
    """A TextInput component.
TextInput component

Keyword arguments:

- id (string; optional):
    Specify a custom id for the <input>.

- className (string; optional):
    Specify an optional className to be applied to the wrapper node.

- defaultValue (number | string; optional):
    Optional starting value for uncontrolled state.

- disabled (boolean; default False):
    Specify if the control should be disabled, or not.

- enableCounter (boolean; optional):
    Specify whether to display the character counter.

- helperText (string; default ''):
    Provide text that is used alongside the control label for
    additional help.

- hideLabel (boolean; default False):
    Specify whether you want the underlying label to be visually
    hidden.

- inline (boolean; optional):
    True to use the inline version.

- invalid (boolean; default False):
    Specify if the currently value is invalid.

- invalidText (string; default 'Provide invalidText'):
    Message which is displayed if the value is invalid.

- labelText (string; optional):
    Provide the text that will be read by a screen reader when
    visiting this control.

- light (boolean; default False):
    `True` to use the light version.

- maxCount (number; optional):
    Max character count allowed for the input. This is needed in order
    for enableCounter to display.

- placeholder (string; optional):
    Specify the placeholder attribute for the <input>.

- readOnly (boolean; optional):
    Whether the input should be read-only.

- size (a value equal to: 'sm', 'md', 'lg', 'xl'; optional):
    Specify the size of the Number Input. Currently supports either
    `sm` or `xl` as an option.

- type (string; optional):
    Specify the type of the <input>.

- value (number | string; optional):
    Specify the value of the input.

- warn (boolean; default False):
    Specify whether the control is currently in warning state.

- warnText (string; default ''):
    Provide the text that is displayed when the control is in warning
    state."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_carbon_components'
    _type = 'TextInput'
    @_explicitize_args
    def __init__(self, className=Component.UNDEFINED, defaultValue=Component.UNDEFINED, disabled=Component.UNDEFINED, enableCounter=Component.UNDEFINED, helperText=Component.UNDEFINED, hideLabel=Component.UNDEFINED, id=Component.UNDEFINED, inline=Component.UNDEFINED, invalid=Component.UNDEFINED, invalidText=Component.UNDEFINED, labelText=Component.UNDEFINED, light=Component.UNDEFINED, maxCount=Component.UNDEFINED, onChange=Component.UNDEFINED, onClick=Component.UNDEFINED, placeholder=Component.UNDEFINED, readOnly=Component.UNDEFINED, size=Component.UNDEFINED, type=Component.UNDEFINED, value=Component.UNDEFINED, warn=Component.UNDEFINED, warnText=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'defaultValue', 'disabled', 'enableCounter', 'helperText', 'hideLabel', 'inline', 'invalid', 'invalidText', 'labelText', 'light', 'maxCount', 'placeholder', 'readOnly', 'size', 'type', 'value', 'warn', 'warnText']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'defaultValue', 'disabled', 'enableCounter', 'helperText', 'hideLabel', 'inline', 'invalid', 'invalidText', 'labelText', 'light', 'maxCount', 'placeholder', 'readOnly', 'size', 'type', 'value', 'warn', 'warnText']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TextInput, self).__init__(**args)
