from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, ECemail,password=None,**extra_fields):#for creating users with this model I have to write: EducationCentre.objects.create_user()
        if not ECemail:
            raise ValueError("Email must be set")
        ECemail = self.normalize_email(ECemail)
        user = self.model(ECemail=ECemail, **extra_fields)
        user.set_password(password)#this will hash the password and save it
        user.save(using=self._db)#usually, using is iqual to None, So it will be equal to default database(in settings file)
        return user

    def create_superuser(self,ECemail, password=None, **extra_fields):
        user = self.create_user(ECemail, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user