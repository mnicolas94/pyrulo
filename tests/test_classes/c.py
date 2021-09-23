from tests.test_classes.a import A


class C(A):

    def f(self):
        return A.f(self) + ".c"
