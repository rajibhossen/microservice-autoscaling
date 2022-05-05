utilizations = {}


def get_uniform_utilizations(configurations, utilizations_list, target_utilization):
    for item in utilizations_list:
        for key in item.keys():
            if key in utilizations:
                utilizations[key] += item[key]
            else:
                utilizations[key] = item[key]

    for key in utilizations.keys():
        utilizations[key] = utilizations[key] / len(utilizations_list)
    # print(utilizations)

    # print("Target utilizations is: ", target_utilization)
    new_configurations = {}
    for key in configurations.keys():
        current_cpu = configurations[key]
        current_util = utilizations[key]
        new_cpu = (current_cpu * (current_util / 100)) / (target_utilization / 100)
        new_configurations[key] = max(0.3, round(new_cpu, 1))
        new_configurations[key] = min(5, new_configurations[key])

    return new_configurations


configurations = {'hotel-reserv-frontend': 1.6, 'hotel-reserv-geo': 0.3, 'hotel-reserv-profile': 0.5,
                  'hotel-reserv-rate': 0.3, 'hotel-reserv-recommendation': 0.3, 'hotel-reserv-reservation': 0.3,
                  'hotel-reserv-search': 0.5, 'hotel-reserv-user': 0.3}
utilizations_list = [{'hotel-reserv-frontend': 31.642052001168246, 'hotel-reserv-geo': 16.700510231258033, 'hotel-reserv-profile': 23.6032627833172, 'hotel-reserv-rate': 18.494963755583115,
                      'hotel-reserv-recommendation': 15.458233631286038, 'hotel-reserv-reservation': 24.916101915844184, 'hotel-reserv-search': 25.559604925718027, 'hotel-reserv-user': 14.720783491480677},
                     {'hotel-reserv-frontend': 32.1813450829289, 'hotel-reserv-geo': 16.972007977685955, 'hotel-reserv-profile': 22.212115100435646,
                      'hotel-reserv-rate': 18.86856892381525, 'hotel-reserv-recommendation': 15.312409340011444, 'hotel-reserv-reservation': 24.586883888904104,
                      'hotel-reserv-search': 24.34890801229827, 'hotel-reserv-user': 14.649351629256554},
                     {'hotel-reserv-frontend': 31.120752794187627, 'hotel-reserv-geo': 17.30546413988549, 'hotel-reserv-profile': 21.709856393207343,
                      'hotel-reserv-rate': 18.401941656377108, 'hotel-reserv-recommendation': 15.535567324323484, 'hotel-reserv-reservation': 24.292786265405677,
                      'hotel-reserv-search': 24.916015205311663, 'hotel-reserv-user': 14.694945995357012}]
print(get_uniform_utilizations(configurations, utilizations_list, 25))
