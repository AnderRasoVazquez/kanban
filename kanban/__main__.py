"""Main module."""
from kanban.board import MarkdownParser, Kanban
from kanban.ui import UIMain


def main() -> None:
    """Main function."""
    m = MarkdownParser()
    kanban: Kanban = m.parse_file("kanban.md")
    ui = UIMain()
    ui.build_board(kanban)
    ui.run()


if __name__ == '__main__':
    main()
