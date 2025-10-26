import sys
from pathlib import Path
from scanner import Scanner

class Lox():
    def __init__(self):
        self.hadError = False

    def main(self, args: list):
        length = len(args)
        if length > 1:
            print("Usage: plox [script]")
            sys.exit(64)
        elif length == 1:
            self.runFile(args[0])
        else:
            self.runPrompt()

    def runFile(self, path: str):
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError
        self.run(p.read_text(encoding="utf-8"))

        if self.hadError: sys.exit(65)

    def runPrompt(self):
        while True:
            line = input("> ")
            if not line: break
            self.run(line)
            self.hadError = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        print("[line " + line + "] Error" + where + ": " + message, file=sys.stderr)
        self.hadError = True