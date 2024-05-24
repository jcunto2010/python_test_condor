from itertools import permutations
from collections import Counter


# Función para verificar si un número es primo
def es_primo(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def verificar_condiciones_adicionales(digitos):
    # Verificar que todos los 8 estén juntos
    indices_8 = [i for i, x in enumerate(digitos) if x == 8]
    if indices_8 and (max(indices_8) - min(indices_8) + 1 != len(indices_8)):
        return False

    # Verificar que todos los 9 estén separados por un número único
    indices_9 = [i for i, x in enumerate(digitos) if x == 9]
    if indices_9:
        for i in range(len(indices_9) - 1):
            if digitos[indices_9[i] + 1] != digitos[indices_9[i + 1] - 1] or digitos[indices_9[i] + 1] in [8, 9]:
                return False

    # Verificar que dos números diferentes aparezcan dos veces cada uno y estén separados por al menos un 8
    contador = Counter(digitos)
    numeros_dobles = [num for num, count in contador.items() if count == 2]
    if len(numeros_dobles) >= 2:
        num1, num2 = numeros_dobles[0], numeros_dobles[1]
        indices_num1 = [i for i, x in enumerate(digitos) if x == num1]
        indices_num2 = [i for i, x in enumerate(digitos) if x == num2]
        if not any(digitos[min(i, j):max(i, j)].count(8) > 0 for i in indices_num1 for j in indices_num2):
            return False

    # Verificar que todos los 3 estén rodeados por el mismo número
    indices_3 = [i for i, x in enumerate(digitos) if x == 3]
    if indices_3:
        numero_rodante = digitos[indices_3[0] - 1] if indices_3[0] > 0 else digitos[indices_3[0] + 1]
        if not all(
                (digitos[i - 1] if i > 0 else None) == numero_rodante and (
                digitos[i + 1] if i < len(digitos) - 1 else None) == numero_rodante
                for i in indices_3
        ):
            return False

    return True


def construir_prefijos(digitos):
    # Prefijos de teléfonos móviles de Venezuela
    prefijos_venezolanos = {"0412", "0424", "0426", "0416", "0414"}

    # Convertir los prefijos a cadenas para facilitar la comparación
    prefijos_venezolanos = set(prefijos_venezolanos)

    # Lista para almacenar los prefijos encontrados y sus posiciones
    prefijos_encontrados = []

    # Generar todas las permutaciones posibles de 4 dígitos con sus índices
    for permutacion in permutations(enumerate(digitos), 4):
        indices = tuple(p[0] for p in permutacion)
        combinacion = ''.join(str(p[1]) for p in permutacion)
        if combinacion in prefijos_venezolanos:
            prefijos_encontrados.append((combinacion, indices))
            

    return prefijos_encontrados


def construir_numeros_telefono(prefijo, digitos, posiciones_usadas):
    # Filtrar los dígitos restantes
    digitos_restantes = [digitos[i] for i in range(len(digitos)) if i not in posiciones_usadas]

    # Lista para almacenar los números de teléfono válidos
    numeros_validos = []

    # Generar todas las combinaciones posibles de 7 dígitos
    for combinacion in permutations(digitos_restantes, 7):
        # Verificar las condiciones adicionales y evitar división por cero
        if (es_primo(combinacion[-1]) and combinacion[-1] != 0 and combinacion[-2] % combinacion[-1] == 0 and
                combinacion[4] != 0 and combinacion[5] != 0 and combinacion[6] != 0 and
                combinacion[4] % combinacion[5] == 0 and combinacion[5] % combinacion[6] == 0 and
                combinacion[4] % combinacion[6] == 0 and verificar_condiciones_adicionales(list(combinacion))):
            numero_telefono = prefijo + ''.join(map(str, combinacion))
            numeros_validos.append(numero_telefono)

    return numeros_validos


if __name__ == "__main__":
    # Lista de ejemplos para probar
    ejemplos = [
        [0, 0, 2, 2, 3, 4, 4, 8, 8, 9, 9]
    ]

    for vector_digitos in ejemplos:
        print(f"Probando vector: {vector_digitos}")
        prefijos_encontrados = construir_prefijos(vector_digitos)

        numeros_telefono_validos = []
        posiciones_usadas = set()  # Iniciar posiciones usadas
        for prefijo, posiciones in prefijos_encontrados:
            # Crear una copia de las posiciones usadas para cada prefijo
            numeros_validos = construir_numeros_telefono(prefijo, vector_digitos, posiciones)
            numeros_telefono_validos.extend(numeros_validos)

        # Eliminar duplicados de numeros_telefono_validos mientras se preserva el orden
        numeros_telefono_validos_sin_duplicados = []
        vistos = set()
        for numero in numeros_telefono_validos:
            if numero not in vistos:
                numeros_telefono_validos_sin_duplicados.append(numero)
                vistos.add(numero)

        if numeros_telefono_validos_sin_duplicados:
            for numero in numeros_telefono_validos_sin_duplicados:
                print(f"Numero de telefono completo: {numero}")
        else:
            print("No se pudo construir un número de teléfono que cumpla con las condiciones.")
