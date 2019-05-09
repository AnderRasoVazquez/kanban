from typing import List

"""
## To Do
- Una tarea de prueba
- Otra tarea
    > Más descripción
- Otro todo
    * [ ] Subtareas
## Done
- Más tareas
    > La descripción
    * [ ] Una subtarea
    * [x] Otra tarea
    * [ ] Última tarea
"""

# TODO hardcoded parsing is not good
HEADING = "## "
ITEM_NAME = "- "
ITEM_DESCRIPTION = "    > "
SUB_ITEM = "    * "
TODO = "    * [ ] "
COMPLETED = "    * [x] "


class SubTask(object):
    """Represents a subitem"""
    def __init__(self, name, completed=False):
        self.name: str = name
        self.completed: bool = completed


class Card(object):
    """Represents a card of a kanban board."""
    def __init__(self, name: str, description: str = None):
        self.name: str = name
        self.description: str = description
        self.subtasks: List[SubTask] = []

    def append(self, subtask: SubTask):
        """Append a new subtask"""
        self.subtasks.append(subtask)

    def __str__(self) -> str:
        result: str = ""
        result += ITEM_NAME + self.name
        result += "\n"
        if self.description:
            result += ITEM_DESCRIPTION + self.description
            result += "\n"
        for subtask in self.subtasks:
            result += TODO if subtask.completed else COMPLETED
            result += subtask.name
            result += "\n"
        return result

    def subtasks_completed(self) -> int:
        """Returns the number of completed tasks"""
        return sum(subtask.completed for subtask in self.subtasks)

    def subtasks_uncompleted(self) -> int:
        """Returns the number of completed tasks"""
        return sum(not subtask.completed for subtask in self.subtasks)


class CardList(object):
    """Reperesents a card list of a kanban board."""
    def __init__(self, name: str):
        self.name: str = name
        self.cards: List[Card] = []

    def append(self, card: Card):
        """Append a new card"""
        self.cards.append(card)

    def move_card_down(self, initial_pos: int) -> bool:
        """Moves a column right"""
        pos_right: int = initial_pos + 1
        if pos_right >= len(self.cards):
            return False
        else:
            self.cards[initial_pos], self.cards[pos_right] = self.cards[pos_right], self.cards[initial_pos]
            return True

    def move_card_up(self, initial_pos: int) -> bool:
        """Moves a column right"""
        pos_left: int = initial_pos - 1
        if pos_left <= 0:
            return False
        else:
            self.cards[initial_pos], self.cards[pos_left] = self.cards[pos_left], self.cards[initial_pos]
            return True

    def __str__(self) -> str:
        result: str = ""
        result += HEADING + self.name
        result += "\n"
        result += "\n"
        for card in self.cards:
            result += str(card)
        return result


class Kanban(object):
    """Represents a kanban board."""
    def __init__(self):
        self.columns: List[CardList] = []
        pass

    def append(self, card_list: CardList):
        """Append a new column"""
        self.columns.append(card_list)

    def move_column_right(self, initial_pos: int) -> bool:
        """Moves a column right"""
        pos_right: int = initial_pos + 1
        if pos_right >= len(self.columns):
            return False
        else:
            self.columns[initial_pos], self.columns[pos_right] = self.columns[pos_right], self.columns[initial_pos]
            return True

    def move_column_left(self, initial_pos: int) -> bool:
        """Moves a column right"""
        pos_left: int = initial_pos - 1
        if pos_left <= 0:
            return False
        else:
            self.columns[initial_pos], self.columns[pos_left] = self.columns[pos_left], self.columns[initial_pos]
            return True

    def save(self, path):
        """Save Kanban contents to a file."""
        with open(path, 'w') as f:
            f.write(str(self))

    def __str__(self) -> str:
        result: str = ""
        for card_list in self.columns:
            result += str(card_list)
            result += "\n"
        return result


class MarkdownParser(object):
    """Parses markdown."""
    def __init__(self):
        self.kanban = None
        self._current_card_list = None
        self._current_card = None

    def _parse_line(self, line: str):
        """Create a kanban board by parsing lines."""
        if line.startswith(HEADING):
            list_title = line[len(HEADING):]
            self._current_card_list = CardList(list_title)
            self.kanban.append(self._current_card_list)
        elif line.startswith(ITEM_NAME):
            card_title = line[len(ITEM_NAME):]
            self._current_card = Card(card_title)
            self._current_card_list.append(self._current_card)
        elif line.startswith(ITEM_DESCRIPTION):
            card_description = line[len(ITEM_DESCRIPTION):]
            self._current_card.description = card_description
        elif line.startswith(SUB_ITEM):
            subtask_name = line[len(TODO):]
            subtask = SubTask(name=subtask_name)
            if line.startswith(TODO):
                subtask.completed = False
            elif line.startswith(COMPLETED):
                subtask.completed = True
            self._current_card.append(subtask)

    def parse_file(self, path: str) -> Kanban:
        """Parse a markdown file and return a kanban board."""
        # Restart values
        self.kanban = Kanban()
        self._current_card_list = None
        self._current_card = None

        with open(path) as f:
            text = f.read()
            for line in text.split('\n'):
                if line:
                    self._parse_line(line)
        return self.kanban
