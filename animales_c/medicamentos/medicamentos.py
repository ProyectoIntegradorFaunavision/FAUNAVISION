class Medicamentos:
    def __init__(self,codigo,nombre,stock,principioActivo,cantConcentrado,tamano,viaAdm):
        self._codigo=codigo
        self._nombre=nombre
        self._stock=stock
        self._principioActivo=principioActivo
        self._cantConcentrado=cantConcentrado
        self._tamano=tamano
        self._viaAdm=viaAdm

    @property
    def codigo(self):
        return self._codigo
    @property 
    def cantConcentrado(self):
        return self._cantConcentrado
    @property
    def nombre(self):
        return self._nombre
    @property
    def stock(self):
        return self._stock
    @property
    def tamano(self):
        return self._tamano
    @property
    def principioActivo(self):
        return self._principioActivo
    @property
    def viaAdm(self):
        return self._viaAdm
    @codigo.setter
    def codigo(self,codigo):
        self._codigo=codigo        
    @nombre.setter
    def nombre(self,nombre):
        self._nombre=nombre        
    @stock.setter
    def stock(self,stock):
        self._stock=stock
    @princio_activo.setter
    def princio_activo(self,principioActivo):
        self._principioActivo=principioActivo
    @cantConcentrado.setter
    def cantConcentrado(self,cantConcentrado):
        self._cantConcentrado=cantConcentrado        
    @tamano.setter
    def tamano(self):
        self._tamano=tamano
    @viaAdm.setter
    def viaAdm(self,viaAdm):
        self._viaAdm=viaAdm


      
    def agregar(self):
        pass
    def actualizar(self):
        pass  
    def borrar(self):
        pass
    def mostrar(self):
        pass
    def limpiar(self):
        pass

