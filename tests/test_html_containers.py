import unittest

from src.completescraper.parser.html_containers import (
    HtmlContainer,
    HtmlForm,
    HtmlOl,
    HtmlSelect,
    HtmlUl,
)


class TestHtmlContainer(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <form name="test_form">
            <input name="input1" value="value1"/>
            <input name="input2" value="value2"/>
        </form>
        """

    def test_html_containers_bool(self) -> None:
        self.assertFalse(HtmlContainer("", "form", "input"))
        self.assertTrue(
            HtmlContainer(
                self.html,
                "form",
                "input",
                "test_form",
                0,
                "name",
                "name",
                "value",
            )
        )

    def test_html_containers_parse(self) -> None:
        self.assertEqual(
            HtmlContainer(
                self.html,
                "form",
                "input",
                "test_form",
                0,
                "name",
                "name",
                "value",
            ),
            HtmlContainer(
                name="test_form", children={"input1": "value1", "input2": "value2"}
            ),
        )


class TestHtmlFormBasic(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <form name="test_form">
            <input name="input1" value="value1"/>
            <input name="input2" value="value2"/>
        </form>
        """

    def test_html_form_basic(self) -> None:
        self.assertEqual(
            HtmlForm(self.html, "test_form"),
            HtmlForm(
                name="test_form", children={"input1": "value1", "input2": "value2"}
            ),
        )
        self.assertEqual(
            HtmlForm(self.html, "test_form", 0),
            HtmlForm(
                name="test_form", children={"input1": "value1", "input2": "value2"}
            ),
        )
        self.assertEqual(
            HtmlForm(self.html, "test_form", form_id_attr="name"),
            HtmlForm(
                name="test_form", children={"input1": "value1", "input2": "value2"}
            ),
        )
        self.assertEqual(
            HtmlForm(self.html, "test_form", input_value_attr="value"),
            HtmlForm(
                name="test_form", children={"input1": "value1", "input2": "value2"}
            ),
        )
        self.assertEqual(
            HtmlForm(self.html, "test_form", 0, "name", "name", "value"),
            HtmlForm(
                name="test_form", children={"input1": "value1", "input2": "value2"}
            ),
        )
        self.assertNotEqual(
            HtmlForm(self.html, "test_form", 0, "name", "name", "value"),
            HtmlForm(
                name="test_form", children={"input1": "value1", "input3": "value3"}
            ),
        )


class TestHtmlFormMultiple(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <html>
        <form name="test_form">
            <input name="input1" value="value1"/>
            <input name="input2" value="value2"/>
        </form>
        <form name="my_form">
            <input name="input3" value="value3"/>
            <input name="input4" value="value4"/>
        </form>
        <form name="my_form">
            <input name="input5" value="value5"/>
            <input name="input6" value="value6"/>
        </form>
        </html>
        """

    def test_html_form_multiple(self) -> None:
        self.assertEqual(
            HtmlForm(self.html, "my_form"),
            HtmlForm(name="my_form", children={"input3": "value3", "input4": "value4"}),
        )
        self.assertEqual(
            HtmlForm(self.html, "my_form", 0),
            HtmlForm(name="my_form", children={"input3": "value3", "input4": "value4"}),
        )
        self.assertEqual(
            HtmlForm(self.html, "my_form", 1),
            HtmlForm(name="my_form", children={"input5": "value5", "input6": "value6"}),
        )
        self.assertEqual(
            HtmlForm(self.html, form_position=1),
            HtmlForm(name="my_form", children={"input3": "value3", "input4": "value4"}),
        )
        self.assertEqual(
            HtmlForm(self.html, "my_form", form_id_attr="name", form_position=1),
            HtmlForm(name="my_form", children={"input5": "value5", "input6": "value6"}),
        )
        self.assertEqual(
            HtmlForm(self.html, "test_form", input_value_attr="value").children[
                "input1"
            ],
            "value1",
        )
        self.assertEqual(
            HtmlForm(self.html, "my_form", 0, "name", "name", "value").name, "my_form"
        )
        self.assertNotEqual(
            HtmlForm(
                self.html,
                form_position=0,
                form_id_attr="name",
                input_id_attr="name",
                input_value_attr="value",
            ),
            HtmlForm(
                name="test_form", children={"input1": "value1", "input3": "value3"}
            ),
        )


class TestHtmlSelectBasic(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <select name="test_select">
            <option name="option1" value="value1">VALUE1</option>
            <option name="option2" value="value2">VALUE2</option>
        </select>
        """

    def test_html_select_basic(self) -> None:
        self.assertEqual(
            HtmlSelect(self.html, "test_select"),
            HtmlSelect(
                name="test_select", children={"option1": "value1", "option2": "value2"}
            ),
        )
        self.assertEqual(
            HtmlSelect(self.html, "test_select", 0),
            HtmlSelect(
                name="test_select", children={"option1": "value1", "option2": "value2"}
            ),
        )
        self.assertEqual(
            HtmlSelect(self.html, "test_select", select_id_attr="name"),
            HtmlSelect(
                name="test_select", children={"option1": "value1", "option2": "value2"}
            ),
        )
        self.assertEqual(
            HtmlSelect(self.html, "test_select", option_value_attr="value"),
            HtmlSelect(
                name="test_select", children={"option1": "value1", "option2": "value2"}
            ),
        )
        self.assertEqual(
            HtmlSelect(self.html, "test_select", 0, "name", "name", "value"),
            HtmlSelect(
                name="test_select", children={"option1": "value1", "option2": "value2"}
            ),
        )
        self.assertNotEqual(
            HtmlSelect(self.html, "test_select", 0, "name", "name", "value"),
            HtmlSelect(
                name="test_select", children={"option1": "value1", "option3": "value3"}
            ),
        )


class TestHtmlSelectMultiple(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <html>
        <select name="test_select">
            <option name="option1" value="value1">VALUE1</option>
            <option name="option2" value="value2">VALUE2</option>
        </select>
        <select name="my_select">
            <option name="option3" value="value3">VALUE3</option>
            <option name="option4" value="value4">VALUE4</option>
        </select>
        <select name="my_select">
            <option name="option5" value="value5">VALUE5</option>
            <option name="option6" value="value6">VALUE6</option>
        </select>
        </html>
        """

    def test_html_select_multiple(self) -> None:
        self.assertEqual(
            HtmlSelect(self.html, "my_select"),
            HtmlSelect(
                name="my_select", children={"option3": "value3", "option4": "value4"}
            ),
        )
        self.assertEqual(
            HtmlSelect(self.html, "my_select", 0),
            HtmlSelect(
                name="my_select", children={"option3": "value3", "option4": "value4"}
            ),
        )
        self.assertEqual(
            HtmlSelect(self.html, "my_select", 1),
            HtmlSelect(
                name="my_select", children={"option5": "value5", "option6": "value6"}
            ),
        )
        self.assertEqual(
            HtmlSelect(self.html, select_position=1),
            HtmlSelect(
                name="my_select", children={"option3": "value3", "option4": "value4"}
            ),
        )
        self.assertEqual(
            HtmlSelect(self.html, select_position=1, option_value_attr=None),
            HtmlSelect(
                name="my_select", children={"option3": "VALUE3", "option4": "VALUE4"}
            ),
        )
        self.assertEqual(
            HtmlSelect(
                self.html,
                "my_select",
                select_id_attr="name",
                select_position=1,
                option_value_attr=None,
            ),
            HtmlSelect(
                name="my_select", children={"option5": "VALUE5", "option6": "VALUE6"}
            ),
        )
        self.assertEqual(
            HtmlSelect(self.html, "test_select", option_value_attr="value").children[
                "option1"
            ],
            "value1",
        )
        self.assertEqual(
            HtmlSelect(self.html, "my_select", 0, "name", "name", "value").name,
            "my_select",
        )
        self.assertNotEqual(
            HtmlSelect(
                self.html,
                select_position=0,
                select_id_attr="name",
                option_id_attr="name",
                option_value_attr="value",
            ),
            HtmlForm(
                name="test_select", children={"option1": "value1", "option3": "value3"}
            ),
        )


class TestHtmlUlBasic(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <ul name="test_ul">
            <li name="li1" value="value1">VALUE1<a>OTHER VALUE1</a></li>
            <li name="li2" value="value2">VALUE2
            OTHER VALUE2</li>
        </ul>
        """

    def test_html_ul_basic(self) -> None:
        self.assertEqual(
            HtmlUl(self.html, "test_ul"),
            HtmlUl(
                name="test_ul",
                children={
                    "li1": "VALUE1 OTHER VALUE1",
                    "li2": "VALUE2\n            OTHER VALUE2",
                },
            ),
        )
        self.assertEqual(
            HtmlUl(self.html, "test_ul", 0),
            HtmlUl(
                name="test_ul",
                children={
                    "li1": "VALUE1 OTHER VALUE1",
                    "li2": "VALUE2\n            OTHER VALUE2",
                },
            ),
        )
        self.assertEqual(
            HtmlUl(self.html, "test_ul", ul_id_attr="name"),
            HtmlUl(
                name="test_ul",
                children={
                    "li1": "VALUE1 OTHER VALUE1",
                    "li2": "VALUE2\n            OTHER VALUE2",
                },
            ),
        )
        self.assertEqual(
            HtmlUl(self.html, "test_ul", li_value_attr="value"),
            HtmlUl(name="test_ul", children={"li1": "value1", "li2": "value2"}),
        )
        self.assertEqual(
            HtmlUl(self.html, "test_ul", 0, "name", "name", "value"),
            HtmlUl(name="test_ul", children={"li1": "value1", "li2": "value2"}),
        )
        self.assertNotEqual(
            HtmlUl(self.html, "test_ul", 0, "name", "name", "value"),
            HtmlUl(name="test_ul", children={"li1": "value1", "li3": "value3"}),
        )


class TestHtmlUlMultiple(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <html>
        <ul name="test_ul">
            <li name="li1" value="value1">VALUE1</li>
            <li name="li2" value="value2">VALUE2</li>
        </ul>
        <ul name="my_ul">
            <li name="li3" value="value3">VALUE3</li>
            <li name="li4" value="value4">VALUE4</li>
        </ul>
        <ul name="my_ul">
            <li name="li5" value="value5">VALUE5</li>
            <li name="li6" value="value6">VALUE6</li>
        </ul>
        </html>
        """

    def test_html_ul_multiple(self) -> None:
        self.assertEqual(
            HtmlUl(self.html, "my_ul"),
            HtmlUl(name="my_ul", children={"li3": "VALUE3", "li4": "VALUE4"}),
        )
        self.assertEqual(
            HtmlUl(self.html, "my_ul", 0),
            HtmlUl(name="my_ul", children={"li3": "VALUE3", "li4": "VALUE4"}),
        )
        self.assertEqual(
            HtmlUl(self.html, "my_ul", 1),
            HtmlUl(name="my_ul", children={"li5": "VALUE5", "li6": "VALUE6"}),
        )
        self.assertEqual(
            HtmlUl(self.html, ul_position=1),
            HtmlUl(name="my_ul", children={"li3": "VALUE3", "li4": "VALUE4"}),
        )
        self.assertEqual(
            HtmlUl(self.html, ul_position=1, li_value_attr=None),
            HtmlUl(name="my_ul", children={"li3": "VALUE3", "li4": "VALUE4"}),
        )
        self.assertEqual(
            HtmlUl(self.html, ul_position=1, li_value_attr="value"),
            HtmlUl(name="my_ul", children={"li3": "value3", "li4": "value4"}),
        )
        self.assertEqual(
            HtmlUl(
                self.html,
                "my_ul",
                ul_id_attr="name",
                ul_position=1,
                li_value_attr=None,
            ),
            HtmlUl(name="my_ul", children={"li5": "VALUE5", "li6": "VALUE6"}),
        )
        self.assertEqual(
            HtmlUl(self.html, "test_ul", li_value_attr="value").children["li1"],
            "value1",
        )
        self.assertEqual(
            HtmlUl(self.html, "my_ul", 0, "name", "name", "value").name,
            "my_ul",
        )
        self.assertNotEqual(
            HtmlUl(
                self.html,
                ul_position=0,
                ul_id_attr="name",
                li_id_attr="name",
                li_value_attr="value",
            ),
            HtmlForm(name="test_ul", children={"li1": "value1", "li3": "value3"}),
        )


class TestHtmlOlBasic(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <ol name="test_ol">
            <li name="li1" value="value1">VALUE1</li>
            <li name="li2" value="value2">VALUE2</li>
        </ol>
        """

    def test_html_ol_basic(self) -> None:
        self.assertEqual(
            HtmlOl(self.html, "test_ol"),
            HtmlOl(name="test_ol", children={"li1": "VALUE1", "li2": "VALUE2"}),
        )
        self.assertEqual(
            HtmlOl(self.html, "test_ol", 0),
            HtmlOl(name="test_ol", children={"li1": "VALUE1", "li2": "VALUE2"}),
        )
        self.assertEqual(
            HtmlOl(self.html, "test_ol", ol_id_attr="name"),
            HtmlOl(name="test_ol", children={"li1": "VALUE1", "li2": "VALUE2"}),
        )
        self.assertEqual(
            HtmlOl(self.html, "test_ol", li_value_attr="value"),
            HtmlOl(name="test_ol", children={"li1": "value1", "li2": "value2"}),
        )
        self.assertEqual(
            HtmlOl(self.html, "test_ol", 0, "name", "name", "value"),
            HtmlOl(name="test_ol", children={"li1": "value1", "li2": "value2"}),
        )
        self.assertNotEqual(
            HtmlOl(self.html, "test_ol", 0, "name", "name", "value"),
            HtmlOl(name="test_ol", children={"li1": "value1", "li3": "value3"}),
        )


class TestHtmlOlMultiple(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <html>
        <ol name="test_ol">
            <li name="li1" value="value1">VALUE1</li>
            <li name="li2" value="value2">VALUE2</li>
        </ol>
        <ol name="my_ol">
            <li name="li3" value="value3">VALUE3</li>
            <li name="li4" value="value4">VALUE4</li>
        </ol>
        <ol name="my_ol">
            <li name="li5" value="value5">VALUE5</li>
            <li name="li6" value="value6">VALUE6</li>
        </ol>
        </html>
        """

    def test_html_ol_multiple(self) -> None:
        self.assertEqual(
            HtmlOl(self.html, "my_ol"),
            HtmlOl(name="my_ol", children={"li3": "VALUE3", "li4": "VALUE4"}),
        )
        self.assertEqual(
            HtmlOl(self.html, "my_ol", 0),
            HtmlOl(name="my_ol", children={"li3": "VALUE3", "li4": "VALUE4"}),
        )
        self.assertEqual(
            HtmlOl(self.html, "my_ol", 1),
            HtmlOl(name="my_ol", children={"li5": "VALUE5", "li6": "VALUE6"}),
        )
        self.assertEqual(
            HtmlOl(self.html, ol_position=1),
            HtmlOl(name="my_ol", children={"li3": "VALUE3", "li4": "VALUE4"}),
        )
        self.assertEqual(
            HtmlOl(self.html, ol_position=1, li_value_attr=None),
            HtmlOl(name="my_ol", children={"li3": "VALUE3", "li4": "VALUE4"}),
        )
        self.assertEqual(
            HtmlOl(self.html, ol_position=1, li_value_attr="value"),
            HtmlOl(name="my_ol", children={"li3": "value3", "li4": "value4"}),
        )
        self.assertEqual(
            HtmlOl(
                self.html,
                "my_ol",
                ol_id_attr="name",
                ol_position=1,
                li_value_attr=None,
            ),
            HtmlOl(name="my_ol", children={"li5": "VALUE5", "li6": "VALUE6"}),
        )
        self.assertEqual(
            HtmlOl(self.html, "test_ol", li_value_attr="value").children["li1"],
            "value1",
        )
        self.assertEqual(
            HtmlOl(self.html, "my_ol", 0, "name", "name", "value").name,
            "my_ol",
        )
        self.assertNotEqual(
            HtmlOl(
                self.html,
                ol_position=0,
                ol_id_attr="name",
                li_id_attr="name",
                li_value_attr="value",
            ),
            HtmlForm(name="test_ol", children={"li1": "value1", "li3": "value3"}),
        )


class TestHtmlContainerMultipleClasses(unittest.TestCase):
    def setUp(self) -> None:
        self.html = """
        <div id="div1">
            <a class="class1 class3" value="value1">VALUE1</a>
            <a class="class2" value="value2">VALUE2</a>
        </div>
        """

    def test_html_container_multiple_classes(self) -> None:
        print(HtmlContainer(self.html, "div", "a", "div1", 0, "id", "class", None))
        self.assertEqual(
            HtmlContainer(self.html, "div", "a", "div1", 0, "id", "class", None),
            HtmlContainer(
                name="div1", children={"class1 class3": "VALUE1", "class2": "VALUE2"}
            ),
        )


if __name__ == "__main__":
    unittest.main()
