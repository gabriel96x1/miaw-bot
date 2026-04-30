def edit_file(path: str, operation: str, content: str = "", line_number: int = None, old_text: str = "") -> str:
    """
    Edita archivos de texto en el sistema de archivos local.
    Úsala cuando el usuario quiera modificar, actualizar, agregar
    o eliminar contenido de un archivo existente. Para crear archivos
    nuevos usa create_file en su lugar.
    
    Operaciones disponibles:
    - 'replace_text': reemplaza un texto específico por otro
    - 'insert_line': inserta contenido en una línea específica
    - 'delete_line': elimina una línea específica
    - 'append': agrega contenido al final del archivo
    - 'overwrite': reemplaza todo el contenido del archivo
    
    REQUIERE CONFIRMACIÓN HUMANA para operaciones destructivas
    como 'overwrite' o 'delete_line'. Nunca ejecutes sin que
    el usuario haya aprobado explícitamente los cambios.
    
    Args:
        path: Ruta absoluta o relativa al archivo
        operation: Tipo de operación ('replace_text', 'insert_line',
                   'delete_line', 'append', 'overwrite')
        content: Contenido nuevo a escribir o insertar
        line_number: Número de línea para 'insert_line' y 'delete_line' (1-indexed)
        old_text: Texto a reemplazar cuando operation es 'replace_text'
    """
    import os

    print(f"\n[Tool] 📝 Editando archivo: {path} | Operación: {operation}...")

    try:
        if not os.path.exists(path):
            return f"Error: El archivo '{path}' no existe."

        # Leer contenido actual
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            raw = ''.join(lines)

        if operation == 'append':
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f"\n{content}")
            return f"Contenido agregado al final de '{path}'."

        elif operation == 'overwrite':
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Archivo '{path}' sobreescrito correctamente."

        elif operation == 'replace_text':
            if not old_text:
                return "Error: Debes proporcionar 'old_text' para la operación replace_text."
            if old_text not in raw:
                return f"Error: El texto '{old_text}' no se encontró en el archivo."
            nuevo = raw.replace(old_text, content, 1)  # solo primera ocurrencia
            with open(path, 'w', encoding='utf-8') as f:
                f.write(nuevo)
            return f"Texto reemplazado exitosamente en '{path}'."

        elif operation == 'insert_line':
            if line_number is None:
                return "Error: Debes proporcionar 'line_number' para insert_line."
            idx = line_number - 1
            lines.insert(idx, content + '\n')
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return f"Línea insertada en la posición {line_number} de '{path}'."

        elif operation == 'delete_line':
            if line_number is None:
                return "Error: Debes proporcionar 'line_number' para delete_line."
            if line_number > len(lines):
                return f"Error: El archivo solo tiene {len(lines)} líneas."
            eliminada = lines.pop(line_number - 1).strip()
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return f"Línea {line_number} eliminada: '{eliminada}'."

        else:
            return f"Error: Operación '{operation}' no reconocida."

    except UnicodeDecodeError:
        return f"Error: '{path}' no es un archivo de texto legible."
    except PermissionError:
        return f"Error: Sin permisos para editar '{path}'."
    except Exception as e:
        return f"Error al editar el archivo: {str(e)}"