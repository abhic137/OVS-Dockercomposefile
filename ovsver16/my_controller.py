from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

class MyController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MyController, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install a flow entry to forward traffic between Ubuntu1 and Ubuntu2
        match = parser.OFPMatch(in_port=<port_number_of_Ubuntu1>, eth_dst=<Ubuntu2_MAC_address>)
        actions = [parser.OFPActionOutput(<port_number_of_Ubuntu2>)]
        self.add_flow(datapath, 10, match, actions)

        match = parser.OFPMatch(in_port=<port_number_of_Ubuntu2>, eth_dst=<Ubuntu1_MAC_address>)
        actions = [parser.OFPActionOutput(<port_number_of_Ubuntu1>)]
        self.add_flow(datapath, 10, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        instructions = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        flow_mod = parser.OFPFlowMod(
            datapath=datapath, cookie=0, cookie_mask=0,
            table_id=0, command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=0,
            priority=priority, buffer_id=ofproto.OFP_NO_BUFFER,
            out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY,
            flags=0, match=match, instructions=instructions
        )
        datapath.send_msg(flow_mod)
