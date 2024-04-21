from django.db import models

# Create your models here.
class users(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
class category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class cars(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    daily_price = models.IntegerField()

    def __str__(self):
        return f"{self.brand} - {self.model}"

class rentals(models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    car = models.ForeignKey(cars, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auto kikolcsonozve {self.users.username} altal a kovetkezo gepjarmu: - {self.cars.brand} {self.cars.model} ettol:  {self.from_date} eddig:  {self.to_date}"
    
class sales(models.Model):
    car = models.ForeignKey(cars, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    percent = models.IntegerField()

    def __str__(self):
        return f"{self.percent}% akcio a {self.cars.brand} {self.cars.model} gepjarmuvon"