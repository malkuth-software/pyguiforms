"""Python bindings for GUI.Forms, over its C ABI (``gui_forms_abi1``).

    import pyguiforms

    window = pyguiforms.Window("Hello", 320, 120)
    button = pyguiforms.Button(text="Close", bounds=(24, 24, 120, 32))
    window.add(button)

    @button.on("click")
    def clicked(event):
        window.close()

    window.run()

Layers, from the bottom: ``_abi`` (generated from the pinned ABI manifest:
records, slots, constants), ``native`` (ownership, callbacks, failures and
the UI-thread rule), ``schema`` (the library's own type list), ``values``
(Python values as ``gf_value``), and the Pythonic classes: ``controls``,
``_controls`` (one class per schema type, generated from the pinned control
schema) and ``window``; ``forms`` loads form documents, ``binding`` holds
the model values they bind, ``themes`` loads theme sheets, and
``automation`` offers the controls as model tools and an MCP server. The
library loads on the first object created.
"""

from __future__ import annotations

from pyguiforms import automation  # noqa: F401
from pyguiforms import themes  # noqa: F401
from pyguiforms._controls import *  # noqa: F401,F403 (the generated classes, listed in its __all__)
from pyguiforms.binding import Value
from pyguiforms.controls import Component
from pyguiforms.controls import Control
from pyguiforms.controls import Property
from pyguiforms.forms import Form
from pyguiforms.forms import FormError
from pyguiforms.forms import load_form
from pyguiforms.forms import read_form
from pyguiforms.native import CallbackFailure
from pyguiforms.native import Event
from pyguiforms.native import GuiFormsError
from pyguiforms.native import Subscription
from pyguiforms.native import WrongThreadError
from pyguiforms.native import set_failure_hook
from pyguiforms.values import Font
from pyguiforms.values import Insets
from pyguiforms.values import Point
from pyguiforms.values import Rect
from pyguiforms.values import Size
from pyguiforms.values import rgba
from pyguiforms.window import Window
