class Expedientes():
    def __init__(self,id_historial,animal,veterinario,medicamento,fechaAplicacion,fechaProxima,tipo_evento,peso_actual,diagnostico_motivo):
        self._id_historial=id_historial
        self._animal=animal
        self._veterinario=veterinario
        self._medicamento=medicamento
        self._fechaAplicacion=fechaAplicacion
        self._fechaProxima=fechaProxima
        self._tipo_evento=tipo_evento
        self._peso_actual=peso_actual
        self._diagnostico_motivo=diagnostico_motivo
    @property
    def id_historial(self):
        return self._id_historial 
    @property
    def animal(self):
        return self._animal
    @property
    def veterinario(self):
        return self._veterinario
    @property
    def medicamento(self):
        return self._medicamento
    @property
    def fechaAplicacion(self):
        return self._fechaAplicacion
    @property
    def fechaProxima(self):
        return self._fechaProxima  
    @property
    def tipo_evento(self):
        return self._tipo_evento     
    @property
    def peso_actual(self):
        return self._peso_actual
    @property
    def diagnostico_motivo(self):
        return self._diagnostico_motivo

    @id_historial.setter
    def id_historial(self, id_historial):
        self._id_historial = id_historial
    @fechaAplicacion.setter
    def fechaAplicacion(self, fechaAplicacion):
        self._fechaAplicacion = fechaAplicacion

    @fechaProxima.setter
    def fechaProxima(self, fechaProxima):
        self._fechaProxima = fechaProxima
    @tipo_evento.setter
    def tipo_evento(self, tipo_evento):
        self._tipo_evento = tipo_evento
    @peso_actual.setter
    def peso_actual(self, peso_actual):
        self._peso_actual = peso_actual 

    @diagnostico_motivo.setter
    def diagnostico_motivo(self, diagnostico_motivo):
        self._diagnostico_motivo = diagnostico_motivo   

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

