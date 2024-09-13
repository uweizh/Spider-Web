# 将 header 和 data 转换成字典列表
def convert_to_dict(header, data):
    result = []
    for row in data:
        row_dict = {}
        for i, value in enumerate(row):
            row_dict[header[i]] = value
        result.append(row_dict)
    return result

