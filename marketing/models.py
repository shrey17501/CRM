from django.db import models


class Lead(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name =  models.CharField(max_length=50)
	email =  models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address =  models.CharField(max_length=100)
	city =  models.CharField(max_length=50)
	state =  models.CharField(max_length=50)
	zipcode =  models.CharField(max_length=20)
	discription = models.CharField(max_length=1000)
	status = models.CharField(max_length=200, null=True, choices=(
        ('COLD','COLD'),
        ('DEAD','DEAD'),
        ('POTENTIAL','POTENTIAL'),
        ('CONVERTED','CONVERTED'),
	))
	total_payment = models.CharField(max_length=100, default='0')
	payment_status = models.CharField(max_length=200, null=True, choices=(
        ('RECIEVED','RECIEVED'),
        ('LEFT','LEFT'),
	))

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")
