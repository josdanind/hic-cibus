def is_list_of_tuples_with_n_elements(obj: object, n: int) -> bool:
    """
    Verifica si un objeto es una lista de tuplas,
    y cada tupla contiene exactamente `n` elementos.

    Args:
        obj (object): Objeto a verificar.
        n (int): Número exacto de elementos que debe tener cada tupla.

    Returns:
        bool: True si `obj` es una lista de tuplas con `n` elementos cada una, False en caso contrario.

    Ejemplos:
        >>> is_list_of_tuples_with_n_elements([(1, 2), (3, 4)], 2)
        True

        >>> is_list_of_tuples_with_n_elements([(1,), (2, 3)], 2)
        False

        >>> is_list_of_tuples_with_n_elements("no es una lista", 2)
        False
    """
    if not isinstance(obj, list):
        return False

    for item in obj:
        if not isinstance(item, tuple) or len(item) != n:
            return False

    return True
