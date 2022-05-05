import client


def apply_configurations(configs, settings):
    for x in configs:
        cpu = configs[x] / len(settings[x])
        print("Apply new configs.... ")
        for info in settings[x]:
            print(x, info["node"], cpu, info["id"])
            client.apply_actions(info["id"], info["node"], int(cpu * 100000))


configs = {'carts': 3.0, 'catalogue': 3.0, 'front-end': 3.0, 'orders': 3.0, 'payment': 3.0, 'shipping': 3.0,
           'user': 3.0}
settings = {'carts': [{
                          'id': '/kubepods.slice/kubepods-pod9a90f25f_66cf_40cc_b26f_f4065d700e2c.slice/docker-7ccfe3cb41a5c52ad269ce4314e8e0914f18186d376828f8a586700a07a612ba.scope',
                          'node': 'ridlserver10'}],
            'catalogue': [{
                              'id': '/kubepods.slice/kubepods-pod37618f38_db10_4827_8c2f_4b8b509aa6a2.slice/docker-ca6c5b4564541a349fff65aaba9ca36f80171c3efd6beab295161e6ecbfdfc18.scope',
                              'node': 'ridlserver07'}],
            'front-end': [{
                              'id': '/kubepods.slice/kubepods-pod27078a9f_3b72_4738_bb74_ad69cbdabc74.slice/docker-655a7a20f60fbacc127d8598e36faad569e6fcbfbc81ddaa272a7c80dfca2bef.scope',
                              'node': 'ridlserver08'}],
            'orders': [{
                           'id': '/kubepods.slice/kubepods-pod76b58468_32b2_4b94_9d04_01e2a8b63306.slice/docker-5664f6a701eb0feb192088316798d7a619a0ec90e72e23dfac7f2f8c4b40bece.scope',
                           'node': 'ridlserver06'}],
            'payment': [{
                            'id': '/kubepods.slice/kubepods-pod36c078af_9bf8_4105_8441_2e2597aa6640.slice/docker-7ca12ac91540380fbac2e38568a1bc1f51f93d34278ddcdfba2372fc938aab49.scope',
                            'node': 'ridlserver08'}],
            'shipping': [{
                             'id': '/kubepods.slice/kubepods-pod98125ef5_d68f_41be_afe8_2277e8445d52.slice/docker-24030cf744725cd7f14181c713298f864cd30c4f65bc96d58610c51a687eeddc.scope',
                             'node': 'ridlserver10'}],
            'user': [{
                         'id': '/kubepods.slice/kubepods-podac1005ba_cfdf_4ebc_83fa_9d3d2bf677b5.slice/docker-5735061f787b8ff238ae459db556051d6fe508f517cbeee682f6af14d5128fdf.scope',
                         'node': 'ridlserver07'}]}

apply_configurations(configs, settings)
