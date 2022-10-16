from os import remove
from addons import *
clear()
Master_password=str()
primary_color='cyan'

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b85encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b85decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class KeyProcess:
	def __init__(self):
		self.path_dir=open("data/path_dir","r").read()

	def encrypt(self,raw_password,key):
		aes=AESCipher(key)
		raw_encrypted_password=aes.encrypt(raw_password)
		t=str(raw_encrypted_password)
		splitted_encrypted_password=(t.split("'")[-2])#splitting raw_encrypted_password
		return splitted_encrypted_password

	def decrypt(self,key,path):
		aes=AESCipher(key)
		path=open(path,'r')
		encrypted_password=path.read()#opening encrypted password from root
		decrypted_password=aes.decrypt(encrypted_password)
		if decrypted_password:return decrypted_password #return if the string is not empty
		return '********'

	def encrypt_password(self,raw_password,key,path):

		aes=AESCipher(key)
		iteration=choice(['6','5','6','7','8','9','10'])

		encrypted_password=raw_password
		for i in range(int(iteration)):
			encrypted_password=aes.encrypt(encrypted_password)
			encrypted_password=str(encrypted_password)
			encrypted_password=(encrypted_password.split("'")[-2])
		
		encrypted_iteration=aes.encrypt(iteration)
		encrypted_iteration=str(encrypted_iteration)
		encrypted_iteration=(encrypted_iteration.split("'")[-2])

		open(f"{path}/iterables",'w+').write(encrypted_iteration)
		open(f"data/exc.pyc",'w+').write(f'|?~p~;{encrypted_password}|?~p~;')

		compress(['data/exc.pyc'],f'{path}/password.psl',b"passlock")
		os.remove("data/exc.pyc")

		return encrypted_password

	def decrypt_password(self,key,path):
		try:
			aes=AESCipher(key)
			iteration=open(f"{path}/iterables",'r').read()
			iteration=aes.decrypt(iteration)
			iteration=int(iteration)
			password=open(f"{path}/password.psl",'rb').read()
			password=str(password)
			decrypted_password=(password.split("|?~p~;")[-2])	

			for i in range(iteration):
				decrypted_password=aes.decrypt(decrypted_password)
				decrypted_password=str(decrypted_password)

			if decrypted_password:return decrypted_password #return if the string is not empty
			return '********'
		except ValueError:return '********'

	def reencrypt_password(self,id,password,key):
		aes=AESCipher(key)
		reencrypted_password=aes.encrypt(password)
		root=open(f"{self.path_dir}\\{id}\\password",'w')
		t=str(reencrypted_password)
		splitted_reencrypted_password=(t.split("'")[-2])
		root.write(splitted_reencrypted_password)
