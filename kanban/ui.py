"""Contains UI widgets."""
from typing import Tuple

import urwid

from kanban.board import Kanban


class SelectableText(urwid.Text):
    """Represents a card's title."""
    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class UICard(urwid.LineBox):
    """Represents a card."""
    def __init__(self, text, desc: str = None, subtasks: Tuple[int, int] = None):
        self.selectable_text = SelectableText(text)
        self.attr_map = urwid.AttrMap(self.selectable_text, '',  'reveal focus')

        pile = []
        subtitle_text = ''
        if desc:
            subtitle_text += '≡'
        if subtasks:
            subtitle_text += f' [{subtasks[0]}/{subtasks[1]}]'
        subtitle_text = subtitle_text.strip()

        self.tags = urwid.AttrMap(urwid.Text('[tag][another_tag]'), 'tag')
        pile.append(self.attr_map)

        if subtitle_text:
            pile.append(
                urwid.AttrMap(urwid.Text(subtitle_text), 'card_description')
            )

        self.pile = urwid.Pile(pile)
        super().__init__(self.pile,
                         # title='', title_align='center', tlcorner='┌', tline='─', lline='│', trcorner='┐', blcorner='╘', rline='│', bline='═', brcorner='╛'
                         # title='', title_align='center', tlcorner='╭', tline='─', lline='│', trcorner='╮', blcorner='╰', rline='│', bline='─', brcorner='╯'
                         title='', title_align='center', tlcorner='', tline=' ', lline='', trcorner='', blcorner='', rline='', bline='', brcorner=''
                         )

    def set_text(self, text):
        self.selectable_text.set_text(text)


class MyColumns(urwid.Columns):
    """Represents Kanban board columns."""
    def __init__(self, widget_list, *args, **kwargs):
        super().__init__(widget_list, *args, **kwargs)

    def keypress(self, size, key):
        if key in ["l", "right"]:
            super().keypress(size, 'right')
        elif key in ["h", "left"]:
            super().keypress(size, 'left')
        elif key in ["k", "up"]:
            super().keypress(size, 'up')
        elif key in ["j", "down"]:
            super().keypress(size, 'down')
        else:
            return key

    def _get_current_column(self):
        """Returns focused column."""
        focused_list: urwid.ListBox = self.get_focus_widgets()
        current_column = focused_list[0].body
        return current_column

    def is_empty(self):
        """Return True if the board is empty."""
        column_list = self.contents
        return len(column_list) <= 0

    def delete_current_column(self):
        """Deletes focused column."""
        if self.is_empty():
            return
        column_list = self.contents
        if len(column_list) > 0:
            col, row, *_ = self.get_focus_path()
            del column_list[col]

    def delete_current_card(self):
        """Delete focused card."""
        if self.is_empty():
            return
        col, row, *_ = self.get_focus_path()
        current_column = self._get_current_column()
        if row != 0:
            current_column.pop(row)

    def move_current_card_down(self):
        """Move focused card down"""
        if self.is_empty():
            return
        col, row, *_ = self.get_focus_path()
        current_column = self._get_current_column()
        if row < len(self[col].body) - 1:
            a_card = current_column.pop(row)
            current_column.insert(row + 1, a_card)
            self.set_focus_path([col, row + 1])

    def move_current_card_up(self):
        """Move focused card up"""
        if self.is_empty():
            return
        col, row, *_ = self.get_focus_path()
        current_column = self._get_current_column()
        if row > 1:
            a_card = current_column.pop(row)
            current_column.insert(row - 1, a_card)
            self.set_focus_path([col, row - 1])

    def move_current_card_to_next_column(self):
        """Move focused to the next column"""
        if self.is_empty():
            return
        col, row, *_ = self.get_focus_path()
        current_column = self._get_current_column()
        column_list = self.contents
        if col < len(column_list) - 1:
            a_card = current_column.pop(row)
            self[col + 1].body.append(a_card)
            self.set_focus_path([col + 1, len(self[col + 1].body) - 1])

    def move_current_card_to_previous_column(self):
        """Move focused to the previous column"""
        if self.is_empty():
            return
        col, row, *_ = self.get_focus_path()
        current_column = self._get_current_column()
        if col != 0:
            a_card = current_column[row]
            self[col - 1].body.append(a_card)
            del current_column[row]
            self.set_focus_path([col - 1, len(self[col - 1].body) - 1])

    def set_focus_to_first_column_item(self):
        """Focus column's top card."""
        if self.is_empty():
            return
        col, row, *_ = self.get_focus_path()
        self.set_focus_path([col, 1])

    def set_focus_to_last_column_item(self):
        """Focus append card to """
        if self.is_empty():
            return
        col, row, *_ = self.get_focus_path()
        self.set_focus_path([col, len(self[col].body) - 1])

    def append_to_current_column(self, card: UICard):
        """Append a card to current column."""
        if self.is_empty():
            return
        col, row, *_ = self.get_focus_path()
        current_column = self._get_current_column()
        current_column.insert(len(self[col].body), card)
        self.set_focus_to_last_column_item()

    def prepend_to_current_column(self, card: UICard):
        """Append a card to current column."""
        if self.is_empty():
            return
        col, row, *_ = self.get_focus_path()
        current_column = self._get_current_column()
        current_column.insert(1, card)
        self.set_focus_to_first_column_item()


# TODO this could be a frame?
class UIMain:
    """App's main user interface."""
    def __init__(self):
        self.palette = [
            ('reveal focus', 'dark magenta', 'default', 'standout'),
            # ('reveal focus', 'bold, dark magenta', 'default', 'standout'),
            # ('list_title', 'dark red', 'default'),
            ('list_title', 'dark green', 'default'),
            # ('tag', 'black', 'dark green'),
            ('tag', 'dark green', 'default'),
            ('streak', 'black', 'dark red'),
            ('card_description', 'brown', 'default'),
            ('board_title', 'dark blue', 'default'),
            ('footer', 'dark blue', 'black'),
            ('footer_text', 'dark blue', 'black'),
            ('footer_separator', 'dark magenta', 'black'),
            ('footer_item', 'white', 'black'),
            ('bg', 'black', 'dark blue'),
        ]
        self.loop = None
        self.cols = None
        self.frame = None

    def build_board(self, kanban: Kanban):
        """Display Kanban board."""
        column_list = []
        for count, col in enumerate(kanban.columns):
            list_content = []
            # TODO title mejor en un objeto customizado
            list_content.append(
                urwid.AttrMap(urwid.Text(f'{count + 1}. {col.name}'), 'list_title'),
            )
            for card in col.cards:
                subtasks = None
                if card.subtasks:
                    subtasks = (card.subtasks_completed(), len(card.subtasks))
                list_content.append(
                    UICard(f'{card.name}', desc=card.description, subtasks=subtasks),
                )
            col_content = urwid.SimpleListWalker(list_content)
            listbox = urwid.ListBox(col_content)
            column_list.append(listbox)
            self.cols = MyColumns(column_list, dividechars=4, min_width=30)

            padding = urwid.Padding(self.cols, left=2, right=2)
            header = urwid.AttrMap(urwid.Text('DAS: Android Final Project\n', align=urwid.CENTER), 'board_title')
            footer = urwid.AttrMap(
                urwid.Text([
                    # ('footer_text', u"Total cards: "),
                    # ('footer_item', u"11"),
                    # ('footer_separator', u" | "),
                    ('footer_text', u"Help "),
                    ('footer_item', u"?"),
                ]),
                'footer')
            # self.frame = urwid.Frame(body=padding, footer=footer)
            self.frame = urwid.Frame(body=padding, header=header, footer=footer)

    def unhandled_input(self, key):
        """Handle input that no other widget has handled."""
        if key == 'enter':
            # TODO debug in footer
            self.frame.footer.base_widget.set_text("Debug text")
        elif key == "D":
            self.cols.delete_current_card()
        elif key == "A":
            self.cols.append_to_current_column(UICard("Testing"))
        elif key == "I":
            self.cols.prepend_to_current_column(UICard("Testing"))
        elif key == "X":  # delete column
            self.cols.delete_current_column()
        elif key in ["shift down", "J"]:
            self.cols.move_current_card_down()
        elif key in ["shift up", "K"]:
            self.cols.move_current_card_up()
        elif key in ["shift right", "L"]:
            self.cols.move_current_card_to_next_column()
        elif key in ["shift left", "H"]:
            self.cols.move_current_card_to_previous_column()
        elif key in "G$":
            self.cols.set_focus_to_last_column_item()
        elif key in "g0^":
            self.cols.set_focus_to_first_column_item()
        elif key in 'qQ':
            raise urwid.ExitMainLoop()

    def run(self):
        """Start UI."""
        self.loop = urwid.MainLoop(self.frame, palette=self.palette, unhandled_input=self.unhandled_input, handle_mouse=False)
        # TODO support more colors
        # loop.screen.set_terminal_properties(colors=256)

        try:
            self.loop.run()
        except KeyboardInterrupt:
            pass
