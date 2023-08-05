import unittest
import re

import filecabinet.processor as fp


class TestRuleParser(unittest.TestCase):
    def test_one_rule(self):
        text = "match /hello/"
        rules = fp.Rule.parse(text)
        self.assertEqual(len(rules), 1)
        self.assertEqual(len(rules[0].conditions), 1)
        self.assertTrue(rules[0].match("why hello there"))

    def test_no_match(self):
        text = "match /sausage/"
        rules = fp.Rule.parse(text)
        self.assertFalse(rules[0].match("why hello there"))

    def test_fail_parse_match(self):
        text = "match /spam"
        with self.assertRaises(fp.ParseError):
            fp.Rule.parse(text)

    def test_more_conditions(self):
        text = "match /albatros/ and /foo/ /ice cream/"
        rules = fp.Rule.parse(text)
        self.assertTrue(rules[0].match("You fool, I don't want an albatros, I want ice cream!"))

    def test_impossible_expression(self):
        text = "match /some\/ stuff/"
        with self.assertRaises(fp.ParseError):
            fp.Rule.parse(text)

    def test_possible_expression(self):
        text = "match :some/ stuff:"
        fp.Rule.parse(text)

    def test_many_rules(self):
        text = "match /banana/\nmatch /spamalot/"
        rules = fp.Rule.parse(text)
        self.assertEqual(len(rules), 2)

    def test_find_rules(self):
        text = """match /meh/
find issuer /(Big Corp [a-zA-Z]+)/
set issuer {issuer}

match /fibsh/
  find format /Format[ \\n\\t]+([^\\n]+)/
  find title /Subject[ \\n\\t]+([^\\n]+)/
  set format {format}
  set title {title}
"""
        rules = fp.Rule.parse(text)
        self.assertEqual(len(rules), 2)
        self.assertEqual(len(rules[0].finds), 1)
        self.assertEqual(len(rules[1].finds), 2)

    def test_regex_fail(self):
        text = "match /bla [/"

        with self.assertRaises(fp.RegExParseError):
            fp.Rule.parse(text)

    def test_unused_finds(self):
        text = """match /meh/
find foo /(bar)/
"""

        with self.assertRaises(fp.UnusedFindsError):
            fp.Rule.parse(text)

    def test_undefined_find(self):
        text = """match /meh/
set state very {state}
"""

        with self.assertRaises(fp.UndefinedFindError):
            fp.Rule.parse(text)

    def test_set_regex(self):
        text = """match /foo/ and /bar/
set issuer /(Big Corp [a-zA-Z]+)/"""

        rules = fp.Rule.parse(text)
        self.assertTrue(isinstance(rules[0].sets['issuer'].pop(), re.Pattern))

    def test_spaced_set(self):
        text = """match /albatross/
set "ice cream" yes
set "ice cream flavour" /([a-z]+) taste/"""

        rules = fp.Rule.parse(text)
        self.assertEqual(rules[0].sets['ice cream'].pop(), 'yes')


class TestRuleExecution(unittest.TestCase):
    GENERIC_INVOICE = """Invoice #12345\n2012-04-13\n\nDear Customer,\nThanks for ordering at Big Corp.
Please pay us now this ridiculous amount: $500.20 until 2012-05-30.\nThanks."""

    def test_str_set(self):
        rules = fp.Rule.parse("""match /Big Corp/
set issuer Big Corp Inc.
""")

        attrs = rules.run(TestRuleExecution.GENERIC_INVOICE)
        self.assertEqual(attrs['issuer'], {'Big Corp Inc.',})

    def test_find_set(self):
        rules = fp.Rule.parse("""match /Invoice/
find invoicenr /Invoice[ \t]+#([0-9]+)/
find amount /[ \t]+\$[ \t]*([0-9]+\.?[0-9]{2}?)/
set bill "{invoicenr}"
set amount ${amount}
# set other "not"
; set commented out
""")

        attrs = rules.run(TestRuleExecution.GENERIC_INVOICE)
        self.assertEqual(len(attrs), 2)
        self.assertEqual(attrs['bill'], {'12345',})
        self.assertEqual(attrs['amount'], {'$500.20',})

    def test_direct_regex(self):
        rules = fp.Rule.parse("""match /Big Corp/
set invoicenr /Invoice[ \t]+#([0-9]+)/
set date /([0-9]{4}-[01][0-9]-[0-3][0-9])/
""")

        attrs = rules.run(TestRuleExecution.GENERIC_INVOICE)
        self.assertEqual(attrs['invoicenr'], {'12345',})
        self.assertEqual(attrs['date'], {'2012-05-30', '2012-04-13'})

    def test_multi_set(self):
        rules = fp.Rule.parse("""match /Big Corp/
set issuer Big Corp
set issuer BCinc""")

        attrs = rules.run(TestRuleExecution.GENERIC_INVOICE)
        self.assertEqual(attrs['issuer'], {'Big Corp', 'BCinc'})

    def test_case_insensitive_match(self):
        rules = fp.Rule.parse("""match .big corp.i
set issuer Big Corp
""")
        attrs = rules.run(TestRuleExecution.GENERIC_INVOICE)
        self.assertEqual(attrs['issuer'], {'Big Corp'})

    def test_case_insensitive_find(self):
        rules = fp.Rule.parse("""match /Big Corp/
find issuer /(big [a-z]+)/i
set issuer {issuer}
""")
        attrs = rules.run(TestRuleExecution.GENERIC_INVOICE)
        self.assertEqual(attrs['issuer'], {'Big Corp'})

    def test_case_insensitive_set(self):
        rules = fp.Rule.parse("""match /Big Corp/
set issuer /(big [a-z]+)/i
""")
        attrs = rules.run(TestRuleExecution.GENERIC_INVOICE)
        self.assertEqual(attrs['issuer'], {'Big Corp'})

    def test_spaced_set(self):
        text = """match /Big Corp/
set "silly amount" /\\$([0-9]+)/"""

        rules = fp.Rule.parse(text)
        attrs = rules.run(TestRuleExecution.GENERIC_INVOICE)
        self.assertEqual(attrs['silly amount'], {'500'})


if __name__ == "__main__":
    unittest.main()

