import re
import shutil
from pathlib import Path

import pytest

from deepwick_spec.ansi import runs, style_of
from deepwick_spec.check_port import check_port
from deepwick_spec.palette import ANSI_KEYS, load_palette
from deepwick_spec.tui import capture, tmux_available

REPO = Path(__file__).resolve().parents[1]
PALETTE = load_palette()
C = PALETTE.colors


def isolated_env(tmp_path, **extra):
    dirs = {"HOME": tmp_path / "home"}
    for kind in ("CONFIG", "DATA", "STATE", "CACHE"):
        dirs[f"XDG_{kind}_HOME"] = tmp_path / kind.lower()
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    env = {key: str(path) for key, path in dirs.items()}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")
    env.update({key: str(value) for key, value in extra.items()})
    return env


THEME = REPO / "deepwick.xsh"
renders = pytest.mark.skipif(not (tmux_available() and shutil.which("xonsh")), reason="requires tmux and xonsh")
EXPECTED = {
    "Token.Comment": "italic #7A86A8", "Token.Keyword": "#569CD6", "Token.Keyword.Namespace": "#C586C0",
    "Token.Name.Builtin": "#DCDCAA", "Token.Name.Function": "#DCDCAA", "Token.Name.Class": "#4EC9B0",
    "Token.Name.Variable": "#9CDCFE", "Token.String": "#CE9178", "Token.String.Escape": "#D7BA7D",
    "Token.String.Regex": "#D16969", "Token.Number": "#B5CEA8", "Token.Error": "#F44747",
    "Token.Operator": "#D4D4D4", "Token.Operator.Word": "#569CD6", "Token.Text": "#D4D4D4",
    "completion-menu.completion.current": "noreverse bg:#264F78 #D4D4D4",
}
ANSI_NAMES = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "PURPLE", "CYAN", "WHITE"]


def styles():
    assert THEME.is_file(), "deepwick.xsh missing"
    return dict(re.findall(r'^\s*"([^"]+)":\s*"([^"]*)",\s*$', THEME.read_text(encoding="utf-8"), re.M))


def test_role_styles():
    s = styles()
    for key, value in EXPECTED.items():
        assert s[key] == value, key


def test_ansi_color_names_use_deepwick_slots():
    s = styles()
    names = ANSI_NAMES + [f"INTENSE_{n}" for n in ANSI_NAMES]
    for name, key in zip(names, ANSI_KEYS):
        assert s[f"Color.{name}"] == PALETTE.ansi[key], name


def xonsh_command(tmp_path):
    rc = tmp_path / "rc.xsh"
    rc.write_text(
        "$XONSH_HISTORY_BACKEND = 'dummy'\n"
        "$XONSH_SUPPRESS_WELCOME = True\n"
        "$PROMPT = 'xonsh> '\n"
        "$RIGHT_PROMPT = ''\n"
        "$UPDATE_COMPLETIONS_ON_KEYPRESS = False\n"
        f"source {THEME}\n"
    )
    return f"xonsh --rc {rc} -i"


@renders
def test_xonsh_highlights_subprocess_line(tmp_path):
    text = capture(xonsh_command(tmp_path), isolated_env(tmp_path), wait_for="xonsh>", literal='echo "hi" 42 # note')
    assert style_of(text, "echo")["fg"] == C["yellow"].lower()
    assert style_of(text, '"hi"')["fg"] == C["orange"].lower()
    comment = style_of(text, "# note")
    assert comment["fg"] == C["comment"].lower() and comment["italic"]


@renders
def test_xonsh_highlights_python_line(tmp_path):
    text = capture(xonsh_command(tmp_path), isolated_env(tmp_path), wait_for="xonsh>", literal="for x in range(3): pass")
    assert style_of(text, "for")["fg"] == C["blue"].lower()
    assert style_of(text, "range")["fg"] == C["yellow"].lower()
    word = style_of(text, "in")
    assert word["fg"] == C["blue"].lower() and not word["bold"]
    assert style_of(text, "3")["fg"] == C["sage"].lower()


@renders
def test_xonsh_uses_24_bit_color(tmp_path):
    text = capture(xonsh_command(tmp_path), isolated_env(tmp_path), wait_for="xonsh>", literal="echo hi")
    assert any(s["fg"] == C["yellow"].lower() for _, s in runs(text))


def test_port_conventions():
    assert check_port(REPO, PALETTE.allowed_hex()) == []
