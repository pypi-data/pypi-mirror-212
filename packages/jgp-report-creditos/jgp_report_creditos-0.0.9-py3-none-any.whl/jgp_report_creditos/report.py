#!/usr/bin/env python3
from .core.contrato.v1.contratos import ContratoPersonal, ContratoConvenio, ContratoConvenioCustodiaInmueble, ContratoConvenioCustodiaVehiculo, ContratoCustosiaInmueblePampahasi, ContratoDocumentoCustodiaVehiculo, ContratoOtroDocumentoCustodiaPatente, ContratoPersonalDocumentosCustodiaVehiculo, ContratoQuirografariaOficinaElCarmen, ContratoSolidario, ContratoConvenioGarantiaPersonal, ContratoPrendariayPersonal, ContratoErrorBase

def makeContato(object_json):
        #CONVIERTO EL JSON EN LIBRERIA
        contrato = object_json
        #SACO EL NOMBRE DEL DOCUMENTO---(descriptión)
        print("DDDDDDDDDDDDDDDDDDDDDDDDdd", contrato)
        tipo_garantia_=contrato["tipo_garantia"]
        print(tipo_garantia_)
        description=tipo_garantia_["descripcion"]
        print(description)
        #GENERO LOS PDF
        if description == "Personal":
            contrato_personal = ContratoPersonal(contrato)    
            return contrato_personal.generar1()

        elif description == "Solidario":
            contrato_solidario = ContratoSolidario(contrato)    
            return contrato_solidario.generar1()

        elif description == "Quirografaria":
            contrato_quirografaria_carmen = ContratoQuirografariaOficinaElCarmen(contrato)    
            return contrato_quirografaria_carmen.generar1()

        elif description == "Convenio":
            contrato_convenio = ContratoConvenio(contrato)  
            x = contrato_convenio.generar1()
            return x
            
        elif description == "Personal y Doc. custodia Vehiculo":
                contrato_personal_documento_custodia_vehiculo = ContratoPersonalDocumentosCustodiaVehiculo(contrato)    
                return contrato_personal_documento_custodia_vehiculo.generar1()
        
        elif description == "Doc. Custodia de Inmueble":
            contrato_custodia_inmueble_pampahasi = ContratoCustosiaInmueblePampahasi(contrato)    
            return contrato_custodia_inmueble_pampahasi.generar1()
            
        elif description == "Doc. Custodia de Vehiculo":
            contrato_documento_custodia_vehiculo = ContratoDocumentoCustodiaVehiculo(contrato)    
            return contrato_documento_custodia_vehiculo.generar1()

        elif description == "Otros Doc. En Custodia":
            contrato_otros_documentos_custodia_patente = ContratoOtroDocumentoCustodiaPatente(contrato)    
            return contrato_otros_documentos_custodia_patente.generar1()

        elif description == "Convenio y Doc. Custodia Inmueble":
            contrato_convenio_doc_custodia_inmueble = ContratoConvenioCustodiaInmueble(contrato)    
            return contrato_convenio_doc_custodia_inmueble.generar1()
            
        elif description == "Convenio y Doc. Custodia Vehiculo":
                contrato_convenio_doc_custodia_vehiculo = ContratoConvenioCustodiaVehiculo(contrato)    
                return contrato_convenio_doc_custodia_vehiculo.generar1()

        # 11 CONVENIO Y GARANTIA PERSONAL
        elif description == "Convenio y Garantia personal":
                contrato_convenio_garantia_personal = ContratoConvenioGarantiaPersonal(contrato)    
                return contrato_convenio_garantia_personal.generar1()
        
        # 12 PRENDARIA Y PERSONAL
        elif description == "Prendaria y Personal":
                contrato_garante_depositario = ContratoPrendariayPersonal(contrato)    
                return contrato_garante_depositario.generar1()            

        else:
            print("ªªªªªªªªª No se encontro el tipo de garantia ªªªªªªªªªªªªªªªªªª")
            contrato_error_base = ContratoErrorBase(contrato)    
            return contrato_error_base.generar1() 
            
    
