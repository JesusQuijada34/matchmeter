import ast
from pathlib import Path

source = Path("matchmeter.py").read_text(encoding="utf-8")
ast.parse(source, filename="matchmeter.py")
details = Path("details.xml").read_text(encoding="utf-8")
readme = Path("README.md").read_text(encoding="utf-8")
requirements = Path("lib/requirements.txt").read_text(encoding="utf-8")
assert "PyQt5" not in source
assert "PyQt6" in source
assert "app.exec()" in source
assert "app.exec_()" not in source
assert "<platform>AlphaCube</platform>" in details
assert "PyQt6" in requirements
assert "AlphaCube" in readme
assert "return 0" not in source
assert "class MatchMeterApp" in source
assert "self.result_frame.setVisible(True)" in source
print("MATCHMETER_STATIC_FUNCTIONAL_CHECK_OK")
