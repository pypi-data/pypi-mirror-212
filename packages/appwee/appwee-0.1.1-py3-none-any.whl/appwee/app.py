import peewee as _peewee

class App:
    def __init__(self, database : _peewee.Database) -> None:
        self.database = database
        self.models : list[self._base_model] = []

        class Model(_peewee.Model):
            def __init_subclass__(cls):
                _peewee.Model.__init_subclass__()
                self.models.append(cls)
                
            class Meta:
                database = self.database
        self.Model = Model

    def init(self):
        self.database.create_tables(self.models)
        return self.database

if __name__ == "__main__":
    db = _peewee.SqliteDatabase("test.db")
    app = App(db)
    class Test(app.Model):
        field = _peewee.IntegerField()
    app.init()