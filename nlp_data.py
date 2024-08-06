raw_database = [
                    """(DTIME PQ HCMC "7AM 1/7")""",
                    """(ATIME PQ PQ "9AM 1/7")""",
                    """(DTIME PQ HCMC "8AM 5/7")""",
                    """(ATIME PQ PQ "10AM 5/7")""",
                    """(DTIME DN HCMC "7AM 1/7")""",
                    """(ATIME DN DN "9AM 1/7")""",
                    """(DTIME DN HCMC "7AM 4/7")""",
                    """(ATIME DN DN "9AM 4/7")""",
                    """(DTIME NT HCMC "7AM 1/7")""",
                    """(ATIME NT NT "12AM 1/7")""",
                    """(DTIME NT HCMC "7AM 5/7")""",
                    """(ATIME NT NT "12AM 5/7")""",
                    """(RUN-TIME PQ HCM PQ 2:00 HR)""",
                    """(RUN-TIME DN HCM DN 2:00 HR)""",
                    """(RUN-TIME NT HCM NT 5:00 HR)""",
                    """(BY PQ airplane)""",
                    """(BY DN airplane)""",
                    """(BY NT train)"""
]

def categorize_database(database):

    arrival_times = [data.replace('(','').replace(')','') for data in database if 'ATIME' in data]
    departure_times = [data.replace('(','').replace(')','') for data in database if 'DTIME' in data]
    run_times = [data.replace('(','').replace(')','') for data in database if 'RUN-TIME' in data]
    by = [data.replace('(','').replace(')','') for data in database if 'BY' in data]
    result = { 'arrival':arrival_times, 'departure':departure_times, 'runtime': run_times, 'by': by}
    return result

def get_dict_for_tuple(data):
    data = data.split(" ")           
    if data[0] == "ATIME" or data[0] == "DTIME":
        return {'type': data[0], 'tourname': data[1], 'from': data[2], 'to': data[1], 'time': data[3] + ' ' + data[4]}
    if data[0] == "RUN-TIME":
        return {'type': data[0], 'tourname': data[1], 'from': data[2], 'to': data[3], 'time': data[4] + ' ' + data[5]}
    if data[0] == "BY":
        return {'type': data[0], 'tourname': data[1], 'by': data[2]}
            

def retrieve_result(semantics):

    database = categorize_database(raw_database)
    
    result = ""
    question_type = 0
    
    if semantics["whtype"] == 'YESNO':
        if semantics["request"] == 'REMIND':
            if int(semantics["gap"].find("tour")) != -1:
                result = result + f"Có tổng cộng {len(database['departure'])} tour \n"
                for departure in database['departure']:
                    data = get_dict_for_tuple(departure)
                    result = result + f"tour đi từ {data['from']} đến {data['to']} khởi hành lúc {data['time']}\n" 
        question_type = 1
                    
    if semantics["whtype"] == 'HOWLONG':
        for run_time in database['runtime']:
            data = get_dict_for_tuple(run_time)
            if data["to"] == semantics["location"]:
                result = result + f"tour đi từ {data['from']} đến {data['to']} hết {data['time']}" 
        question_type = 2
            
    if semantics["whtype"] == 'HOWMANY':
        if "tour" in semantics["object"]:
            tour_count = 0 
            for arrival in database['arrival']:
                data = get_dict_for_tuple(arrival)
                if data["to"] == semantics["location"]: 
                    tour_count += 1
            result = result + f"có {tour_count} tour đi đến {semantics['location']}" 
            question_type = 3 
        if "date" in semantics["object"]:
            for arrival in database['arrival']:
                data = get_dict_for_tuple(arrival)
                if data["to"] == semantics["location"]:
                    time = data["time"].replace('\"','').split(" ")[1]
                    result = result + f"đi {semantics['location']} có ngày {time}\n"
            question_type = 5
                    
    if semantics["whtype"] == 'WHAT': 
        tour_location = semantics["location"]
        for by in database['by']:
            data = get_dict_for_tuple(by) 
            if data["tourname"] == semantics["location"]:
               result = result + f"đi {tour_location} bằng {data['by']}\n" 
        question_type = 4    

    return result, question_type