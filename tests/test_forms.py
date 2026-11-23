"""Form documents: the reader and checker need no library; building them does."""

from __future__ import annotations

import pathlib
import unittest

import pyguiforms
from pyguiforms import forms
from pyguiforms import native
from pyguiforms import values

LIBRARY_PRESENT: bool = native.find_library().is_file()
EXAMPLE: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent / "examples" / "forms" / "settings.form"
HEAD: str = '<?xml version="1.0" encoding="UTF-8"?>\n'


def document(body: str, root_attributes: str = "") -> str:
    """A form whose root panel holds body."""
    return (HEAD + '<form xmlns="urn:gui-forms:form:1" id="t.window" text="T" client-size="200 100"' +
            root_attributes + '>\n<panel id="t.root">\n' + body + '\n</panel>\n</form>\n')


def refusal_codes(text: str) -> list[str]:
    try:
        forms.read_form(text)
    except forms.FormError as refused:
        return refused.codes()
    return []


class Model:
    def __init__(self) -> None:
        self.autosave: pyguiforms.Value = pyguiforms.Value(True)


class ReaderTests(unittest.TestCase):

    def test_the_example_reads(self) -> None:
        plan: forms.FormPlan = forms.read_form(EXAMPLE)
        self.assertEqual(plan.window_id, "settings.window")
        self.assertEqual(plan.title, "Settings")
        self.assertEqual(plan.client_size, values.Size(360.0, 150.0))
        self.assertEqual(plan.accept_button, "settings.ok")
        assert plan.root is not None
        self.assertEqual(len(plan.root.children), 3)
        self.assertEqual(plan.root.children[0].bindings[0].source, "autosave")

    def test_values_by_kind(self) -> None:
        plan: forms.FormPlan = forms.read_form(document(
            '<button id="t.b" text="a &amp; b" bounds="1 2 3 4" enabled="false" tab-index="3" '
            'text-alignment="middle-center" padding="4 8" anchor="top right"/>'
            '<list-box id="t.l" items="AM FM \'Wide FM\' \'tab\\there\'"/>'))
        assert plan.root is not None
        assigned: dict[str, object] = {}
        for assignment in plan.root.children[0].assignments:
            assigned[assignment.name] = assignment.value
        self.assertEqual(assigned["text"], "a & b")
        self.assertEqual(assigned["bounds"], values.Rect(1.0, 2.0, 3.0, 4.0))
        self.assertIs(assigned["enabled"], False)
        self.assertEqual(assigned["tab_index"], 3)
        self.assertEqual(assigned["text_alignment"], "middle_center")
        self.assertEqual(assigned["padding"], values.Insets(8.0, 4.0, 8.0, 4.0))
        self.assertEqual(assigned["anchor"], "top, right")
        self.assertEqual(plan.root.children[1].assignments[0].value, ["AM", "FM", "Wide FM", "tab\there"])

    def test_every_defect_is_reported_together(self) -> None:
        codes: list[str] = refusal_codes(document(
            '<button id="t.b" no-such="1"/>'
            '<button id="t.b" text="again"/>'
            '<no-such-type id="t.x"/>'
            '<button id="t.c" fore-color="#fff"/>'
            '<button id="t.d" on-click="handler"/>'
            '<button id="t.e" layout-direction="yes"/>'
            '<button id="t.f" enabled="maybe"/>'
            '<button text="no id"/>'
            '<style id="t.s"/>'))
        self.assertEqual(codes, ["E804", "E803", "E802", "E813", "E816", "E820", "E807", "E801", "E810"])

    def test_bindings_are_checked(self) -> None:
        codes: list[str] = refusal_codes(document(
            '<check-box id="t.a"><bind property="checked"/></check-box>'
            '<check-box id="t.b"><bind property="checked" to="not an identifier"/></check-box>'
            '<check-box id="t.c"><bind property="checked" to="x" colour="red"/></check-box>'
            '<check-box id="t.d"><bind property="checked" to="x" field="name"/></check-box>'
            '<check-box id="t.e" checked="true"><bind property="checked" to="x"/></check-box>'
            '<button id="t.f"><bind property="command" to="accept"/></button>'))
        self.assertEqual(codes, ["E817", "E817", "E818", "E999", "E806", "E999"])

    def test_the_xml_subset(self) -> None:
        self.assertEqual(refusal_codes(HEAD + '<!DOCTYPE form [<!ENTITY a "b">]><form/>'), ["E821"])
        self.assertEqual(refusal_codes('<form xmlns="urn:gui-forms:form:1" id="w"><![CDATA[x]]></form>'),
                         ["E821"])
        self.assertEqual(refusal_codes('<form id="w"><panel id="p"/></form>'), ["E821"])
        self.assertEqual(refusal_codes(document('text')), ["E821"])
        self.assertEqual(refusal_codes("<form"), ["E821"])

    def test_a_form_holds_one_control_and_its_buttons_exist(self) -> None:
        two_roots: str = (HEAD + '<form xmlns="urn:gui-forms:form:1" id="w"><panel id="a"/><panel id="b"/>'
                          '<command id="c"/></form>')
        self.assertEqual(refusal_codes(two_roots), ["E801"])
        self.assertEqual(refusal_codes(document("", ' accept-button="t.none"')), ["E807"])

    def test_bounds(self) -> None:
        deep: str = '<panel id="d0">'
        for level in range(1, forms.MAXIMUM_DEPTH + 2):
            deep += '<panel id="d' + str(level) + '">'
        self.assertEqual(refusal_codes(HEAD + '<panel xmlns="urn:gui-forms:form:1" id="r">' + deep), ["E821"])
        self.assertEqual(refusal_codes(b" " * (forms.MAXIMUM_DOCUMENT_BYTES + 1)), ["E821"])

    def test_member_names(self) -> None:
        self.assertEqual(forms.member_name("settings.ok-button"), "settings_ok_button")


@unittest.skipUnless(LIBRARY_PRESENT, "no gui_forms_abi1 library (set GUI_FORMS_ABI_LIBRARY)")
class BuildTests(unittest.TestCase):

    def test_the_example_builds_and_binds(self) -> None:
        model: Model = Model()
        with pyguiforms.load_form(EXAMPLE, model=model) as form:
            self.assertIsNotNone(form.window)
            self.assertIs(form.settings_autosave.checked, True)
            model.autosave.value = False
            self.assertIs(form.settings_autosave.checked, False)
            form.settings_autosave.checked = True
            self.assertIs(model.autosave.value, True)
            self.assertIs(form.accept_button, form["settings.ok"])
            self.assertEqual(form.settings_status.text, "Not saved yet.")

    def test_a_missing_model_is_refused(self) -> None:
        with self.assertRaises(forms.FormError) as refused:
            pyguiforms.load_form(EXAMPLE)
        self.assertEqual(refused.exception.codes(), ["E812"])

    def test_a_value_the_library_refuses_is_e807(self) -> None:
        plan: forms.FormPlan = forms.read_form(document('<button id="t.b" text-alignment="top-left top-right"/>'))
        with self.assertRaises(forms.FormError) as refused:
            forms.build_form(plan)
        self.assertEqual(refused.exception.codes(), ["E807"])


if __name__ == "__main__":
    unittest.main()
