class AnimalesC:
    def __init__(self,id,especie,peso,edad,talla,observaciones):
        self._id=id
        self._especie=especie
        self._peso=peso
        self._edad=edad
        self._talla=talla
        self._observaciones=observaciones
    @property
    def id(self):
        return self._id
    @property 
    def especie(self):
        return self._especie
    @property
    def peso(self):
        return self._peso
    @property
    def edad(self):
        return self._edad
    @property
    def talla(self):
        return self._talla
    @property
    def observaciones(self):
        return self._observaciones
    @id.setter
    def id(self,id):
        self._id=id
    @especie.setter
    def especie(self,especie):
        self._especie=especie
    @peso.setter
    def peso(self,peso):
        self._peso
    @edad.setter
    def edad(self,edad):
        self._edad
    @talla.setter
    def talla(self,talla):
        self._talla=talla
    @observaciones.setter
    def observaciones(self,observaciones):
        self._observaciones=observaciones


