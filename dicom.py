import os
import pydicom
from pydicom.errors import InvalidDicomError
import numpy as np
import pandas as pd


class ProcesadorDICOM:

    def __init__(self, sort_by="IntensidadPromedio", ascending=False):
        self.sort_by = sort_by
        self.ascending = ascending
        self.registros = []
        self.df = pd.DataFrame()

    def es_dicom(self, ruta):
        try:
            with open(ruta, "rb") as f:
                f.seek(128)
                return f.read(4) == b"DICM"
        except:
            return False

    def _safe_get(self, ds, tag):
        try:
            val = ds.get(tag, "N/A")
            return str(val) if val is not None else "N/A"
        except:
            return "N/A"

    def extraer_datos_desde_ds(self, ds):
        return {
            "PacienteID": self._safe_get(ds, "PatientID"),
            "PacienteNombre": self._safe_get(ds, "PatientName"),
            "EstudioUID": self._safe_get(ds, "StudyInstanceUID"),
            "DescripcionEstudio": self._safe_get(ds, "StudyDescription"),
            "FechaEstudio": self._safe_get(ds, "StudyDate"),
            "Modalidad": self._safe_get(ds, "Modality"),
            "Filas": self._safe_get(ds, "Rows"),
            "Columnas": self._safe_get(ds, "Columns"),
        }

    def procesar_directorio(self, directorio):
        self.registros = []

        for root, _, files in os.walk(directorio):
            for f in files:
                ruta = os.path.join(root, f)

                try:
                    ds = pydicom.dcmread(ruta)
                except:
                    continue

                datos = self.extraer_datos_desde_ds(ds)

                try:
                    arr = ds.pixel_array.astype(np.float32)
                    datos["IntensidadPromedio"] = float(np.mean(arr))
                except:
                    datos["IntensidadPromedio"] = "N/A"

                datos["Archivo"] = ruta
                self.registros.append(datos)

        self.df = pd.DataFrame(self.registros)

        if not self.df.empty and self.sort_by in self.df.columns:
            self.df = self.df.sort_values(by=self.sort_by,
                                          ascending=self.ascending).reset_index(drop=True)

    def mostrar(self):
        if self.df.empty:
            print("\n No se encontraron archivos DICOM válidos.\n")
            return

        print("\n RESULTADOS DICOM ENCONTRADOS:\n")
        print(self.df.to_string(index=False))
        print("\nTotal archivos:", len(self.df))

if __name__ == "__main__":

    ruta_default = r"C:\Users\Est01\Downloads\T2"

    print("\n=== PROCESADOR DICOM ===")
    print("Presiona ENTER para usar la ruta por defecto:")
    print(f"Ruta por defecto: {ruta_default}\n")

    ruta_input = input("Ingrese ruta o ENTER: ").strip()

    ruta = ruta_default if ruta_input == "" else ruta_input

    proc = ProcesadorDICOM()
    proc.procesar_directorio(ruta)
    proc.mostrar()
