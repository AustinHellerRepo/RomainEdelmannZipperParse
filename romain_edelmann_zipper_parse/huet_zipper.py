# based largely on scala code from Romain Edelmann "Efficient Parsing with Derivatives and Zippers"
# https://infoscience.epfl.ch/record/287059


from __future__ import annotations
from abc import ABC, abstractmethod


class Tree(ABC):

    pass


class Branch(Tree):

    def __init__(self, *, left: Tree, right: Tree):

        self.__left = left
        self.__right = right

    def get_left(self) -> Tree:
        return self.__left

    def get_right(self) -> Tree:
        return self.__right


class Leaf(Tree):

    def __init__(self, *, value: object):

        self.__value = value

    def get_value(self) -> object:
        return self.__value


class Context(ABC):

    pass


class EmptyContext(Context):

    pass


class InLeftContext(Context):

    def __init__(self, *, right: Tree, parent: Context):

        self.__right = right
        self.__parent = parent

    def get_right(self) -> Tree:
        return self.__right

    def get_parent(self) -> Context:
        return self.__parent


class InRightContext(Context):

    def __init__(self, *, left: Tree, parent: Context):

        self.__left = left
        self.__parent = parent

    def get_left(self) -> Tree:
        return self.__left

    def get_parent(self) -> Context:
        return self.__parent


class Zipper():

    def __init__(self, *, focus: Tree, context: Context = EmptyContext()):

        self.__focus = focus
        self.__context = context

    def unfocus(self) -> Tree:
        if isinstance(self.__context, EmptyContext):
            return self.__focus
        elif isinstance(self.__context, InLeftContext):
            return Zipper(
                focus=Branch(
                    left=self.__focus,
                    right=self.__context.get_right()
                ),
                context=self.__context.get_parent()
            ).unfocus()
        elif isinstance(self.__context, InRightContext):
            return Zipper(
                focus=Branch(
                    left=self.__context.get_left(),
                    right=self.__focus
                ),
                context=self.__context.get_parent()
            ).unfocus()
        else:
            raise Exception(f"Unexpected condition")

    def move_up(self) -> Zipper:
        if isinstance(self.__context, EmptyContext):
            return self
        elif isinstance(self.__context, InLeftContext):
            return Zipper(
                focus=Branch(
                    left=self.__focus,
                    right=self.__context.get_right()
                ),
                context=self.__context.get_parent()
            )
        elif isinstance(self.__context, InRightContext):
            return Zipper(
                focus=Branch(
                    left=self.__context.get_left(),
                    right=self.__focus
                ),
                context=self.__context.get_parent()
            )
        else:
            raise Exception(f"Unexpected condition")

    def move_left(self) -> Zipper:
        if isinstance(self.__focus, Leaf):
            return self
        elif isinstance(self.__focus, Branch):
            return Zipper(
                focus=self.__focus.get_left(),
                context=InLeftContext(
                    right=self.__focus.get_right(),
                    parent=self.__context
                )
            )
        else:
            raise Exception(f"Unexpected condition")

    def move_right(self) -> Zipper:
        if isinstance(self.__focus, Leaf):
            return self
        elif isinstance(self.__focus, Branch):
            return Zipper(
                focus=self.__focus.get_right(),
                context=InRightContext(
                    left=self.__focus.get_left(),
                    parent=self.__context
                )
            )
        else:
            raise Exception(f"Unexpected condition")

    def is_focus_leaf(self) -> bool:
        return isinstance(self.__focus, Leaf)

    def get_leaf_value(self) -> object:
        if not isinstance(self.__focus, Leaf):
            raise Exception(f"Focus is not currently a leaf")
        else:
            return self.__focus.get_value()
