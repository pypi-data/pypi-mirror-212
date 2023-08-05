import json


def dump(obj, fp, output_type='text', separator='_', entropy=False):
    if output_type == 'text':
        if entropy:
            obj = separator.join(map(str, obj))
        else:
            obj = separator.join(obj)
    elif output_type == 'json':
        if entropy:
            obj = {'entropy': obj[0], 'n': obj[1]}
        else:
            obj = tuple(obj)
        obj = json.dumps(obj)
    else:
        raise ValueError(output_type)
    fp.write(obj + '\n')
