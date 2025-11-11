import hashlib
from pathlib import Path

import pytest

from jane_the_ripper import crack_passwords


def md5(text: str) -> str:
	return hashlib.md5(text.encode()).hexdigest()


def write_lines(path: Path, lines):
	path.write_text("\n".join(lines) + ("\n" if lines else ""))


def test_crack_passwords_finds_all_matches(tmp_path, capsys):
	# create hashes for two known words
	words = ["secret", "hello"]
	hash_lines = [md5(w) for w in words]

	hash_file = tmp_path / "hashes.txt"
	wordlist_file = tmp_path / "wordlist.txt"

	# the wordlist contains the passwords (in different order)
	write_lines(hash_file, hash_lines)
	write_lines(wordlist_file, ["foo", "hello", "bar", "secret"])

	crack_passwords(str(hash_file), str(wordlist_file))
	captured = capsys.readouterr()
	out = captured.out

	# should report both cracked and success
	for h, w in zip(hash_lines, words):
		assert f"Cracked: {h} --> {w}" in out
	assert "All hashes cracked successfully" in out


def test_crack_passwords_partial(tmp_path, capsys):
	# one hash matches, one does not
	present = "password"
	missing = "notinthelist"
	hash_file = tmp_path / "hashes.txt"
	wordlist_file = tmp_path / "wordlist.txt"

	write_lines(hash_file, [md5(present), md5(missing)])
	write_lines(wordlist_file, [present])

	crack_passwords(str(hash_file), str(wordlist_file))
	captured = capsys.readouterr()
	out = captured.out

	assert f"Cracked: {md5(present)} --> {present}" in out
	# should show a FAILED line for the remaining hash
	assert "FAILED:" in out


def test_crack_passwords_empty_wordlist(tmp_path, capsys):
	# hash file has entries but wordlist is empty
	hashes = [md5("a"), md5("b")]
	hash_file = tmp_path / "hashes.txt"
	wordlist_file = tmp_path / "wordlist.txt"

	write_lines(hash_file, hashes)
	write_lines(wordlist_file, [])

	crack_passwords(str(hash_file), str(wordlist_file))
	captured = capsys.readouterr()
	out = captured.out

	# should not claim success
	assert "All hashes cracked successfully" not in out
	# should list each remaining hash as FAILED
	for h in hashes:
		assert h in out
