class Correo:

    def __init__(self, correo, password, url):
        self.correo = correo
        self.password = password
        self.url = url

    def __str__(self):
        return 'url; {}, correo: {}, password: {}'.format(self.url, self.correo, self.password)

    def __repr__(self):
        return self.__str__()