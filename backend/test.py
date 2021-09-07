from src  import api_app 

Drink = api_app.Drink
db = api_app.db

# cola = Drink(title='cola', recipe='{"color":"black", "name":"cola", "parts":"60"}')
# cola.insert()

f = Drink.query.get(1)
print(f.short())
print(f.long())

# f.delete()