from pathlib import Path

pot_path = Path(__file__).parent.parent / "package_build" / "locale" / "messages.pot"

data = pot_path.read_text("utf-8").splitlines(keepends=True)

with pot_path.open("w") as pot_file:
    for line in data:
        if line.startswith('"POT-Creation-Date:'):
            continue

        pot_file.write(line)
