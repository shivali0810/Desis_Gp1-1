from django.db import models
from django.contrib.auth.models import Permission, Group, AbstractUser, BaseUserManager


'''
NgoManager class inherits from Django's BaseUserManager class and is responsible for creating and managing instances of the customaised user model: ngo.
It has an additional feature of setting is_ngo True whenever a ngo registers 
It returns an instance of ngo user
'''
class NgoManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email is required')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_ngo = True
        user.save(using=self._db)
        return user    


'''
DonorManager class inherits from Django's BaseUserManager class and is responsible for creating and managing instances of the customaised user model: donor.
It has an additional feature of setting is_ngo False whenever a donor registers 
It returns an instance of donor user
It is also used to create superuser to manage the administration
'''
class DonorManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email is required')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_ngo = False
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    

''' 
pincode model is used to store this information in normalized and efficient way.
''' 
class pincode(models.Model):
    code = models.IntegerField(default=248001)
    city = models.CharField(max_length=250,default="es")
    state= models.CharField(max_length=250,default="qw")
    def __str__(self):
        return self.city
    

''' 
ngo Class is model used to represent an ngo in our application.

It is child class of AbstractUser inheritiong:
   - the fields username, password, email
   - methods for handling passwords, including password hashing and validation 
   - built-in managers for creating, querying, and modifying user objects

Thus, by inheriting from AbstractUser, we are able to use the built-in authentication and permission features provided by Django, 
while customizing the model with additional fields and functionality specific to NGOs.
'''  
class ngo(AbstractUser):
    ngo_name = models.CharField(max_length=255,default="a")
    email = models.EmailField(max_length=55,default="b")
    phone_no = models.IntegerField(default=123456789)
    is_ngo = models.BooleanField(default=True)
    points = models.PositiveBigIntegerField(default=500)
    longitude = models.DecimalField(decimal_places=10,max_digits=15,default=0.000)
    latitude = models.DecimalField(decimal_places=10,max_digits=15,default=0.000)
    pincode = models.ForeignKey(pincode, on_delete=models.CASCADE,null=True)
    groups = models.ManyToManyField(Group, related_name='ngo_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='ngo_user_permissions',
    )
    objects = NgoManager()

    def __str__(self):
        return self.ngo_name


'''
The same goes for donor Class which is used to represent a donor in our application
It has a function donations_made to return all donations made by that particular user
'''  
class donor(AbstractUser):
    donor_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=55)
    phone_no = models.IntegerField(default=123456789)
    points = models.PositiveBigIntegerField(default=0)
    longitude = models.DecimalField(decimal_places=10,max_digits=15,default=0.000)
    latitude = models.DecimalField(decimal_places=10,max_digits=15,default=0.000)
    pincode = models.ForeignKey(pincode, on_delete=models.CASCADE,null=True)
    is_ngo = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='donor_groups')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='donor_user_permissions',
    )

    objects = DonorManager()
    def __str__(self):
        return self.donor_name
    
    def donations_made(self):
        return donations.objects.filter(donor_id=self.id)

'''
This Class which is used to represent donation made by any donor.

    - donor_id maps this donation to the donor who has made it
    - ngo_id maps this donation to the ngo who will take it
    - status is a bool flag representing if donor has donated the donation
    - status2 is a bool flag representing if ngo has recieved the donation, depending on these two we transfer coins from ngo to donor
''' 
class donations(models.Model):
    id = models.AutoField(primary_key=True)
    donor_id = models.ForeignKey(donor, on_delete=models.CASCADE)
    ngo_id = models.ForeignKey(ngo, on_delete=models.CASCADE, related_name='ngo_donations', blank=True, null=True)
    donation_date = models.DateField(null=True)
    exp_date = models.DateField()
    longitude = models.DecimalField(decimal_places=10,max_digits=15)
    latitude = models.DecimalField(decimal_places=10,max_digits=15)
    pincode = models.ForeignKey("pincode", on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=10)
    desc = models.TextField(default="description")
    status = models.BooleanField(default=True)
    status2 = models.BooleanField(default=True)
  
    def __str__(self):
        return self.desc

class Redemption(models.Model):
    donor = models.ForeignKey(donor, on_delete=models.CASCADE)
    points = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
# {% extends 'auth1/base.html' %}
# {% load static %}
# {% block extra_head %}
#     <link rel="stylesheet" href="{% static 'images/styles.css' %}">
# {% endblock %}

# {% block content %}
#     <div class="container">
#       <div class="row justify-content-center">
#         <div class="col-md-6">
#           <div class="card">
#             <div class="card-header">
#               <h2>Sign up</h2>
#             </div>
#             <div class="card-body">
#               <form method="post">
#                 {% csrf_token %}
#                 {{ form.as_p }}
#                 <button type="submit" class="btn btn-primary">Sign up</button>
#               </form>
#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
# {% endblock %} 


