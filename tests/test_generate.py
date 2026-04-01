# ABOUTME: Tests for the secret generation module.
# ABOUTME: Validates character set selection, length, and ambiguous character handling.

import string

import pytest

from vaultuner.generate import generate_secret

LOWERCASE = set(string.ascii_lowercase)
UPPERCASE = set(string.ascii_uppercase)
DIGITS = set(string.digits)
SPECIAL = set("!@#$%^&*")
AMBIGUOUS = set("IOl01")


class TestGenerateDefaults:
    def test_default_length(self):
        result = generate_secret()
        assert len(result) == 24

    def test_default_contains_lowercase(self):
        # With 24 chars and all sets enabled, statistically guaranteed
        # Run multiple times to reduce flakiness
        chars = set("".join(generate_secret() for _ in range(10)))
        assert chars & LOWERCASE

    def test_default_contains_uppercase(self):
        chars = set("".join(generate_secret() for _ in range(10)))
        assert chars & UPPERCASE

    def test_default_contains_digits(self):
        chars = set("".join(generate_secret() for _ in range(10)))
        assert chars & DIGITS

    def test_default_contains_special(self):
        chars = set("".join(generate_secret() for _ in range(10)))
        assert chars & SPECIAL

    def test_default_avoids_ambiguous(self):
        # Generate many secrets, none should contain ambiguous chars
        for _ in range(50):
            result = generate_secret()
            assert not (set(result) & AMBIGUOUS), f"Found ambiguous char in: {result}"


class TestGenerateLength:
    def test_custom_length(self):
        assert len(generate_secret(length=64)) == 64

    def test_minimum_length(self):
        assert len(generate_secret(length=1)) == 1

    def test_zero_length_raises(self):
        with pytest.raises(ValueError, match="at least 1"):
            generate_secret(length=0)

    def test_negative_length_raises(self):
        with pytest.raises(ValueError, match="at least 1"):
            generate_secret(length=-5)


class TestGenerateCharacterSets:
    def test_lowercase_only(self):
        result = generate_secret(
            length=100, uppercase=False, numbers=False, special=False
        )
        assert set(result) <= LOWERCASE

    def test_uppercase_only(self):
        result = generate_secret(
            length=100, lowercase=False, numbers=False, special=False
        )
        # With avoid_ambiguous=True, I and O are excluded
        assert set(result) <= (UPPERCASE - AMBIGUOUS)

    def test_numbers_only(self):
        result = generate_secret(
            length=100, lowercase=False, uppercase=False, special=False
        )
        assert set(result) <= (DIGITS - AMBIGUOUS)

    def test_special_only(self):
        result = generate_secret(
            length=100,
            lowercase=False,
            uppercase=False,
            numbers=False,
        )
        assert set(result) <= SPECIAL

    def test_no_character_sets_raises(self):
        with pytest.raises(ValueError, match="At least one"):
            generate_secret(
                lowercase=False, uppercase=False, numbers=False, special=False
            )


class TestGenerateAmbiguous:
    def test_allow_ambiguous(self):
        # With ambiguous allowed and enough length, should eventually include them
        chars = set(
            "".join(
                generate_secret(length=100, avoid_ambiguous=False) for _ in range(20)
            )
        )
        assert chars & AMBIGUOUS

    def test_avoid_ambiguous_excludes_from_all_sets(self):
        for _ in range(50):
            result = generate_secret(length=100, avoid_ambiguous=True)
            assert not (set(result) & AMBIGUOUS)


class TestGenerateCLI:
    """Tests for the generate CLI command."""

    from typer.testing import CliRunner

    runner = CliRunner()

    def test_generate_prints_secret(self):
        from vaultuner.cli import app

        result = self.runner.invoke(app, ["generate"])
        assert result.exit_code == 0
        # Output should be a single line with the generated secret
        lines = result.stdout.strip().split("\n")
        assert len(lines) == 1
        assert len(lines[0]) == 24

    def test_generate_custom_length(self):
        from vaultuner.cli import app

        result = self.runner.invoke(app, ["generate", "--length", "64"])
        assert result.exit_code == 0
        assert len(result.stdout.strip()) == 64

    def test_generate_no_special(self):
        from vaultuner.cli import app

        result = self.runner.invoke(app, ["generate", "--no-special", "-l", "100"])
        assert result.exit_code == 0
        assert not (set(result.stdout.strip()) & SPECIAL)

    def test_generate_no_uppercase(self):
        from vaultuner.cli import app

        result = self.runner.invoke(app, ["generate", "--no-uppercase", "-l", "100"])
        assert result.exit_code == 0
        assert not (set(result.stdout.strip()) & UPPERCASE)

    def test_generate_no_lowercase(self):
        from vaultuner.cli import app

        result = self.runner.invoke(app, ["generate", "--no-lowercase", "-l", "100"])
        assert result.exit_code == 0
        assert not (set(result.stdout.strip()) & LOWERCASE)

    def test_generate_no_numbers(self):
        from vaultuner.cli import app

        result = self.runner.invoke(app, ["generate", "--no-numbers", "-l", "100"])
        assert result.exit_code == 0
        assert not (set(result.stdout.strip()) & DIGITS)

    def test_generate_allow_ambiguous(self):
        from vaultuner.cli import app

        chars = set()
        for _ in range(20):
            result = self.runner.invoke(
                app, ["generate", "--allow-ambiguous", "-l", "100"]
            )
            chars.update(result.stdout.strip())
        assert chars & AMBIGUOUS

    def test_generate_invalid_length(self):
        from vaultuner.cli import app

        result = self.runner.invoke(app, ["generate", "--length", "0"])
        assert result.exit_code == 1
