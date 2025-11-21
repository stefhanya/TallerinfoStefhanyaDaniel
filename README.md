<p align="center">
  <img src="udea.jpg" width="180" alt="Escudo UdeA">
</p>
# Procesador de Archivos DICOM 

## 1. Descripción del proyecto

Este proyecto desarrolla una aplicación en Python orientada a automatizar la **lectura**, **extracción**, **procesamiento** y **organización** de información proveniente de archivos médicos en formato **DICOM (Digital Imaging and Communications in Medicine)**.

La aplicación implementa la clase `ProcesadorDICOM`, que utiliza:

- **pydicom** para leer los archivos DICOM, acceder a sus metadatos y validar su estructura.
- **numpy** para realizar análisis básicos de la imagen, incluyendo el cálculo de la **intensidad promedio** de los valores del pixel array.
- **pandas** para almacenar y estructurar los metadatos extraídos dentro de un **DataFrame**, lo que permite su consulta, filtrado y análisis de forma más cómoda.

El flujo del programa simula el proceso básico de un sistema PACS (Picture Archiving and Communication System):

1. Escanear un directorio.
2. Identificar archivos DICOM válidos.
3. Extraer metadatos clínicos importantes como:
   - ID del paciente,
   - Nombre del paciente,
   - UID del estudio,
   - Descripción del estudio,
   - Modalidad,
   - Fecha del estudio,
   - Dimensiones de la imagen (filas y columnas).
4. Procesar el pixel array para obtener la **IntensidadPromedio**.
5. Organizar toda la información dentro de un DataFrame.
6. Mostrar los resultados de forma ordenada y legible.

De esta manera, se replica en pequeña escala el funcionamiento de sistemas reales de imagenología médica.

---

## 2. Importancia de DICOM y HL7 para la interoperabilidad en salud y diferencias conceptuales

###  Importancia de la interoperabilidad

En el área de informática médica, la **interoperabilidad** es la capacidad de distintos sistemas (HIS, PACS, RIS, LIS, EHR) para **intercambiar información de manera efectiva, segura y estandarizada**.  
Para lograrlo, se utilizan estándares internacionales como **DICOM** y **HL7**, cada uno con un propósito diferente pero complementario.

---

###  DICOM 

- Es el estándar universal para **imágenes médicas**.
- Define tanto el **formato del archivo** como los **protocolos de comunicación** entre dispositivos.
- Permite que máquinas como TAC, resonancia magnética, rayos X, ecografía, PET o mamografías puedan:
  - guardar imágenes,
  - enviarlas a un PACS,
  - compartirlas con estaciones de trabajo,
  - mantener metadatos clínicos incrustados.

**Claves de DICOM:**

- Maneja imágenes como matrices numéricas (pixel array).
- Incluye metadatos como StudyInstanceUID, PatientID, fecha del estudio, tipo de modalidad, etc.
- Es esencial para garantizar que una imagen pueda ser usada en cualquier software compatible.

---

### HL7 

- Estándar dedicado al **intercambio de información textual y administrativa clínica**.
- Usado para transmitir:
  - datos demográficos del paciente,
  - órdenes médicas,
  - resultados de laboratorio,
  - informes clínicos,
  - admisiones, altas y transferencias.

**Claves de HL7:**

- Estructura mensajes clínicos,
- No maneja imágenes,
- Establece cómo debe formatearse la información para que distintos sistemas la interpreten igual.

---

### Diferencias conceptuales

| Característica | **DICOM** | **HL7** |
|----------------|-----------|---------|
| Enfoque | Imágenes médicas y sus metadatos | Mensajes clínicos y administrativos |
| Tipo de Datos | Archivos binarios + tags | Texto estructurado |
| Uso | Radiología, PACS, estaciones de imagen | HIS, RIS, EHR, LIS |
| Concepto | “Estándar de la imagen” | “Estándar del mensaje clínico” |

**En resumen:**  
- **DICOM** asegura que las imágenes se almacenen y transmitan correctamente.  
- **HL7** asegura que la información clínica se comunique entre sistemas.  

Ambos son esenciales para la interoperabilidad completa.

---

## 3. Relevancia clínica y de preprocesamiento del análisis de intensidades en imágenes médicas

El análisis de la distribución de intensidades en imágenes médicas es fundamental para la interpretación clínica y para el procesamiento computarizado.

En el proyecto, este análisis se representa mediante el cálculo de la columna **IntensidadPromedio**, obtenida a partir del pixel array mediante:

`python
arr = ds.pixel_array.astype(np.float32)
np.mean(arr)`

---

## 4. Dificultades encontradas e importancia de Python en análisis de datos médicos

### **Dificultades encontradas**
- **Ausencia o variabilidad de metadatos** debido a anonimización → manejado con `_safe_get`.
- **Archivos corruptos o no válidos** → controlados con bloques `try/except`.
- **Fallas al acceder a pixel_array**, especialmente en DICOM sin imagen → segundo manejo de errores en el cálculo de intensidad.
- **Estructuración de datos heterogéneos** en un DataFrame uniforme.

### **Importancia de Python**
- Ecosistema sólido: **pydicom**, **numpy**, **pandas**, entre otras.
- Sintaxis clara y soporte para Programación Orientada a Objetos.
- Integración sencilla con librerías como scikit-learn, TensorFlow y PyTorch.
- Ideal para prototipar, automatizar procesos clínicos y analizar imágenes médicas con rapidez y precisión.
