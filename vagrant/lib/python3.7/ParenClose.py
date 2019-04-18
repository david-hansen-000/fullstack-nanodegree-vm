class ParenClose:
    '''
    When loaded as an extension to IDLE, and paren_close is True, the symbols
    ([{ will have their closures printed after them and the insertion cursor
    moved between the two.  The same is true for tick closures and the symbols ' and ".  When \'\'\' or """ are
    typed and tick_close is True, it will also produce the closing symbols.
    If skip_closures is True, then when a closure symbol is typed and the same
    one is to the right of it, that symbols is deleted before the new one is
    typed, effectively skipping over the closure.
    '''
    def __init__(self, editwin=None): #setting default to none makes testing easier
        if editwin:
            self.text = editwin.text
        else:
            self.text=None
        self.paren_close = idleConf.GetOption(
            'extensions', 'ParenClose', 'paren_close', default=True)
        self.tick_close = idleConf.GetOption(
            'extensions', 'ParenClose', 'tick_close', default=True)
        self.skip_closures = idleConf.GetOption(
            'extensions', 'ParenClose', 'skip_closures', default=True)

    def p_open_event(self, event):
        if self.paren_close:
            closer = {'(': ')', '[': ']', '{': '}'}[event.char]
            pos = self.text.index('insert')
            self.text.insert(pos, closer)
            self.text.mark_set('insert', pos)

    def p_close_event(self, event):
        pos = self.text.index('insert')
        if self.skip_closures == True \
           and self.text.get(pos, pos + ' +1c') == event.char:
            self.text.delete(pos, pos + ' +1c')

    def t_open_event(self, event):
        if self.tick_close:
            pos = self.text.index('insert')
            # don't do if there are two ticks
            # user wants to make docstring or multiline
            if self.text.get(pos + ' -2c', pos) != event.char * 2 \
               or self.text.get(pos, pos + ' +1c') == event.char:
                if self.skip_closures == True\
                   and self.text.get(pos, pos + ' +1c') == event.char:
                    self.text.delete(pos, pos + ' +1c')
                else:
                    self.text.insert(pos, event.char)
                    self.text.mark_set('insert', pos)
            else:
                self.text.insert(pos, event.char * 3)
                self.text.mark_set('insert', pos)
