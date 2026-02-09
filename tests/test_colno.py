"""Tests for column number tracking in AST nodes."""

from jinja2 import Environment
from jinja2 import nodes


class TestColno:
    """Test that AST nodes track column numbers correctly."""

    def setup_method(self):
        self.env = Environment()

    def test_simple_variable(self):
        t = self.env.parse("{{ foo }}")
        names = list(t.find_all(nodes.Name))
        assert len(names) == 1
        assert names[0].name == "foo"
        assert names[0].lineno == 1
        assert names[0].colno == 4

    def test_multiple_variables_same_line(self):
        t = self.env.parse("{{ foo }} {{ bar }}")
        names = list(t.find_all(nodes.Name))
        assert len(names) == 2
        assert names[0].name == "foo"
        assert names[0].colno == 4
        assert names[1].name == "bar"
        assert names[1].colno == 14

    def test_multiline(self):
        t = self.env.parse("{{ foo }}\n{{ bar }}")
        names = list(t.find_all(nodes.Name))
        assert names[0].lineno == 1
        assert names[0].colno == 4
        assert names[1].lineno == 2
        assert names[1].colno == 4

    def test_expression_colno(self):
        t = self.env.parse("{{ a + b }}")
        names = list(t.find_all(nodes.Name))
        assert names[0].name == "a"
        assert names[0].colno == 4
        assert names[1].name == "b"
        assert names[1].colno == 8

    def test_for_loop_colno(self):
        t = self.env.parse("{% for x in items %}{% endfor %}")
        for_node = t.find(nodes.For)
        assert for_node is not None
        assert for_node.lineno == 1

    def test_if_colno(self):
        t = self.env.parse("{% if true %}yes{% endif %}")
        if_node = t.find(nodes.If)
        assert if_node is not None
        assert if_node.lineno == 1

    def test_const_colno(self):
        t = self.env.parse('{{ "hello" }}')
        consts = list(t.find_all(nodes.Const))
        assert consts[0].colno == 4

    def test_integer_colno(self):
        t = self.env.parse("{{ 42 }}")
        consts = list(t.find_all(nodes.Const))
        assert consts[0].colno == 4

    def test_set_colno(self):
        """Test the set_colno helper method."""
        t = self.env.parse("{{ foo }}")
        name = t.find(nodes.Name)
        assert name is not None
        name.set_colno(10, override=True)
        assert name.colno == 10

    def test_colno_default_none(self):
        """Nodes created without colno should have None."""
        node = nodes.Name("test", "load", lineno=1)
        assert node.colno is None

    def test_multiline_block(self):
        t = self.env.parse("line1\n  {{ x }}")
        names = list(t.find_all(nodes.Name))
        assert names[0].name == "x"
        assert names[0].lineno == 2
        assert names[0].colno == 6

    def test_token_colno(self):
        """Test that tokens carry column numbers."""
        from jinja2.lexer import get_lexer

        lexer = get_lexer(self.env)
        stream = lexer.tokenize("{{ foo }}")
        tokens = list(stream)
        # Find the 'foo' name token
        name_tokens = [t for t in tokens if t.type == "name"]
        assert len(name_tokens) == 1
        assert name_tokens[0].value == "foo"
        assert name_tokens[0].colno == 4
