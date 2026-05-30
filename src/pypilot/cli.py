# pypilot/cli.py
from rich_pyfiglet import RichFiglet
from rich.console import Console
import cmd
from pathlib import Path
import os
from pypilot.memory.chat_store import DataBaseStore
from pypilot.Model_Decider.process import Checker
from pypilot.context_builder import ContextBuilder
from pypilot.context_store import ContextStore
from pypilot.presentation.tree_printer import print_tree

console = Console()


class PypilotCLI(cmd.Cmd):
    print("\n")
    fig = RichFiglet(
        "Pysitant", 
        font="banner3-D",
        colors=["#02701e", "#3d7002", "#ffffff"],
        border_padding=(3, 5),
    )
    
    console.print(fig)
    
    print("\n")
    
    intro = "Welcome to Pypilot. Type 'help' to list commands."
    prompt = "Pypilot> "

    def __init__(self):
        super().__init__()
        self.consent_given = False
        self.project_root = None
        self.builder = None
        self.store = None

    def do_consent(self, arg):
        """Give consent and set project path"""
        path_input = arg.strip() if arg.strip() else os.getcwd()
        project_path = Path(path_input).expanduser().resolve()

        if not project_path.exists() or not project_path.is_dir():
            print("Invalid project path.")
            return

        db = DataBaseStore()
        project_id = db.get_or_create_project(str(project_path))

        if project_id and db.get_consent(project_id):
            self.consent_given = True
            self.project_root = project_path
            self.builder = ContextBuilder(project_path)
            self.store = ContextStore(project_path)
            print(f"Consent already recorded. Project locked to: {project_path}")
            return

        decision = input("Do you agree to share your project structure with the AI? (y/n): ").strip().lower()
        if decision not in ("y", "yes"):
            print("Consent not given.")
            return

        if project_id is None:
            print("Failed to initialize project in database.")
            return

        db.update_consent(project_id, True)

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
        if not self._ready():
            return

        if self.store and self.builder:
            try:
                context = self.builder.build()
                self.store.save(context)
                print("Context refreshed successfully.")
            except Exception as e:
                print(f"Failed to refresh context: {e}")

    def do_inspect(self, arg):
        """Inspect the project structure"""
        if not self._ready():
            return

        if self.store and not self.store.exists():
            print("Nothing to inspect. Run 'build_once' first.")
            return

        if self.store:
            print_tree(self.store.load())

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
        checker = Checker(project_path=self.project_root)

        try:
            result = checker.decide(question=question, context=context)
            print(result)
        except Exception as e:
            print("\n[ERROR] Failed to process request.\n")
            print(e)

    def _ready(self) -> bool:
        db = DataBaseStore()

        if not self.project_root:
            project_path = db.fetch_last_project_path()
            if not project_path:
                print("No project selected. Run: consent")
                return False
            self.project_root = Path(project_path)
            self.builder = ContextBuilder(self.project_root)
            self.store = ContextStore(self.project_root)

        project_id = db.fetch_id(str(self.project_root))
        if project_id is None:
            print("Project not initialized. Run: consent")
            return False

        self.consent_given = db.get_consent(project_id)
        if not self.consent_given:
            print("Consent required. Run: consent")
            return False

        return True
    
    def do_EOF(self, arg):
        """Handle end-of-input (e.g. non-interactive stdin) and exit cleanly."""
        print()
        return self.do_exit(arg)

    def do_exit(self, arg):
        """Exit Pypilot"""
        print("Goodbye.")
        return True

    do_quit = do_exit

    def emptyline(self):
        pass

if __name__ == "__main__":
    PypilotCLI().cmdloop()