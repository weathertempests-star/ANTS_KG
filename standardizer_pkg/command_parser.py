"""Conservative command surface syntax, never execution or shell expansion.

Spans index Python Unicode characters in the exact original string. ``value``
only removes a matching pair of enclosing quotes; it is NOT an argv value.
Windows quoting varies by executable; POSIX expansions, substitutions, comments,
here-documents and nested shells are deliberately not interpreted. Relations
describe surface syntax, not execution, data flow, or causality.
"""

import re


OPERATORS = ("&&", "||", ">>", "<<", "|", ";", "&", ">", "<", "(", ")")
REG_SUBCOMMANDS = {"query", "add", "delete", "copy", "save", "restore", "load", "unload", "compare", "export", "import", "flags"}
# /ve, /f and /reg:* are flags; /s takes a separator only for REG ADD.
REG_BOUND_OPTIONS = {
    "query": {"/v", "/f", "/t", "/se"},
    "add": {"/v", "/t", "/d", "/s"},
    "delete": {"/v"},
    "compare": {"/v"},
}


def _lex(text, dialect):
    tokens, warnings = [], []
    i = 0
    while i < len(text):
        if text[i].isspace():
            i += 1
            continue
        start = i
        op = next((op for op in OPERATORS if text.startswith(op, i)), None)
        if op:
            i += len(op)
            tokens.append({"raw": op, "start": start, "end": i, "value": op,
                           "role": "command_operator"})
            continue
        quote = None
        while i < len(text):
            char = text[i]
            if dialect == "posix" and char == "\\" and quote != "'" and i + 1 < len(text):
                i += 2
                continue
            if dialect == "windows" and char == "\\":
                end = i
                while end < len(text) and text[end] == "\\":
                    end += 1
                if end < len(text) and text[end] == '"' and (end - i) % 2:
                    i = end + 1
                    continue
            quote_chars = "\"'" if dialect == "posix" else '"'
            if char in quote_chars:
                if quote == char:
                    quote = None
                elif quote is None:
                    quote = char
                i += 1
                continue
            if quote is None and (char.isspace() or any(text.startswith(op, i) for op in OPERATORS)):
                break
            i += 1
        raw = text[start:i]
        value = raw
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in quote_chars and quote is None:
            value = raw[1:-1]
        token = {"raw": raw, "start": start, "end": i, "value": value,
                 "role": "command_argument"}
        if quote:
            token["unresolved"] = "unterminated_quote"
            warnings.append("unterminated_quote")
        tokens.append(token)
    return tokens, warnings


def parse_command(text: str, dialect="windows") -> dict:
    """Return tokens, typed index relations, and conservative parse warnings.

    ``next_token`` preserves order independently of ``argument_of``,
    ``option_value_of`` and ``redirection_target_of``. Only known REG option
    syntax binds separate values. Inline --option=value and /option:value keep
    their original token and expose ``option_name``/``inline_value`` metadata.
    Shell control tokens are surfaced without claiming a complete shell AST.
    ``command_executable`` identifies a syntactic command-position candidate,
    not the image resolved by an operating system. In particular, an unquoted
    Windows path containing spaces is ambiguous here; use a process image field
    when telemetry supplies an authoritative complete image path.
    """
    if not isinstance(text, str):
        raise TypeError("command input must be a string")
    if dialect not in {"windows", "posix"}:
        raise ValueError("dialect must be 'windows' or 'posix'")
    tokens, warnings = _lex(text, dialect)
    relations = [{"source": i, "target": i + 1, "type": "next_token"}
                 for i in range(len(tokens) - 1)]
    executable = None
    executable_name = None
    subcommand = None
    redirection = None
    binding = None
    end_options = False
    nested = False
    for i, token in enumerate(tokens):
        value = token["value"]
        lower = value.lower()
        if token["role"] == "command_operator":
            warnings.append("shell_structure_is_surface_only")
            if binding is not None:
                warnings.append("missing_option_value")
            binding = None
            if value in {">", ">>", "<", "<<"}:
                redirection = i
                if value == "<<":
                    warnings.append("here_document_not_interpreted")
            else:
                redirection = None
                executable = None
                executable_name = None
                subcommand = None
                end_options = False
                nested = False
            continue
        if redirection is not None:
            token["role"] = "command_redirection_target"
            relations.append({"source": i, "target": redirection, "type": "redirection_target_of"})
            redirection = None
            continue
        if binding is not None and token["raw"] == value and re.fullmatch(r"/[A-Za-z?]+(?::.*)?", value):
            # A second bare REG switch is not silently consumed as a value.
            # A quoted string such as "/f" remains a possible literal value.
            warnings.append("missing_option_value")
            binding = None
        if nested:
            token["role"] = "command_unknown"
            token["unresolved"] = "nested_command_payload"
        elif executable is None:
            token["role"] = "command_executable"
            executable = i
            executable_name = re.split(r"[\\/]", lower)[-1]
            continue
        elif binding is not None:
            relations.append({"source": i, "target": binding, "type": "option_value_of"})
            binding = None
        elif executable_name in {"reg", "reg.exe"} and i == executable + 1 and lower in REG_SUBCOMMANDS:
            token["role"] = "command_subcommand"
            subcommand = lower
        elif not end_options and (value.startswith("-") and len(value) > 1 or
                                  dialect == "windows" and re.fullmatch(r"/[A-Za-z?]+(?::.*)?", value)):
            token["role"] = "command_option"
            if value == "--":
                end_options = True
            inline = re.match(r"^(--[^=]+)=(.*)$", value) or (
                re.match(r"^(/[A-Za-z?]+):(.*)$", value) if dialect == "windows" else None)
            if inline:
                token["option_name"], token["inline_value"] = inline.groups()
            if executable_name in {"reg", "reg.exe"} and lower in REG_BOUND_OPTIONS.get(subcommand, set()):
                binding = i
            if executable_name in {"cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "pwsh.exe", "sh", "bash", "zsh"} and lower in {"/c", "/k", "-c", "-command", "-encodedcommand", "-ec"}:
                nested = True
                warnings.append("nested_command_not_interpreted")
        if executable is not None:
            relations.append({"source": i, "target": executable, "type": "argument_of"})
    if redirection is not None:
        warnings.append("missing_redirection_target")
    if binding is not None:
        warnings.append("missing_option_value")
    if dialect == "posix" and ("$" in text or "`" in text or "#" in text):
        warnings.append("shell_expansions_and_comments_not_interpreted")
    if dialect == "windows" and any(char in text for char in "%!^"):
        warnings.append("shell_expansions_and_escapes_not_interpreted")
    if dialect == "windows" and len(tokens) > 1:
        first = tokens[0]
        if (first["role"] == "command_executable" and
                re.match(r"^(?:[A-Za-z]:[\\/]|\\\\)", first["raw"]) and
                not re.search(r"\.(?:exe|com|bat|cmd)$", first["raw"], re.I)):
            warnings.append("unquoted_windows_image_path_may_be_ambiguous")
    return {"tokens": tokens, "relations": relations, "warnings": list(dict.fromkeys(warnings)),
            "dialect": dialect, "interpretation": "surface_syntax_only"}
