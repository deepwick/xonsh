# Deepwick for xonsh. Source from ~/.xonshrc or put in ~/.config/xonsh/rc.d/.
from xonsh.tools import register_custom_style as _deepwick_register

_deepwick_styles = {
    "Token.Text": "#D4D4D4",
    "Token.Text.Whitespace": "#D4D4D4",
    "Token.Name": "#D4D4D4",
    "Token.Punctuation": "#D4D4D4",
    "Token.Operator": "#D4D4D4",
    "Token.Operator.Word": "#569CD6",
    "Token.Comment": "italic #7A86A8",
    "Token.Keyword": "#569CD6",
    "Token.Keyword.Constant": "#569CD6",
    "Token.Keyword.Namespace": "#C586C0",
    "Token.Name.Builtin": "#DCDCAA",
    "Token.Name.Function": "#DCDCAA",
    "Token.Name.Decorator": "#DCDCAA",
    "Token.Name.Class": "#4EC9B0",
    "Token.Name.Namespace": "#4EC9B0",
    "Token.Name.Constant": "#4FC1FF",
    "Token.Name.Variable": "#9CDCFE",
    "Token.String": "#CE9178",
    "Token.String.Affix": "#569CD6",
    "Token.String.Escape": "#D7BA7D",
    "Token.String.Interpol": "#9CDCFE",
    "Token.String.Regex": "#D16969",
    "Token.String.Backtick": "#D7BA7D",
    "Token.Number": "#B5CEA8",
    "Token.Error": "#F44747",
    "Color.BLACK": "#1B2140",
    "Color.RED": "#F44747",
    "Color.GREEN": "#57A64A",
    "Color.YELLOW": "#DCDCAA",
    "Color.BLUE": "#569CD6",
    "Color.PURPLE": "#C586C0",
    "Color.CYAN": "#4EC9B0",
    "Color.WHITE": "#D4D4D4",
    "Color.INTENSE_BLACK": "#6E7899",
    "Color.INTENSE_RED": "#FF7A7A",
    "Color.INTENSE_GREEN": "#7FC46E",
    "Color.INTENSE_YELLOW": "#F2F2C4",
    "Color.INTENSE_BLUE": "#9CDCFE",
    "Color.INTENSE_PURPLE": "#E0A8DC",
    "Color.INTENSE_CYAN": "#7FE5CF",
    "Color.INTENSE_WHITE": "#FFFFFF",
    "completion-menu": "bg:#10192C #D4D4D4",
    "completion-menu.completion.current": "noreverse bg:#264F78 #D4D4D4",
}

_deepwick_register("deepwick", _deepwick_styles, background_color="#04041a", highlight_color="#264F78")
$XONSH_COLOR_STYLE = "deepwick"
if ${...}.get("COLORTERM", "") in ("truecolor", "24bit"):
    $PROMPT_TOOLKIT_COLOR_DEPTH = "DEPTH_24_BIT"
del _deepwick_register, _deepwick_styles
