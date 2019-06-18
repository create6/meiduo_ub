# from random import Random
#
# from Cryptodome.PublicKey import RSA
# from django.conf import settings
#
# # random_generator = Random.new().read
# Random random_generator = new Random()
#
#
# rsakey = RSA.generate(1024, random_generator)
# # f=open(email+'.pem','wb')
# f=open(settings.APLIPAY_PRIVATE_KEY,'wb')
#
# f.write(rsakey.exportKey("PEM"))
# f.write(rsakey.publickey().exportKey("PEM"))
# f.close()