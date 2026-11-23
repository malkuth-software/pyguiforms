"""Form documents (``.form``, gui_forms docs/user/forms.md), loaded from Python.

    form = pyguiforms.load_form("settings.form", model=settings)
    form.settings_ok.on("click")(save)
    form.run()

A form document is XML in the namespace ``urn:gui-forms:form:1``. Each
element is an object named by its schema type in kebab case (``form`` is
the window), ``id`` is its stable ID, every other attribute a property in
kebab case, and a ``bind`` element binds a property to a model value. The
C++ build generates a class from a document; Python reads it at run time
in two steps:

1. ``read_form`` checks the document against the pinned schema (the
   generated classes) and gives a ``FormPlan``, or raises ``FormError``
   with every defect found, each with its gui_forms code (E801 to E821),
   line and column. It needs no library.
2. ``build_form`` makes the plan's objects in document order, sets the
   properties in the order written, makes the bindings and gives a
   ``Form``. A value the library refuses is reported as E807 with its
   place, and nothing made is kept.

Differences from the C++ form compiler, each refused with E999 so a
document never half-loads: a ``bind`` with ``field`` (a BindingSource) or
on ``command``, a grid's ``span`` elements and a property the parent's type
provides (``area``, ``cell``). A binding's ``to`` names an attribute of the
model that is a ``pyguiforms.Value``; it binds two way unless
``mode="one-way"``, and a property that raises no change binds one way in
effect. The form's ``accept-button`` and ``cancel-button`` are checked
(each must name a button of the document) and kept on the ``Form``; the
window does not act on Enter and Escape for them yet.

The XML reader admits what gui_forms' admits: UTF-8, elements, attributes,
comments, the predefined entities and character references, and the
leading XML declaration; no DTD, CDATA section or other processing
instruction. A document is bounded: at most ``MAXIMUM_DOCUMENT_BYTES``
bytes, ``MAXIMUM_DEPTH`` levels and ``MAXIMUM_OBJECTS`` objects.
"""

from __future__ import annotations

import pathlib
import re
import xml.parsers.expat

from pyguiforms import _abi
from pyguiforms import _controls
from pyguiforms import binding
from pyguiforms import controls
from pyguiforms import native
from pyguiforms import values
from pyguiforms import window

NAMESPACE: str = "urn:gui-forms:form:1"
MAXIMUM_DOCUMENT_BYTES: int = 4 * 1024 * 1024
MAXIMUM_DEPTH: int = 128
MAXIMUM_OBJECTS: int = 16384
MAXIMUM_VALUE_TOKENS: int = 256

# The root's own properties (gui_forms form_root_type): the window's.
ROOT_PROPERTIES: tuple[str, ...] = ("text", "client_size", "accept_button", "cancel_button")
BIND_ATTRIBUTES: tuple[str, ...] = ("property", "to", "field", "mode", "update", "converter")
BIND_MODES: tuple[str, ...] = ("one-way", "two-way")
BIND_UPDATES: tuple[str, ...] = ("on-validate", "on-change")
RENAMED_PROPERTIES: dict[str, str] = {
    "layout_direction": "write right-to-left instead: left-to-right is no, right-to-left is yes, inherit is inherit",
}
NOT_EXPRESSIBLE_KINDS: tuple[str, ...] = ("image", "object", "null")

# The diagnostic codes' names (forms.md, Refusals).
CODE_NAMES: dict[str, str] = {
    "E801": "form_root_invalid",
    "E802": "form_type_unknown",
    "E803": "form_identity_repeated",
    "E804": "form_property_unknown",
    "E805": "form_property_read_only",
    "E806": "form_member_repeated",
    "E807": "form_value_invalid",
    "E809": "form_children_not_admitted",
    "E810": "form_style_block",
    "E812": "form_generation_refused",
    "E813": "form_presentation_property",
    "E815": "form_escape_invalid",
    "E816": "form_handler_removed",
    "E817": "form_binding_invalid",
    "E818": "form_binding_option_invalid",
    "E820": "form_property_renamed",
    "E821": "form_xml_invalid",
    "E999": "not_yet_built",
}

KEBAB: re.Pattern = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
IDENTIFIER: re.Pattern = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
NUMBER: re.Pattern = re.compile(r"[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][+-]?[0-9]+)?")
INTEGER: re.Pattern = re.compile(r"[+-]?[0-9]+")
COLOR: re.Pattern = re.compile(r"#([0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})")
SINGLE_ESCAPES: dict[str, str] = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "'": "'", "\\": "\\"}


# ----------------------------------------------------------------- diagnostics


class Diagnostic:
    """One defect: its code, place, the object's stable ID, what was written there, and a detail."""

    def __init__(self, code: str, file: str, line: int, column: int, stable_id: str, written: str,
                 detail: str) -> None:
        self.code: str = code
        self.name: str = CODE_NAMES.get(code, "form_unknown")
        self.file: str = file
        self.line: int = line
        self.column: int = column
        self.stable_id: str = stable_id
        self.written: str = written
        self.detail: str = detail

    def __str__(self) -> str:
        place: str = self.file + ":" + str(self.line) + ":" + str(self.column)
        text: str = place + ": " + self.code + " " + self.name
        if self.written != "":
            text += " (" + self.written + ")"
        if self.detail != "":
            text += ": " + self.detail
        return text


class FormError(Exception):
    """A refused document: every defect found, in document order."""

    def __init__(self, diagnostics: list[Diagnostic]) -> None:
        lines: list[str] = []
        for diagnostic in diagnostics:
            lines.append(str(diagnostic))
        super().__init__("the form document is refused:\n" + "\n".join(lines))
        self.diagnostics: list[Diagnostic] = diagnostics

    def codes(self) -> list[str]:
        found: list[str] = []
        for diagnostic in self.diagnostics:
            found.append(diagnostic.code)
        return found


# ------------------------------------------------------------------ the reader


class Element:
    """An XML element as read: its name, attributes in order, children and place."""

    def __init__(self, name: str, attributes: list[tuple[str, str]], line: int, column: int) -> None:
        self.name: str = name
        self.attributes: list[tuple[str, str]] = attributes
        self.line: int = line
        self.column: int = column
        self.children: list[Element] = []


class XmlReader:
    """Reads a document into Elements with expat, admitting gui_forms' XML subset only."""

    def __init__(self, file: str, diagnostics: list[Diagnostic]) -> None:
        self.file: str = file
        self.diagnostics: list[Diagnostic] = diagnostics
        self.parser: xml.parsers.expat.XMLParserType = xml.parsers.expat.ParserCreate("UTF-8")
        self.parser.ordered_attributes = True
        self.parser.SetParamEntityParsing(xml.parsers.expat.XML_PARAM_ENTITY_PARSING_NEVER)
        self.parser.StartElementHandler = self.start
        self.parser.EndElementHandler = self.end
        self.parser.CharacterDataHandler = self.text
        self.parser.StartDoctypeDeclHandler = self.doctype
        self.parser.ProcessingInstructionHandler = self.instruction
        self.parser.StartCdataSectionHandler = self.cdata
        self.parser.EntityDeclHandler = self.entity
        self.parser.ExternalEntityRefHandler = self.external_entity
        self.stack: list[Element] = []
        self.root: Element | None = None
        self.element_count: int = 0
        self.refused: bool = False

    def place(self) -> tuple[int, int]:
        return (self.parser.CurrentLineNumber, self.parser.CurrentColumnNumber + 1)

    def refuse(self, detail: str) -> None:
        line, column = self.place()
        self.diagnostics.append(Diagnostic("E821", self.file, line, column, "", "", detail))
        self.refused = True

    def start(self, name: str, flat_attributes: list[str]) -> None:
        line, column = self.place()
        attributes: list[tuple[str, str]] = []
        for index in range(0, len(flat_attributes), 2):
            attributes.append((flat_attributes[index], flat_attributes[index + 1]))
        element: Element = Element(name, attributes, line, column)
        self.element_count += 1
        if self.element_count > MAXIMUM_OBJECTS:
            self.refuse("more than " + str(MAXIMUM_OBJECTS) + " elements")
            raise StopReading()
        if len(self.stack) >= MAXIMUM_DEPTH:
            self.refuse("deeper than " + str(MAXIMUM_DEPTH) + " levels")
            raise StopReading()
        if len(self.stack) == 0:
            self.root = element
        else:
            self.stack[-1].children.append(element)
        self.stack.append(element)

    def end(self, name: str) -> None:
        self.stack.pop()

    def text(self, data: str) -> None:
        if data.strip() != "":
            self.refuse("text inside an object: only whitespace and comments go between children")

    def doctype(self, *unused: object) -> None:
        self.refuse("a DTD is not admitted")
        raise StopReading()

    def instruction(self, target: str, data: str) -> None:
        self.refuse("a processing instruction is not admitted (only the leading XML declaration)")

    def cdata(self) -> None:
        self.refuse("a CDATA section is not admitted")
        raise StopReading()

    def entity(self, *unused: object) -> None:
        self.refuse("an entity declaration is not admitted")
        raise StopReading()

    def external_entity(self, *unused: object) -> int:
        self.refuse("an external entity is not admitted")
        return 0

    def read(self, document: bytes) -> Element | None:
        if len(document) > MAXIMUM_DOCUMENT_BYTES:
            self.diagnostics.append(Diagnostic("E821", self.file, 1, 1, "", "",
                                               "larger than " + str(MAXIMUM_DOCUMENT_BYTES) + " bytes"))
            return None
        try:
            self.parser.Parse(document, True)
        except StopReading:
            return None
        except xml.parsers.expat.ExpatError as failure:
            detail: str = xml.parsers.expat.ErrorString(failure.code)
            self.diagnostics.append(Diagnostic("E821", self.file, failure.lineno, failure.offset + 1, "", "",
                                               detail))
            return None
        if self.refused:
            return None
        return self.root


class StopReading(Exception):
    """Ends a read the reader refused."""


# -------------------------------------------------------------------- the plan


class BindPlan:
    """A checked binding: the property, the model attribute and whether it writes back."""

    def __init__(self, property_name: str, source: str, two_way: bool, line: int, column: int) -> None:
        self.property_name: str = property_name
        self.source: str = source
        self.two_way: bool = two_way
        self.line: int = line
        self.column: int = column


class Assignment:
    """A checked property value, in the order written."""

    def __init__(self, name: str, value: object, written: str, line: int, column: int) -> None:
        self.name: str = name
        self.value: object = value
        self.written: str = written
        self.line: int = line
        self.column: int = column


class ObjectPlan:
    """A checked object: its class, stable ID, assignments, bindings and children."""

    def __init__(self, component_class: type, stable_id: str, line: int, column: int) -> None:
        self.component_class: type = component_class
        self.stable_id: str = stable_id
        self.line: int = line
        self.column: int = column
        self.assignments: list[Assignment] = []
        self.bindings: list[BindPlan] = []
        self.children: list[ObjectPlan] = []
        # Components written inside (a command, a timer): made and kept, never in the control tree.
        self.components: list[ObjectPlan] = []


class FormPlan:
    """A checked document: the window's properties when its root is ``form``, and the root object."""

    def __init__(self, file: str) -> None:
        self.file: str = file
        self.window_id: str | None = None
        self.title: str = ""
        self.client_size: values.Size | None = None
        self.accept_button: str | None = None
        self.cancel_button: str | None = None
        self.root: ObjectPlan | None = None
        self.components: list[ObjectPlan] = []

    def binds(self) -> bool:
        pending: list[ObjectPlan] = list(self.components)
        if self.root is not None:
            pending.append(self.root)
        while len(pending) > 0:
            plan: ObjectPlan = pending.pop()
            if len(plan.bindings) > 0:
                return True
            pending.extend(plan.children)
            pending.extend(plan.components)
        return False


def registered_from_kebab(written: str) -> str | None:
    """The registered (snake case) name a kebab-case name spells; None for any other spelling."""
    if KEBAB.fullmatch(written) is None:
        return None
    return written.replace("-", "_")


def schema_properties(component_class: type) -> dict[str, controls.Property]:
    """The schema properties a generated class declares, by name."""
    found: dict[str, controls.Property] = {}
    for owner in component_class.__mro__:
        for name, member in vars(owner).items():
            if isinstance(member, controls.Property) and name not in found:
                found[name] = member
    return found


def split_list(text: str) -> list[str] | str:
    """A text collection's items: whitespace-separated, a quoted item with escapes; the fault's text when refused."""
    items: list[str] = []
    index: int = 0
    while index < len(text):
        character: str = text[index]
        if character.isspace():
            index += 1
            continue
        if character != '"' and character != "'":
            end: int = index
            while end < len(text) and not text[end].isspace():
                end += 1
            items.append(text[index:end])
            index = end
            continue
        quote: str = character
        index += 1
        item: list[str] = []
        closed: bool = False
        while index < len(text):
            character = text[index]
            if character == quote:
                closed = True
                index += 1
                break
            if character != "\\":
                item.append(character)
                index += 1
                continue
            escaped: str = text[index + 1] if index + 1 < len(text) else ""
            meaning: str | None = SINGLE_ESCAPES.get(escaped)
            if meaning is not None:
                item.append(meaning)
                index += 2
                continue
            if escaped == "u" and text[index + 2:index + 3] == "{":
                close: int = text.find("}", index + 3)
                digits: str = text[index + 3:close] if close > 0 else ""
                if 1 <= len(digits) <= 6 and re.fullmatch(r"[0-9a-fA-F]+", digits) is not None:
                    scalar: int = int(digits, 16)
                    if scalar <= 0x10FFFF and not 0xD800 <= scalar <= 0xDFFF:
                        item.append(chr(scalar))
                        index = close + 1
                        continue
            return "\\" + escaped
        if not closed:
            return quote
        items.append("".join(item))
        if len(items) > MAXIMUM_VALUE_TOKENS * 64:
            return text[index:index + 16]
    return items


def color_value(word: str) -> int:
    digits: str = word[1:]
    channels: list[int] = [0, 0, 0, 255]
    short: bool = len(digits) <= 4
    count: int = len(digits) if short else len(digits) // 2
    for channel in range(count):
        if short:
            channels[channel] = int(digits[channel], 16) * 17
        else:
            channels[channel] = int(digits[channel * 2:channel * 2 + 2], 16)
    return values.rgba(channels[0], channels[1], channels[2], channels[3])


class ValueParser:
    """Reads one attribute's value by its property's kind (gui_forms form_model's grammar)."""

    def __init__(self, listed: controls.Property) -> None:
        self.listed: controls.Property = listed

    def parse(self, text: str) -> tuple[object, str]:
        """(the value, "") or (None, the offending word)."""
        kind: str = self.listed.kind
        if kind == "text":
            return (text, "")
        if kind == "collection":
            items: list[str] | str = split_list(text)
            if isinstance(items, str):
                return (None, items)
            return (items, "")
        words: list[str] = text.split()
        if len(words) == 0 or len(words) > MAXIMUM_VALUE_TOKENS:
            return (None, text)
        if kind == "boolean":
            if len(words) == 1 and words[0] in ("true", "false"):
                return (words[0] == "true", "")
            return (None, words[0] if len(words) == 1 else words[1])
        if kind == "signed_integer" or kind == "unsigned_integer":
            if len(words) != 1 or INTEGER.fullmatch(words[0]) is None:
                return (None, words[-1])
            integer: int = int(words[0])
            if abs(integer) > 9 * 10 ** 15 or (kind == "unsigned_integer" and integer < 0):
                return (None, words[0])
            return (integer, "")
        if kind == "number":
            if len(words) != 1 or NUMBER.fullmatch(words[0]) is None:
                return (None, words[-1])
            return (float(words[0]), "")
        if kind in ("point", "size", "rectangle", "insets"):
            return self.geometry(words)
        if kind == "color":
            if len(words) != 1 or COLOR.fullmatch(words[0]) is None:
                return (None, words[-1])
            return (color_value(words[0]), "")
        if kind == "enumeration":
            return self.enumeration(words)
        if kind == "font":
            return self.font(words)
        return (None, text)

    def geometry(self, words: list[str]) -> tuple[object, str]:
        numbers: list[float] = []
        for word in words:
            if NUMBER.fullmatch(word) is None:
                return (None, word)
            numbers.append(float(word))
        kind: str = self.listed.kind
        if kind == "point" and len(numbers) == 2:
            return (values.Point(numbers[0], numbers[1]), "")
        if kind == "size" and len(numbers) == 2:
            return (values.Size(numbers[0], numbers[1]), "")
        if kind == "rectangle" and len(numbers) == 4:
            return (values.Rect(numbers[0], numbers[1], numbers[2], numbers[3]), "")
        # Insets in CSS order: all; vertical and horizontal; top right bottom left.
        if kind == "insets" and len(numbers) == 1:
            return (values.Insets(numbers[0], numbers[0], numbers[0], numbers[0]), "")
        if kind == "insets" and len(numbers) == 2:
            return (values.Insets(numbers[1], numbers[0], numbers[1], numbers[0]), "")
        if kind == "insets" and len(numbers) == 4:
            return (values.Insets(numbers[3], numbers[0], numbers[1], numbers[2]), "")
        return (None, words[-1])

    def enumeration(self, words: list[str]) -> tuple[object, str]:
        names: list[str] = []
        for word in words:
            registered: str | None = registered_from_kebab(word)
            if registered is None or (len(self.listed.choices) > 0 and registered not in self.listed.choices):
                return (None, word)
            names.append(registered)
        # The library combines flags written "a, b" and refuses several of a plain enumeration.
        return (", ".join(names), "")

    def font(self, words: list[str]) -> tuple[object, str]:
        roles: dict[str, str] = {"control": "GF_FONT_ROLE_CONTROL", "content": "GF_FONT_ROLE_CONTENT",
                                 "monospace": "GF_FONT_ROLE_MONOSPACE"}
        if len(words) < 3 or len(words) > 6 or words[0] not in roles:
            return (None, words[0] if len(words) >= 3 else words[-1])
        if NUMBER.fullmatch(words[1]) is None or not 0.0 < float(words[1]) <= 4096.0:
            return (None, words[1])
        if INTEGER.fullmatch(words[2]) is None or not 1 <= int(words[2]) <= 1000:
            return (None, words[2])
        italic: bool = False
        spacing: float = 0.0
        next_word: int = 3
        if next_word < len(words) and words[next_word] == "italic":
            italic = True
            next_word += 1
        if next_word < len(words):
            if words[next_word] != "spacing" or next_word + 2 != len(words):
                return (None, words[next_word])
            if NUMBER.fullmatch(words[next_word + 1]) is None:
                return (None, words[next_word + 1])
            spacing = float(words[next_word + 1])
            next_word += 2
        role: int = getattr(_abi, roles[words[0]])
        font: values.Font = values.Font(role, int(words[2]), italic, float(words[1]), spacing)
        return (font, "")


class Checker:
    """Checks a read document against the generated classes, collecting every defect."""

    def __init__(self, file: str, diagnostics: list[Diagnostic]) -> None:
        self.file: str = file
        self.diagnostics: list[Diagnostic] = diagnostics
        self.stable_ids: dict[str, ObjectPlan] = {}

    def report(self, code: str, element: Element, stable_id: str, written: str, detail: str) -> None:
        self.diagnostics.append(Diagnostic(code, self.file, element.line, element.column, stable_id, written,
                                           detail))

    def check_namespace(self, root: Element) -> None:
        for element in walk(root):
            for name, value in element.attributes:
                if name != "xmlns" and not name.startswith("xmlns:"):
                    continue
                if element is root and name == "xmlns" and value == NAMESPACE:
                    continue
                self.report("E821", element, "", name, "only the root declares xmlns=\"" + NAMESPACE + "\"")
        declared: bool = False
        for name, value in root.attributes:
            if name == "xmlns" and value == NAMESPACE:
                declared = True
        if not declared:
            self.report("E821", root, "", "xmlns", "the root declares xmlns=\"" + NAMESPACE + "\"")

    def plan(self, root: Element) -> FormPlan:
        plan: FormPlan = FormPlan(self.file)
        self.check_namespace(root)
        if root.name == "form":
            plan.window_id = self.read_id(root)
            self.read_root_properties(root, plan)
            # A form holds one control, its root, and any components (gui_forms check_form_root).
            control_count: int = 0
            for child in root.children:
                child_plan: ObjectPlan | None = self.plan_object(child)
                if child_plan is None:
                    continue
                if not issubclass(child_plan.component_class, controls.Control):
                    plan.components.append(child_plan)
                    continue
                control_count += 1
                if plan.root is None:
                    plan.root = child_plan
            if control_count != 1:
                self.report("E801", root, plan.window_id or "", "form", "a form holds one control")
        else:
            plan.root = self.plan_object(root)
            if plan.root is not None and not issubclass(plan.root.component_class, controls.Control):
                self.report("E801", root, plan.root.stable_id, root.name, "the root is a form or a control")
                plan.root = None
        self.check_buttons(root, plan)
        return plan

    def read_id(self, element: Element) -> str | None:
        for name, value in element.attributes:
            if name == "id":
                return value
        self.report("E801", element, "", element.name, "an object needs an id")
        return None

    def read_root_properties(self, root: Element, plan: FormPlan) -> None:
        for name, value in root.attributes:
            if name == "id" or name == "xmlns" or name.startswith("xmlns:"):
                continue
            registered: str | None = registered_from_kebab(name)
            if registered is None or registered not in ROOT_PROPERTIES:
                self.report("E804", root, plan.window_id or "", name, "form")
                continue
            if registered == "text":
                plan.title = value
            elif registered == "client_size":
                parsed, offending = ValueParser(controls.Property("client_size", "size", True, "")).parse(value)
                if parsed is None:
                    self.report("E807", root, plan.window_id or "", name, "not a size: " + offending)
                else:
                    plan.client_size = parsed
            elif registered == "accept_button":
                plan.accept_button = value
            else:
                plan.cancel_button = value

    def check_buttons(self, root: Element, plan: FormPlan) -> None:
        for written, stable_id in (("accept-button", plan.accept_button), ("cancel-button", plan.cancel_button)):
            if stable_id is None:
                continue
            found: ObjectPlan | None = self.stable_ids.get(stable_id)
            if found is None or not issubclass(found.component_class, _controls.Button):
                self.report("E807", root, plan.window_id or "", written, "names no button of the document: " +
                            stable_id)

    def plan_object(self, element: Element) -> ObjectPlan | None:
        if element.name == "style":
            self.report("E810", element, "", "style", "the look belongs to the theme, reached by classes")
            return None
        if element.name in ("bind", "span", "form"):
            detail: str = "a form is the root alone" if element.name == "form" else "not an object here"
            if element.name == "span":
                detail = "grid spans are not loaded from Python yet"
            self.report("E999" if element.name == "span" else "E801", element, "", element.name, detail)
            return None
        stable_id: str | None = self.read_id(element)
        registered: str | None = registered_from_kebab(element.name)
        component_class: type | None = None
        if registered is not None:
            component_class = _controls.TYPES.get(registered)
        if component_class is None:
            self.report("E802", element, stable_id or "", element.name, "the schema lists no such type")
            return None
        if stable_id is None:
            return None
        plan: ObjectPlan = ObjectPlan(component_class, stable_id, element.line, element.column)
        if stable_id in self.stable_ids:
            self.report("E803", element, stable_id, "id", "")
        else:
            self.stable_ids[stable_id] = plan
        written_names: set[str] = set()
        listed: dict[str, controls.Property] = schema_properties(component_class)
        for name, value in element.attributes:
            if name == "id" or name == "xmlns" or name.startswith("xmlns:"):
                continue
            self.plan_property(element, plan, listed, written_names, name, value)
        for child in element.children:
            if child.name == "bind":
                self.plan_binding(child, plan, listed, written_names)
                continue
            if not issubclass(component_class, controls.Control):
                self.report("E809", child, stable_id, child.name, component_class.__name__ + " holds no children")
                continue
            child_plan: ObjectPlan | None = self.plan_object(child)
            if child_plan is None:
                continue
            if issubclass(child_plan.component_class, controls.Control):
                plan.children.append(child_plan)
            else:
                plan.components.append(child_plan)
        return plan

    def admitted_property(self, element: Element, plan: ObjectPlan, listed: dict[str, controls.Property],
                          written_names: set[str], written: str) -> controls.Property | None:
        registered: str | None = registered_from_kebab(written)
        if registered is not None and registered in RENAMED_PROPERTIES:
            self.report("E820", element, plan.stable_id, written, RENAMED_PROPERTIES[registered])
            return None
        found: controls.Property | None = listed.get(registered) if registered is not None else None
        if found is None and written.startswith("on-"):
            self.report("E816", element, plan.stable_id, written,
                        "a form names no program code: attach the behaviour from Python")
            return None
        if found is None:
            self.report("E804", element, plan.stable_id, written, plan.component_class.__name__)
            return None
        if not found.writable:
            self.report("E805", element, plan.stable_id, written, "")
            return None
        if not found.content and (found.kind == "font" or found.kind == "color"):
            self.report("E813", element, plan.stable_id, written,
                        "set it in the theme on a class the object names in classes")
            return None
        if found.name in written_names:
            self.report("E806", element, plan.stable_id, written, "")
            return None
        written_names.add(found.name)
        return found

    def plan_property(self, element: Element, plan: ObjectPlan, listed: dict[str, controls.Property],
                      written_names: set[str], written: str, text: str) -> None:
        found: controls.Property | None = self.admitted_property(element, plan, listed, written_names, written)
        if found is None:
            return
        if found.kind in NOT_EXPRESSIBLE_KINDS:
            self.report("E807", element, plan.stable_id, written, "a " + found.kind + " is not written in a form")
            return
        parsed, offending = ValueParser(found).parse(text)
        if parsed is None:
            code: str = "E815" if found.kind == "collection" and offending.startswith("\\") else "E807"
            self.report(code, element, plan.stable_id, written, "refused at " + repr(offending))
            return
        plan.assignments.append(Assignment(found.name, parsed, written, element.line, element.column))

    def plan_binding(self, element: Element, plan: ObjectPlan, listed: dict[str, controls.Property],
                     written_names: set[str]) -> None:
        options: dict[str, str] = {}
        for name, value in element.attributes:
            if name not in BIND_ATTRIBUTES:
                self.report("E818", element, plan.stable_id, name, "a bind takes " + ", ".join(BIND_ATTRIBUTES))
                continue
            options[name] = value
        if len(element.children) > 0:
            self.report("E809", element, plan.stable_id, "bind", "a bind holds nothing")
        if "property" not in options or "to" not in options:
            self.report("E817", element, plan.stable_id, "bind", "a bind names its property and its source (to)")
            return
        if "converter" in options:
            self.report("E999", element, plan.stable_id, "converter", "reserved")
            return
        if "field" in options:
            self.report("E999", element, plan.stable_id, "field", "BindingSource fields are not bound from Python yet")
            return
        if IDENTIFIER.fullmatch(options["to"]) is None:
            self.report("E817", element, plan.stable_id, options["to"], "to is one identifier, the model's attribute")
            return
        mode: str = options.get("mode", "two-way")
        if mode not in BIND_MODES or options.get("update", "on-validate") not in BIND_UPDATES:
            self.report("E818", element, plan.stable_id, "mode", "mode is one-way or two-way; update on-validate "
                        "or on-change")
            return
        if options["property"] == "command":
            # The form language's Command slot, which the control schema does not list.
            self.report("E999", element, plan.stable_id, "command", "Commands are not bound from Python yet")
            return
        found: controls.Property | None = self.admitted_property(element, plan, listed, written_names,
                                                                 options["property"])
        if found is None:
            return
        if not found.bindable:
            self.report("E817", element, plan.stable_id, options["property"], "the property is not bindable")
            return
        plan.bindings.append(BindPlan(found.name, options["to"], mode == "two-way", element.line, element.column))


def walk(root: Element) -> list[Element]:
    found: list[Element] = []
    pending: list[Element] = [root]
    while len(pending) > 0:
        element: Element = pending.pop()
        found.append(element)
        pending.extend(element.children)
    return found


def read_form(document: str | bytes | pathlib.Path) -> FormPlan:
    """Reads and checks a document (a path, or its text or bytes); raises FormError with every defect found."""
    file: str = "<form>"
    encoded: bytes
    if isinstance(document, pathlib.Path):
        file = str(document)
        encoded = document.read_bytes()
    elif isinstance(document, str):
        encoded = document.encode("utf-8")
    else:
        encoded = document
    diagnostics: list[Diagnostic] = []
    root: Element | None = XmlReader(file, diagnostics).read(encoded)
    if root is None:
        raise FormError(diagnostics)
    plan: FormPlan = Checker(file, diagnostics).plan(root)
    if len(diagnostics) > 0:
        raise FormError(diagnostics)
    return plan


# ---------------------------------------------------------------- the building


def member_name(stable_id: str) -> str:
    """The attribute a stable ID is reached by: dots and hyphens become underscores ("settings.ok" -> "settings_ok")."""
    return stable_id.replace(".", "_").replace("-", "_")


class Form:
    """A built document: its objects by stable ID (``form["settings.ok"]`` or ``form.settings_ok``) and its window."""

    def __init__(self, plan: FormPlan) -> None:
        self.plan: FormPlan = plan
        self.objects: dict[str, controls.Component] = {}
        self.members: dict[str, controls.Component] = {}
        self.order: list[controls.Component] = []
        self.observations: list[binding.Observation] = []
        self.root: controls.Control | None = None
        self.window: window.Window | None = None
        self.accept_button: controls.Component | None = None
        self.cancel_button: controls.Component | None = None

    def keep(self, stable_id: str, made: controls.Component) -> None:
        self.objects[stable_id] = made
        self.members[member_name(stable_id)] = made
        self.order.append(made)

    def __getitem__(self, stable_id: str) -> controls.Component:
        return self.objects[stable_id]

    def __getattr__(self, name: str) -> controls.Component:
        members: dict[str, controls.Component] | None = self.__dict__.get("members")
        if members is not None and name in members:
            return members[name]
        raise AttributeError("the form has no object reached as " + name)

    def run(self) -> None:
        """Runs the form's window (a document whose root is ``form``)."""
        if self.window is None:
            raise RuntimeError("this document's root is a control, not a form: add it to a window")
        self.window.run()

    def release(self) -> None:
        """Ends the bindings, disposes the root and gives back every reference."""
        for observation in self.observations:
            observation.end()
        self.observations.clear()
        if self.root is not None and self.root.identity != 0:
            self.root.dispose()
        for made in reversed(self.order):
            made.release()

    def __enter__(self) -> Form:
        return self

    def __exit__(self, *unused_exception: object) -> None:
        self.release()


class Builder:
    """Makes a plan's objects; a refused value becomes an E807 at its place."""

    def __init__(self, plan: FormPlan, model: object | None) -> None:
        self.plan: FormPlan = plan
        self.model: object | None = model
        self.form: Form = Form(plan)
        self.diagnostics: list[Diagnostic] = []

    def report(self, code: str, line: int, column: int, stable_id: str, written: str, detail: str) -> None:
        self.diagnostics.append(Diagnostic(code, self.plan.file, line, column, stable_id, written, detail))

    def make(self, plan: ObjectPlan) -> controls.Component:
        made: controls.Component = plan.component_class(plan.stable_id)
        self.form.keep(plan.stable_id, made)
        for assignment in plan.assignments:
            try:
                made.set(assignment.name, assignment.value)
            except (native.GuiFormsError, ValueError, TypeError) as refused:
                self.report("E807", assignment.line, assignment.column, plan.stable_id, assignment.written,
                            str(refused))
                continue
            if isinstance(assignment.value, str) and ", " in assignment.value and \
                    made.property_info(assignment.name).kind == _abi.GF_VALUE_KIND_ENUMERATION:
                self.check_combination(made, plan, assignment)
        for bind in plan.bindings:
            self.bind(made, plan, bind)
        for child_plan in plan.children:
            child: controls.Component = self.make(child_plan)
            made.add(child)
        for component_plan in plan.components:
            self.make(component_plan)
        return made

    def check_combination(self, made: controls.Component, plan: ObjectPlan, assignment: Assignment) -> None:
        """Refuses choices combined on an enumeration that is not flags.

        The schema does not say which enumerations are flags, and the library
        stores the choices' values combined either way. Read back, a flags
        combination names every choice written; a plain enumeration gives
        another choice (top_left | top_right is top_right) or an unknown
        value.
        """
        read: object = made.get(assignment.name)
        if isinstance(read, str):
            named: set[str] = set(read.split(", "))
            written: set[str] = set(str(assignment.value).split(", "))
            if written <= named:
                return
        # The build fails and releases what it made, so the stored value is not undone.
        self.report("E807", assignment.line, assignment.column, plan.stable_id, assignment.written,
                    "the enumeration takes one choice")

    def bind(self, made: controls.Component, plan: ObjectPlan, bind: BindPlan) -> None:
        source: object = getattr(self.model, bind.source, None) if self.model is not None else None
        if not isinstance(source, binding.Value):
            self.report("E817", bind.line, bind.column, plan.stable_id, bind.source,
                        "the model has no pyguiforms.Value named " + bind.source)
            return
        try:
            made.set(bind.property_name, source.value)
        except (native.GuiFormsError, ValueError, TypeError) as refused:
            self.report("E807", bind.line, bind.column, plan.stable_id, bind.property_name, str(refused))
            return
        self.form.observations.append(source.observe(binding.PropertyWriter(made, bind.property_name)))
        if bind.two_way:
            made.on_change(bind.property_name)(binding.ValueWriter(made, bind.property_name, source))

    def build(self) -> Form:
        if self.plan.binds() and self.model is None:
            raise FormError([Diagnostic("E812", self.plan.file, 1, 1, "", "bind",
                                        "the document binds values: pass its model")])
        assert self.plan.root is not None
        root: controls.Component = self.make(self.plan.root)
        self.form.root = root
        for component_plan in self.plan.components:
            self.make(component_plan)
        if len(self.diagnostics) > 0:
            self.form.release()
            raise FormError(self.diagnostics)
        if self.plan.window_id is not None:
            width: float = 640.0 if self.plan.client_size is None else self.plan.client_size.width
            height: float = 480.0 if self.plan.client_size is None else self.plan.client_size.height
            self.form.window = window.Window(self.plan.title, width, height, root=root)
        if self.plan.accept_button is not None:
            self.form.accept_button = self.form.objects[self.plan.accept_button]
        if self.plan.cancel_button is not None:
            self.form.cancel_button = self.form.objects[self.plan.cancel_button]
        return self.form


def build_form(plan: FormPlan, model: object | None = None) -> Form:
    """Makes a checked plan's objects, properties and bindings; raises FormError for a value the library refuses."""
    built: Form = Builder(plan, model).build()
    return built


def load_form(document: str | bytes | pathlib.Path, model: object | None = None) -> Form:
    """Reads, checks and builds a document. A ``str`` that names an existing ``.form`` file is read from it."""
    source: str | bytes | pathlib.Path = document
    if isinstance(document, str) and document.endswith(".form") and "<" not in document:
        source = pathlib.Path(document)
    plan: FormPlan = read_form(source)
    built: Form = build_form(plan, model)
    return built


__all__: list[str] = ["Diagnostic", "Form", "FormError", "FormPlan", "build_form", "load_form", "read_form"]

