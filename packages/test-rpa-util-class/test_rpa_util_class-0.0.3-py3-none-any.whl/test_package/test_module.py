class TestUtilClass:
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2

    def concatenate(self):
        print(self.var1 + self.var2)

    def concatenate_vals(self, var1, var2):
        print(var1 + var2)

    def concatenate_vals_return(self, var1, var2) -> str:
        return var1 + var2


class TestRPAUtilClass(TestUtilClass):
    def __init__(self):
        pass

    def set_vars(self, var1, var2):
        self.var1 = var1
        self.var2 = var2



