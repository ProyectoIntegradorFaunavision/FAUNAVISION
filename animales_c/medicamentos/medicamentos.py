class Medicamentos:
    def __init__(self,id_medicamento,nombre_medicamento,tipo,laboratorio,stock,descripción):
        self._id_medicamento=id_medicamento
        self._nombre_medicamento=nombre_medicamento
        self._tipo=tipo
        self._laboratorio=laboratorio
        self._stock=stock
        self._descripcion=descripción

    @property
    def id_medicamento(self):
        return self._id_medicamento
    @property 
    def nombre_medicamento(self):
        return self._nombre_medicamento
    @property
    def tipo(self):
        return self._tipo
    @property
    def laboratorio(self):
        return self._laboratorio
    @property
    def stock(self):
        return self._stock
    @property
    def descripcion(self):
        return self._descripcion
    @id_medicamento.setter
    def id_medicamento(self, id_medicamento):
        self._id_medicamento = id_medicamento
    @nombre_medicamento.setter
    def nombre_medicamento(self, nombre_medicamento):
        self._nombre_medicamento = nombre_medicamento
    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo
    @stock.setter
    def stock(self, stock):
        self._stock = stock
    @descripcion.setter
    def descripcion(self, descripcion):
        self._descripcion = descripcion
        self._cantConcentrado=cantConcentrado        
  
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


