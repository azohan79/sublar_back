from collections import deque
from .models import TeamPlacement

def place_in_tree(sponsor, new_user, side='L'):
    """
    Ищет первую свободную ячейку в ветви side (L или R) для new_user, начиная от sponsor, используя BFS.
    Возвращает кортеж (True, сообщение, уровень) при успехе или (False, сообщение, None) при неудаче.
    """
    queue = deque()
    queue.append((sponsor, 1))  # Начинаем с уровня 1

    while queue:
        current_sponsor, level = queue.popleft()
        # Если у текущего узла на стороне side нет записи – место свободно
        if not TeamPlacement.objects.filter(sponsor=current_sponsor, side=side).exists():
            TeamPlacement.objects.create(
                sponsor=current_sponsor,
                child=new_user,
                side=side,
                level=level
            )
            return (True, f"Пользователь поставлен на уровне {level} в ветке {side}", level)
        else:
            # Если место занято, добавляем ребёнка, занимающего это место, в очередь для поиска на следующем уровне
            placement = TeamPlacement.objects.get(sponsor=current_sponsor, side=side)
            child_user = placement.child
            queue.append((child_user, level + 1))
    return (False, "Нет свободного места", None)

def build_tree(user):
    """
    Рекурсивно строит дерево партнеров для заданного пользователя.
    """
    left_placement = user.placements_as_sponsor.filter(side='L').first()
    right_placement = user.placements_as_sponsor.filter(side='R').first()

    return {
        "user": user,
        "left": build_tree(left_placement.child) if left_placement else None,
        "right": build_tree(right_placement.child) if right_placement else None,
    }