from action_manager import SshClient


def apply_cpu_resource(pod_id, node, cpu):
    client = SshClient("ridl:ridl123@%s" % node)
    result = client.execute(
        "python3 /home/ridl/rajibs_work/mba/action_execution/cpu_scaling.py %s %s " % (pod_id, round(cpu, 2)),
        sudo=True)
    print(result)

# id = "/kubepods.slice/kubepods-pod71efdf1e_edae_4c96_91a1_59cb53a2de4e.slice/docker-d49bdd6cf252a1a431cc12c73c9fb4634493000a9ff6b1ac2d647becc569f892.scope"
# node = "ridlserver10"
# cpu = 200000
# apply_cpu_resource(id, node, cpu)
