from medicamentos import medicamentos
from animales_cautiverio import animales_cautiverio
from veterinarios import veterinarios
class Expedientes(animales_cautiverio.AnimalesC,medicamentos.Medicamentos,veterinarios.Veterinarios):
    def __init__(self,id,especie,peso,edad,talla,observaciones,codigo,medicamento,stock,principioActivo,cantConcentrado,
                    tamano,viaAdm,nombre,apellido1,apellido2,cargo,calle,col,num,codigo_postal,telefono,correo,folio,
                    animal,veterinario,medi,fechaAplicacion, fechaProxima,dosis,anotaciones):
        animales_cautiverio.AnimalesC.__init__(self,id,especie,peso,edad,talla,observaciones)
        medicamentos.Medicamentos.__init__(self,codigo,medicamento,stock,principioActivo,cantConcentrado,tamano,viaAdm)
        veterinarios.Veterinarios.__init__(self,nombre,apellido1,apellido2,cargo,calle,col,num,codigo_postal,telefono,correo)
        self._folio=folio
        self._animal=animal
        self._veterinario=veterinario
        self._medi=medi
        self._fechaAplicacion=fecha
        self._fechaProxima=fechaProxima
        self._dosis=dosis
        self._anotaciones=anotaciones

    @property
    def folio(self):
        pass
    @property
    def f_apli(self):
        pass
    @property
    def f_proxima(self):
        pass
    @property
    def dosis(self):
        pass
    @property
    def observaciones(self):
        pass

    @folio.setter
    def folio(self):
        pass

    @f_apli.setter
    def f_apli(self):
        pass

    @f_proxima.setter
    def f_proxima(self):
        pass

    @dosis.setter
    def dosis(self):
        pass

    @observaciones.setter
    def observaciones(self):
        pass
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
