def get_location(location_list):
    result = None
    for location in location_list:
        if 'NT' in location or 'DN' in location or 'HCM' in location or 'PQ' in location:
            location_list.remove(location)
            result = location        
    return result, location_list 

def findObjectContain(list, findObject):
    result = ''
    for x in list:
        if findObject in x.name:
            result = x.name
    return result
    

def parse_to_procedure(logical_tree):   
    logical_expression = logical_tree.label()['SEM']
    
    result = {}
    
    whquery = list(logical_expression.args)[-1]
    whqParas = [pred.name for pred in whquery.constants()]
    if 'YESNO' in whqParas:
        whtype = 'YESNO'
        request_expression = list(logical_expression.args)[0]
        request = list(request_expression.predicates())[0].name
        gap = findObjectContain(request_expression.constants(), 'tour')
        result = {'whtype': whtype, 'request': request, 'gap': gap}
        
    if 'HOWLONG' in whqParas:
        whtype = 'HOWLONG'
        request_expression = list(logical_expression.args)[0]
        location_list = [pred.name for pred in request_expression.constants()]
        location, objects = get_location(location_list)
        result = {'whtype': whtype, 'location': location}
        
    if 'HOWMANY' in whqParas:
        whtype = 'HOWMANY'
        request_expression = list(logical_expression.args)[0]
        location_list = [pred.name for pred in request_expression.constants()]
        location, objects = get_location(location_list)
        result = {'whtype': whtype, 'location': location, 'object': objects[0]}

    if 'WHAT' in whqParas:
        whtype = 'WHAT'
        request_expression = list(logical_expression.args)[0]
        location_list = [pred.name for pred in request_expression.constants()]
        location, objects = get_location(location_list)
        result = {'whtype': whtype, 'location': location, 'object': objects[0]}
    
    return result
    