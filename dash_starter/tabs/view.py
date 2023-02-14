from database import DataHolder

class View():
    def get_layout(self, data_holder: DataHolder):
        raise NotImplementedError

    def update_layout(self, data_holder: DataHolder, *args, **kwargs):
        raise NotImplementedError
