def parse(str):
    if (str == '[]'):
        return {}

    if (str[0] in ['{', '[']):
        res = dict()
        bracket_num = 0
        res_list = list()
        is_list = (str[0] == '[')
        str = str[1:-1]
        tmp_str = ''

        for tmp_char in str:
            if (tmp_char == ' '):
                continue

            tmp_str += tmp_char

            if (tmp_char[0] in ['{', '[']):
                bracket_num += 1
            elif (tmp_char[0] in ['}', ']']):
                bracket_num -= 1

            if (not bracket_num and tmp_char == ':'):
                key = tmp_str[:-1]
                key = key.replace('\'', '')
                tmp_str = ''
            elif (not bracket_num and tmp_char == ',' and not is_list):
                value = tmp_str[:-1]
                value = value.replace('\'', '')
                res[key] = value
                # key = ''  value = ''
                tmp_str = ''
            elif (not bracket_num and tmp_char == ',' and is_list):
                res_list.append(parse(tmp_str[:-1]))
                # key = ''  value = ''
                tmp_str = ''

        if (tmp_str[0] == '"' or tmp_str[0] == '\''):
            res[key] = tmp_str[1:-1]
        elif is_list:
            res_list.append(parse(tmp_str))
        else:
            res[key] = parse(tmp_str)
    else:
        return str

    if is_list:
        return res_list
    else:
        return res

