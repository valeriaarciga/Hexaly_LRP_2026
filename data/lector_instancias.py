def cargar_instancia(ruta_archivo):
    metadatos = {}
    depositos = []
    clientes = []
    seccion_actual = "meta"
    
    with open(ruta_archivo, 'r') as f:
        for linea in f:
            linea = linea.strip()
            
            # Ignorar líneas vacías o comentarios
            if not linea or linea.startswith("#"):
                continue
                
            # Detener la lectura si llegamos al final del archivo oficial
            if linea == "EOF":
                break
            
            # Detectar el cambio de sección
            if linea.startswith("DEPOT_SECTION"):
                seccion_actual = "depot"
                continue
            elif linea.startswith("CUSTOMER_SECTION"):
                seccion_actual = "customer"
                continue
            
            # Procesar la información según la sección
            partes = linea.split()
            
            if seccion_actual == "meta":
                # Leer configuraciones generales
                if len(partes) >= 3 and partes[1] == ":":
                    metadatos[partes[0]] = partes[2]
                    
            elif seccion_actual == "depot":
                # Formato: ID, X, Y, Costo_Apertura, Capacidad, ?
                depositos.append({
                    "id": int(partes[0]), 
                    "x": float(partes[1]), 
                    "y": float(partes[2]),
                    "capacidad": float(partes[3]),
                    "costo": float(partes[4])
                })
                
            elif seccion_actual == "customer":
                # Formato: ID, X, Y, Demanda
                clientes.append({
                    "id": int(partes[0]), 
                    "x": float(partes[1]), 
                    "y": float(partes[2]),
                    "demanda": float(partes[3])
                })
                
    return metadatos, depositos, clientes

# Tu ruta actual según la terminal
ruta = "data/mock/mock_small_consolidation.txt"

# Ejecutar la función
metadatos, depositos, clientes = cargar_instancia(ruta)

# Imprimir los resultados para verificar que funcionó
print("--- METADATOS ---")
print(metadatos)
print(f"\nTotal de depósitos cargados: {len(depositos)}")
print(f"Total de clientes cargados: {len(clientes)}")

print("\nEjemplo del primer cliente:")
print(clientes[0])