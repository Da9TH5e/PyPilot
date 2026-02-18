import cmd
from pathlib import Path
import os
from pypilot.models.process import Checker
from pypilot.context_builder import ContextBuilder
from pypilot.context_store import ContextStore
from pypilot.presentation.tree_printer import print_tree


class PypilotCLI(cmd.Cmd):
    intro = "Welcome to Pypilot. Type 'help' to list commands."
    prompt = "Pypilot> "

    def __init__(self):
        super().__init__()
        self.consent_given = False
        self.task_consent = False
        self.project_root = None
        self.builder = None
        self.memory = None
        self.store = None

    def do_consent(self, arg):
        """Give consent and set project path"""
        if self.consent_given:
            print(f"Consent already given. Project locked to: {self.project_root}")
            return

        decision = input("Do you agree to the terms? (y/n): ").strip().lower()
        if decision not in ("y", "yes"):
            print("Consent not given.")
            return

        path_input = arg.strip() if arg.strip() else os.getcwd()
        project_path = Path(path_input).expanduser().resolve()

        if not project_path.exists() or not project_path.is_dir():
            print("Invalid project path.")
            return
        self.consent_given = True
        self.project_root = project_path
        self.builder = ContextBuilder(project_path)
        self.store = ContextStore(project_path)

        print(f"Consent recorded. Project set to: {project_path}")

    def do_build_once(self, arg):
        """Build context only if it does not already exist"""
        if not self._ready():
            return

        if self.store and self.builder:
            if self.store.exists():
                print("Context already exists. Use 'refresh' to rebuild.")
                return

            try:
                context = self.builder.build()
                self.store.save(context)
                print("Context built successfully.")
            except Exception as e:
                print(f"Failed to build context: {e}")

    def do_refresh(self, arg):
        """Rebuild context ignoring existing one"""
        if self.store and self.builder:    
            try:
                context = self.builder.build()
                self.store.save(context)
                print("Context refreshed successfully.")
            except Exception as e:
                print(f"Failed to refresh context: {e}")

    def heavy_mode_enabled(self) -> bool:
        user_decision = input("Your prompt includes heavy tasks which might impact the performance it is suggested to connect to internet and then try again.\n If you wish to proceed then Enter(y/n) :")
        if user_decision not in ("yes", "y"):
            return False
        return True

    def do_inspect(self, arg):
        """Inspect the project structure"""
        if not self._ready():
            return

        if self.store and not self.store.exists():
            print("Nothing to inspect. Run 'build_once' first.")
            return

        if self.store:
            print_tree(self.store.load())
    # Backward-compatible alias
    do_display = do_inspect

    def do_ask(self, arg: str) -> None:
        """Ask Pypilot a question about the project."""

        if not self._ready():
            return

        question = arg.strip()
        if not question:
            print("Please provide a question.")
            return

        if not self.store or not self.store.exists():
            print("No context found. Run 'build_once' first.")
            return

        print("Generating response...\n")
        context = self.store.load()
        checker = Checker()

        try:
            result = checker.decide(
                question=question,
                context=context,
                heavy=False,
            )

            print(result)

        except Exception as e:
            print("\n[ERROR] Failed to process request.\n")
            print(e)

    def _ready(self) -> bool:
        if not self.consent_given or not self.builder or not self.store:
            print("Consent required. Run: consent")
            return False

        return True

    def do_exit(self, arg):
        """Exit Pypilot"""
        print("Goodbye.")
        return True
        
    do_quit = do_exit

    def emptyline(self):
        pass

if __name__ == "__main__":
    PypilotCLI().cmdloop()