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


configurations = {'carts': 2.4, 'catalogue': 1.6, 'front-end': 2.6, 'orders': 1.4, 'payment': 0.6, 'shipping': 0.6, 'user': 1.5}
utilizations_list = [{'carts': 19.840637765298645, 'catalogue': 11.470322849371884, 'front-end': 52.888398046119974, 'orders': 8.423494707575662, 'payment': 0.2092107722751899, 'shipping': 0.5133823035744213, 'user': 10.180151709091936},
                     {'carts': 19.568719686012603, 'catalogue': 12.098542566983895, 'front-end': 56.02611424971526, 'orders': 9.333024052389941, 'payment': 0.10090490657156415, 'shipping': 0.29750516226637097, 'user': 10.686611969224556},
                     {'carts': 21.077795920487567, 'catalogue': 12.081930947438316, 'front-end': 56.04967541238045, 'orders': 8.796660659882825, 'payment': 0.1206652919895129, 'shipping': 0.3795878208261037, 'user': 10.153437390105095}]
print(get_uniform_utilizations(configurations, utilizations_list, 10))
