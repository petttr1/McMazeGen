from abc import ABC, abstractmethod


class ChestItem(ABC):
    def __init__(self):
        self.tag = {}
        super().__init__()

    @abstractmethod
    def generate_item_string(self, item, slot):
        return {'id': item.id, 'Count': item.count, 'tag': item.tag}

    @abstractmethod
    def enchant(self):
        pass
