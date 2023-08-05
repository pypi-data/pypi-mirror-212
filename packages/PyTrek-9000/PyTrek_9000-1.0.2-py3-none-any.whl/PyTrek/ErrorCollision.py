class ErrorEnterpriseCollision(Exception):
    '''
    ... because some problems simply have to wait ... =)
    '''
    def __init__(self, glyph):
        super().__init__()
        self.glyph = glyph


