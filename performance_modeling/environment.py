import grpc

import message_pb2
import message_pb2_grpc

NUM_RESOURCES = 5


class Environment:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = message_pb2_grpc.InteractionStub(self.channel)

    def get_state(self, component_id):
        state = self.stub.GetState(component_id)
        if component_id.id != state.id:
            print("Component ID doesn't match!")
            return False, None

        if not state.usage or not state.limit or not state.other:
            print("Incomplete states received!")
            return False, None
        return True, state

    def perform_action(self, message):
        if not message.id or not message.action:
            print("Incomplete action to send!")
            return (False, None)
        response = self.stub.PerformAction(message)
        if response.status != 'OK':
            print("Action failed to execute!")
            return (False, None)
        return (True, response)

    def new_reset(self, id):
        ret, state = self.get_state(id)
        if ret == False:
            return

        self.curr_arrival_rate = state.other.curr_arrival_rate
        self.cpu_limit = 1  # state.limit.cpu
        self.mem_limit = 1  # state.limit.memory
        self.llc_limit = 1  # state.limit.llc
        self.io_limit = 1  # state.limit.io
        self.net_limit = 1  # state.limit.network
        self.curr_cpu_util = state.usage.cpu
        self.curr_mem_util = state.usage.memory
        self.curr_llc_util = state.usage.llc
        self.curr_io_util = state.usage.io
        self.curr_net_util = state.usage.network
        self.slo_retainment = state.other.slo_retainment
        self.rate_ratio = state.other.rate_ratio
        self.percentages = state.other.percentages
        state = {
            'curr_arrival_rate': self.curr_arrival_rate,
            'cpu_limit': self.cpu_limit,
            'mem_limit': self.mem_limit,
            'llc_limit': self.llc_limit,
            'io_limit': self.io_limit,
            'net_limit': self.net_limit,
            'curr_cpu_util': self.curr_cpu_util,
            'curr_mem_util': self.curr_mem_util,
            'curr_llc_util': self.curr_llc_util,
            'curr_io_util': self.curr_io_util,
            'curr_net_util': self.curr_net_util,
            'slo_retainment': self.slo_retainment,
            'rate_ratio': self.rate_ratio,
            'percentages': self.percentages
        }
        return state

    def new_step(self, cpu_action, mem_action, llc_action, io_action, net_action, id):
        action = message_pb2.Action(cpu=cpu_action, memory=mem_action, llc=llc_action, io=io_action, network=net_action)
        msg = message_pb2.ToServerMessage(name='default', node='default', id=id, action=action)
        ret, response = self.perform_action(msg)
        if ret == False:
            return
        self.slo_retainment = response.other_slo_retainment
        self.curr_arrival_rate = response.other.curr_arrival_rate
        self.cpu_limit += cpu_action  # response.limit.cpu
        self.mem_limit += mem_action  # response.limit.memory
        self.llc_limit += llc_action  # response.limit.llc
        self.io_limit += io_action  # response.limit.io
        self.net_limit += net_action  # response.limit.network
        self.curr_cpu_util = response.usage.cpu
        self.curr_mem_util = response.usage.memory
        self.curr_llc_util = response.usage.llc
        self.curr_io_util = response.usage.io
        self.curr_net_util = response.usage.network
        self.rate_ratio = response.other.rate_ratio
        self.percentages = response.other.percentages
        reward = NUM_RESOURCES * self.slo_retainment + self.curr_cpu_util / self.cpu_limit + self.curr_mem_util / self.mem_limit + self.curr_llc_util / self.llc_limit + self.curr_io_util / self.io_limit + self.curr_net_util / self.net_limit
        # if not done:
        #    reward = -(NUM_RESOURCES)*(1-self.slo_retainment) + self.curr_cpu_util/self.cpu_limit + self.curr_mem_util/self.mem_limit + self.curr_llc_util/self.llc_limit + self.curr_io_util/self.io_limit + self.curr_net_util/self.net_limit

        state = {
            'cpu_limit': self.cpu_limit,
            'mem_limit': self.mem_limit,
            'llc_limit': self.llc_limit,
            'io_limit': self.io_limit,
            'net_limit': self.net_limit,
            'curr_cpu_util': self.curr_cpu_util,
            'curr_mem_util': self.curr_mem_util,
            'curr_llc_util': self.curr_llc_util,
            'curr_io_util': self.curr_io_util,
            'curr_net_util': self.curr_net_util,
            'slo_retainment': slo_retainment,
            'curr_arrival_rate': self.curr_arrival_rate,  # workload
            'rate_ratio': self.rate_ratio,  # workload
            'percentages': self.percentages  # workload
        }

        return state, reward, done
