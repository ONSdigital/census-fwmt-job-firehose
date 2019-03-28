def init_app(app):
    pass

class Pause:

    def __init__(self, effective_date, code, reason, hold_until):
        self.effective_date = effective_date
        self.code = code
        self.reason = reason
        self.hold_until = hold_until

def construct_pause():
    return Pause(effective_date='06/02/2019', code='code', reason='reason', hold_until='2019-02-06')
