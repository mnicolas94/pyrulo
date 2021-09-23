from tests.test_classes.a import A


class B(A):

    def f(self):
        return A.f(self) + ".b"
