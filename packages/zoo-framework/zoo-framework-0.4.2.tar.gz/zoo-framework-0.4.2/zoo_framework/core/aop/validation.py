params_validate_map = {

}


def validation(params_key="") -> object:
    def inner(params):
        if params_validate_map.get(params_key) is None:
            params_validate_map[params_key] = []

        params_validate_map[params_key].insert(params)
        return params

    return inner


def validation_params(params_key, value):
    # 获得有效值
    valid_values = params_validate_map.get(params_key)

    if valid_values is None:
        return False

    if type(valid_values) != list:
        return False

    if value in valid_values:
        return True
