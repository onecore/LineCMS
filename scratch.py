class Base(object):

    v = 123

    def __init__(self):
        print("Base init'ed")


class ChildA(Base):
    def __init__(self):
        print("ChildA init'ed")
        Base.__init__(self)
        print v


class ChildB(Base):
    def __init__(self):
        print("ChildB init'ed")
        super().__init__()
