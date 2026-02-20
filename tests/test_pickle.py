import pickle
from copy import copy
from copy import deepcopy

from jinja2 import Environment
from jinja2 import Template


def test_environment(env):
    env = pickle.loads(pickle.dumps(env))
    assert env.from_string("x={{ x }}").render(x=42) == "x=42"


def test_template_copy():
    t = Template("{{ foo }}")
    t_copy = copy(t)
    assert t_copy is t
    assert t_copy.render(foo="bar") == "bar"


def test_template_deepcopy():
    t = Template("{{ foo }}")
    t_copy = deepcopy(t)
    assert t_copy is t
    assert t_copy.render(foo="bar") == "bar"


def test_template_deepcopy_in_container():
    """Deepcopy of an object containing a template should not raise."""
    t = Template("{{ foo }}")
    container = {"template": t, "data": [1, 2, 3]}
    container_copy = deepcopy(container)
    assert container_copy["template"] is t
    assert container_copy["data"] is not container["data"]
    assert container_copy["template"].render(foo="bar") == "bar"


def test_environment_template_copy():
    env = Environment()
    t = env.from_string("{{ x }}")
    assert copy(t) is t
    assert deepcopy(t) is t
    assert t.render(x=42) == "42"
