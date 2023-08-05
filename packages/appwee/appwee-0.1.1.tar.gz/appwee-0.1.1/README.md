# Appwee
peewee wrapper with simple QoL changes
## Installation
```
python -m pip install appwee
```
## Quickstart
```python
import appwee
app = appwee.App(appwee.SqliteDatabase("example.db"))
class ExampleModel(app.Model):
    it_is_just = appwee.IntegerField()
    like_normal_peewee = appwee.BlobField()

if __name__ == "__main__":
    app.init()
```
See [peewee's documentation](https://docs.peewee-orm.com) for more information