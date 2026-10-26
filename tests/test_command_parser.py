import unittest

from standardizer_pkg.command_parser import parse_command


class CommandParserTests(unittest.TestCase):
    def test_windows_spans_and_backslashes(self):
        raw = r'"C:\Program Files\tool.exe" "C:\Users\Alice\file.txt"'
        result = parse_command(raw)
        self.assertEqual(result["tokens"][0]["value"], r"C:\Program Files\tool.exe")
        self.assertEqual(result["tokens"][1]["value"], r"C:\Users\Alice\file.txt")
        for token in result["tokens"]:
            self.assertEqual(raw[token["start"]:token["end"]], token["raw"])

    def test_unquoted_windows_image_is_not_guessed(self):
        raw = r"C:\Program Files\tool.exe /quiet"
        result = parse_command(raw)
        self.assertEqual(result["tokens"][0]["raw"], r"C:\Program")
        self.assertIn("unquoted_windows_image_path_may_be_ambiguous", result["warnings"])
        for token in result["tokens"]:
            self.assertEqual(raw[token["start"]:token["end"]], token["raw"])

    def test_registry_option_bindings(self):
        result = parse_command(r'reg add HKCU\Software\Example /v Example /d "C:\tool.exe" /f')
        self.assertEqual(result["tokens"][1]["role"], "command_subcommand")
        self.assertIn({"source": 4, "target": 3, "type": "option_value_of"}, result["relations"])
        self.assertIn({"source": 6, "target": 5, "type": "option_value_of"}, result["relations"])
        self.assertNotIn("missing_option_value", result["warnings"])

    def test_unknown_option_does_not_bind_argument(self):
        result = parse_command("tool --unknown value")
        self.assertFalse(any(edge["type"] == "option_value_of" for edge in result["relations"]))

    def test_missing_registry_option_value_is_not_next_switch(self):
        result = parse_command(r"reg add HKCU\Software\Example /v /f")
        self.assertIn("missing_option_value", result["warnings"])
        self.assertEqual(result["tokens"][-1]["role"], "command_option")
        self.assertFalse(any(edge["type"] == "option_value_of" for edge in result["relations"]))

    def test_inline_value_keeps_original_token(self):
        result = parse_command("tool --mode=safe /option:value")
        self.assertEqual(result["tokens"][1]["inline_value"], "safe")
        self.assertEqual(result["tokens"][2]["inline_value"], "value")
        self.assertEqual(result["tokens"][1]["raw"], "--mode=safe")

    def test_pipeline_keeps_order_and_branch_boundaries(self):
        result = parse_command("first arg | second > output.txt")
        self.assertEqual(result["tokens"][3]["role"], "command_executable")
        self.assertEqual(result["tokens"][5]["role"], "command_redirection_target")
        self.assertIn({"source": 5, "target": 4, "type": "redirection_target_of"}, result["relations"])
        self.assertEqual(sum(edge["type"] == "next_token" for edge in result["relations"]), 5)
        self.assertIn("shell_structure_is_surface_only", result["warnings"])

    def test_nested_command_is_explicitly_unresolved(self):
        result = parse_command('cmd /c "reg query HKCU\\Software"')
        self.assertEqual(result["tokens"][2]["role"], "command_unknown")
        self.assertIn("nested_command_not_interpreted", result["warnings"])

    def test_posix_quoted_and_escaped_spaces(self):
        raw = r"tool 'a b' c\ d /tmp/file -- -literal"
        result = parse_command(raw, dialect="posix")
        self.assertEqual([t["raw"] for t in result["tokens"]],
                         ["tool", "'a b'", r"c\ d", "/tmp/file", "--", "-literal"])
        self.assertEqual(result["tokens"][3]["role"], "command_argument")
        self.assertEqual(result["tokens"][-1]["role"], "command_argument")

    def test_unterminated_quotes_are_reported(self):
        result = parse_command('tool "unfinished')
        self.assertIn("unterminated_quote", result["warnings"])
        self.assertEqual(result["tokens"][1]["raw"], '"unfinished')

    def test_quoted_operators_are_not_structure(self):
        result = parse_command('tool "a|b" "x>y"')
        self.assertFalse(any(t["role"] == "command_operator" for t in result["tokens"]))

    def test_empty_and_invalid_inputs(self):
        self.assertEqual(parse_command("  ")["tokens"], [])
        with self.assertRaises(TypeError):
            parse_command(None)
        with self.assertRaises(ValueError):
            parse_command("tool", dialect="other")


if __name__ == "__main__":
    unittest.main()
