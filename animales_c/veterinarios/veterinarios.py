import conexionBD

class Veterinarios:
    def __init__(self,nombre,apellido1,apellido2,cargo,calle,col,num,codigo_postal,telefono,correo):
        self._nombre=nombre
        self._apellido1=apellido1
        self._apellido2=apellido2
        self._cargo=cargo
        self._calle=calle
        self._col=col
        self._num=num
        self._codigo_postal=codigo_postal
        self._telefono=telefono
        self._correo=correo

    @property
    def nombre(self):
        return self._nombre
    @property
    def apellido1(self):
        return self._apellido1
    @property
    def apellido2(self):
        return self._apellido2
    @property
    def cargo (self):
        return self._cargo
    @property
    def calle (self):
        return self._calle
    @property
    def col (self):
        return self._col
    @property
    def num (self):
        return self._num
    @property
    def codigo_postal (self):
        return self._codigo_postal
    @property
    def telefono (self):
        return self._telefono
    @property
    def correo (self):
        return self._correo
    @correo.setter
    def nombre(self,nombre):
        self._nombre=nombre
    @apellido1.setter
    def apellido1(self,apellido1):
        self._apellido1=apellido1
    @apellido2.setter
    def apellido2(self,apellido2):
        self._apellido2=apellido2
    @cargo.setter
    def cargo (self,cargo):
        self._cargo=cargo
    @calle.setter
    def calle (self,calle):
        self._calle=calle
    @col.setter
    def col (self,col):
        self._col=col
    @num.setter
    def num (self,num):
        self._num=num
    @codigo_postal.setter
    def codigo_postal (self,codigo_postal):
        self._codigo_postal=codigo_postal
    @correo.setter
    def correo (self,correo):
        self._correo=correo
    @telefono.setter
    def telefono (self,telefono):
        self._telefono=telefono
