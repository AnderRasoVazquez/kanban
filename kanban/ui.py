from typing import Tuple

import urwid

from kanban.board import Kanban


class SelectableText(urwid.Text):
    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class UICard(urwid.LineBox):
    # class UICard(urwid.LineBox):
    def __init__(self, text, desc: str = None, subtasks: Tuple[int, int] = None):
        # TODO pila de valores
        # tags
        # nombre
        # descripcion
        # valores completados de la lista si los hay
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
        pass
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
            filler = urwid.Filler(self.cols, 'top')
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
            self.frame = urwid.Frame(body=padding, header=header, footer=footer)

    def unhandled_input(self, key):
        # TODO controlarlo mejor en clases que lo hereden?
        focused_list: urwid.ListBox = self.cols.get_focus_widgets()
        current_card: UICard = self.cols.focus.focus # esto devuelve la carta
        debug = focused_list[0]
        col, row, *_ = self.cols.get_focus_path()  # devuelve el elemento, ej: [0, 2]
        # si hay mas devuelve   ej: [0, 2, 1]
        # puede ser interesante para coger la tarjeta y actualizarla con el nuevo valor
        # si se guarda con el nuevo valor pasar esa tarjeta a la vista para que se actualice, o un json mejor
        # TODO mirar si existe una forma de obtener el widget que quiero
        item: urwid.LineBox = focused_list[1]  # line box
        # item.set_text("Probando a meter texto")
        # item.set_text("probando a meter texto en la carta")
        # base = item.base_widget
        # base.set_text("widget obtenido")
        # TODO for debugging
        # debug.body[1], debug.body[2] = debug.body[2], debug.body[1]
        # debug.body.insert(1, UICard("insertado"))
        # loop.draw_screen()
        if key == 'enter':
            current_card.set_text("TESTING")
            pass
            # card_one.set_text(repr(debug.body[1].set_text("woow")))
        elif key == "D":  # delete card
            # del current_card
            if row != 0:  # don't delete de title
                del debug.body[row]
                self.loop.draw_screen()
        elif key == "X":  # delete column
            if len(self.cols.contents) > 0:
                del self.cols.contents[col]
                self.loop.draw_screen()
        elif key in ["shift down", "J"]:  # delete column
            if row < len(self.cols[col].body) - 1:
                a_card = debug.body[row]  # get current card
                del debug.body[row]
                debug.body.insert(row + 1, a_card)
                self.cols.set_focus_path([col, row + 1])
        elif key in ["shift up", "K"]:  # delete column
            if row > 1:  # the column title is pos 0
                a_card = debug.body[row]  # get current card
                del debug.body[row]
                debug.body.insert(row - 1, a_card)
                self.cols.set_focus_path([col, row - 1])
        elif key in ["shift right", "L"]:  # delete column
            if self.cols.focus_col < len(self.cols.contents) - 1:
                a_card = debug.body[row]
                self.cols[col + 1].body.append(a_card)
                del debug.body[row]
                # cols.focus_position = [1, 1]

                self.cols.set_focus_path([col + 1, len(self.cols[col + 1].body) - 1])
                # cols.set_focus_path([col + 1, len(cols[0].body)])

                # listbox: urwid.ListBox = cols[col + 1]
                # walker: urwid.ListWalker = listbox.body
                # card = debug.body[row]
                # cols.contents
                # loop.draw_screen()
        elif key in ["shift left", "H"]:  # delete column
            if self.cols.focus_col != 0:
                a_card = debug.body[row]
                self.cols[col - 1].body.append(a_card)
                del debug.body[row]

                self.cols.set_focus_path([col - 1, len(self.cols[col - 1].body) - 1])
                # card = debug.body[row]
                # cols.contents
                # loop.draw_screen()
        elif key in "G$":
            self.cols.set_focus_path([col, len(self.cols[col].body) - 1])
        elif key in "g0^":
            self.cols.set_focus_path([col, 1])

        elif key in 'qQ':
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop = urwid.MainLoop(self.frame, palette=self.palette, unhandled_input=self.unhandled_input, handle_mouse=False)
        # TODO support more colors
        # loop.screen.set_terminal_properties(colors=256)

        try:
            self.loop.run()
        except KeyboardInterrupt:
            pass
