#!/usr/bin/env python
"""
"""
from __future__ import unicode_literals

from prompt_toolkit.application import Application
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.eventloop import create_event_loop, set_event_loop
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.layout.containers import VSplit, HSplit, Float
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.layout.widgets import TextArea, Label, Frame, Box, Checkbox, Dialog, Button, RadioList, MenuContainer, MenuItem, ProgressBar
from prompt_toolkit.styles import Style
from pygments.lexers import HtmlLexer


loop = create_event_loop()
set_event_loop(loop)


# >>>

def accept_yes(app):
    app.set_return_value(True)

def accept_no(app):
    app.set_return_value(False)

def do_exit(app):
    app.set_return_value(False)


# Make partials that pass the loop everywhere.

yes_button = Button(text='Yes', handler=accept_yes)
no_button = Button(text='No', handler=accept_no)
textfield  = TextArea(lexer=PygmentsLexer(HtmlLexer))
textfield2 = TextArea()
checkbox1 = Checkbox(text='Checkbox')
checkbox2 = Checkbox(text='Checkbox')

radios = RadioList(loop=loop, values=[
    ('Red', 'red'),
    ('Green', 'green'),
    ('Blue', 'blue'),
    ('Orange', 'orange'),
    ('Yellow', 'yellow'),
    ('Purple', 'Purple'),
    ('Brown', 'Brown'),
])

animal_completer = WordCompleter([
    'alligator', 'ant', 'ape', 'bat', 'bear', 'beaver', 'bee', 'bison',
    'butterfly', 'cat', 'chicken', 'crocodile', 'dinosaur', 'dog', 'dolphin',
    'dove', 'duck', 'eagle', 'elephant', 'fish', 'goat', 'gorilla', 'kangaroo',
    'leopard', 'lion', 'mouse', 'rabbit', 'rat', 'snake', 'spider', 'turkey',
    'turtle', ], ignore_case=True)

root_container = HSplit([
    VSplit([
        Frame(body=Label(text='Left frame\ncontent')),
        Dialog(title='The custom window',
               body=Label('hello')),
    ]),
    VSplit([
        Frame(body=HSplit([
            textfield,
            ProgressBar(),
        ])),
        #VerticalLine(),
        Frame(body=HSplit([
            checkbox1,
            checkbox2,
            TextArea(),  # XXX: remove
        ], align='TOP')),
        Frame(body=radios),
    ], padding=1),
    Box(
        body=VSplit([
            yes_button,
            no_button,
        ], align='CENTER', padding=3),
        style='class:button-bar',
        height=3,
    ),
])

root_container = MenuContainer(loop=loop, body=root_container, menu_items=[
    MenuItem('File', children=[
        MenuItem('New'),
        MenuItem('Open', children=[
            MenuItem('From file...'),
            MenuItem('From URL...'),
            MenuItem('Something else..', children=[
                MenuItem('A'),
                MenuItem('B'),
                MenuItem('C'),
                MenuItem('D'),
                MenuItem('E'),
            ]),
        ]),
        MenuItem('Save'),
        MenuItem('Save as...'),
        MenuItem('-', disabled=True),
        MenuItem('Exit', handler=do_exit),
        ]),
    MenuItem('Edit', children=[
        MenuItem('Undo'),
        MenuItem('Cut'),
        MenuItem('Copy'),
        MenuItem('Paste'),
        MenuItem('Delete'),
        MenuItem('-', disabled=True),
        MenuItem('Find'),
        MenuItem('Find next'),
        MenuItem('Replace'),
        MenuItem('Go To'),
        MenuItem('Select All'),
        MenuItem('Time/Date'),
    ]),
    MenuItem('View', children=[
        MenuItem('Status Bar'),
    ]),
    MenuItem('Info', children=[
        MenuItem('About'),
    ]),
], floats=[
    Float(xcursor=True,
          ycursor=True,
          content=CompletionsMenu(
              max_height=16,
              scroll_offset=1)),
])

# Global key bindings.
bindings = KeyBindings()
bindings.add('tab')(focus_next)
bindings.add('s-tab')(focus_previous)


style = Style.from_dict({
    'window.border': '#888888',
    'shadow': 'bg:#222222',

    'menubar': 'bg:#aaaaaa #888888',
    'menubar.selecteditem': 'bg:#ffffff #000000',
    'menu': 'bg:#888888 #ffffff',
    'menu.border': '#aaaaaa',
    'window.border shadow': '#444444',

    'focussed  button': 'bg:#880000 #ffffff noinherit',

    # Styling for Dialog widgets.

    'radiolist focussed': 'noreverse',
    'radiolist focussed radio.selected': 'reverse',

    'button-bar': 'bg:#aaaaff'
})


application = Application(
    loop=loop,
    layout=Layout(
        root_container,
        focussed_window=yes_button,
    ),
    key_bindings=merge_key_bindings([
        load_key_bindings(),
        bindings,
    ]),
    style=style,
    mouse_support=True,
    full_screen=True)


def run():
    result = application.run()
    print('You said: %r' % result)


if __name__ == '__main__':
    run()