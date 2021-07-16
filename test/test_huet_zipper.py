from romain_edelmann_zipper_parse.huet_zipper import Zipper, Branch, Leaf
import random
import time


if False:
    _tree = Branch(
        left=Branch(
            left=Leaf(
                value=0
            ),
            right=Leaf(
                value=1
            )
        ),
        right=Branch(
            left=Leaf(
                value=2
            ),
            right=Leaf(
                value=3
            )
        )
    )
else:
    _tree = Branch(
        left=Branch(
            left=Leaf(
                value=0
            ),
            right=Leaf(
                value=1
            )
        ),
        right=Leaf(
            value=2
        )
    )


_zipper = Zipper(
    focus=_tree
)


_leaf_visits_per_leaf_value = {}
_visits_total = 0

for _is_move_up_permitted in (True, False):
    if _is_move_up_permitted:
        print("Move up permitted")
    else:
        print("Move up not permitted")
    for _index in range(100000):
        if _is_move_up_permitted:
            _choice = random.randrange(3)
        else:
            _choice = random.randrange(2) + 1
        if _choice == 0:
            _zipper = _zipper.move_up()
        elif _choice == 1:
            _zipper = _zipper.move_left()
            if _zipper.is_focus_leaf():
                _value = _zipper.get_leaf_value()
                if _value not in _leaf_visits_per_leaf_value:
                    _leaf_visits_per_leaf_value[_value] = 0
                _leaf_visits_per_leaf_value[_value] += 1
                _visits_total += 1
                _zipper = Zipper(
                    focus=_zipper.unfocus()
                )
        elif _choice == 2:
            _zipper = _zipper.move_right()
            if _zipper.is_focus_leaf():
                _value = _zipper.get_leaf_value()
                if _value not in _leaf_visits_per_leaf_value:
                    _leaf_visits_per_leaf_value[_value] = 0
                _leaf_visits_per_leaf_value[_value] += 1
                _visits_total += 1
                _zipper = Zipper(
                    focus=_zipper.unfocus()
                )

    for _value in _leaf_visits_per_leaf_value.keys():
        _average_visits = _leaf_visits_per_leaf_value[_value]/_visits_total
        print(f"Value average: {_value} was visited {_average_visits}")
