# -*- coding:utf-8 -*-

import logging
from flask_wtf import Form
from wtforms.fields import IntegerField, StringField
from wtforms.validators import DataRequired, Optional, InputRequired


from xenadmin.common.utils import  guish_rpc_client
from xenadmin.common.usualfunc import is_ipv6_address, is_ipv4_address, is_ipv4_network, get_ipaddr_version


class InterfaceForm(Form):
    if_type = IntegerField('if_type', validators=[InputRequired(u"缺少输入接口类型")])
    ifname = StringField('ifname', validators=[DataRequired(u"缺少接口名称")])
    admin = IntegerField('admin', validators=[
        InputRequired(u'缺少开关参数')], default=-1)
    autoneg = IntegerField('autoneg', validators=[InputRequired(u"缺少协商类型参数")])
    speed = StringField('speed', validators=[Optional()], default="")
    ipaddr = StringField('ipaddr', validators=[Optional()], default="")
    mask = StringField('mask', validators=[Optional()], default="")
    gw = StringField('gw', validators=[Optional()], default="")
    ipv6addr = StringField('ipv6addr', validators=[Optional()], default="")
    https_allow = IntegerField('https_allow', validators=[
        InputRequired(u'HTTPS选项参数错误')], default=-1)
    http_allow = IntegerField('http_allow', validators=[
        InputRequired(u'HTTP选项参数错误')], default=-1)
    ssh_allow = IntegerField('ssh_allow', validators=[
        InputRequired(u'SSH选项参数错误')], default=-1)

    def is_ipv6addr(self):
        try:
            ipv6_addr, ipv6_mask = self.ipv6addr.data.split("/")
            ipv6_mask = int(ipv6_mask)
        except Exception as e:
            logging.warning("ipv6addr is not valid: %s" % e)
            self.ipv6addr.errors.append(u"IPv6的地址格式不合法")
            return False
        if not is_ipv6_address(ipv6_addr) or ipv6_mask < 0 or ipv6_mask > 128:
            self.ipv6addr.errors.append(u"IPv6的地址格式不合法")
            return False
        return True

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        if self.if_type.data != 0:
            self.if_type.errors.append(u"只能配置管理口")
            return False
        # admin status
        if self.admin.data not in NetWorkManager.admin_state_dic:
            self.admin.errors.append(u"admin参数错误")
            return False
        # autoeng
        if self.autoneg.data not in NetWorkManager.autoneg_dic:
            self.autoneg.errors.append(u"autoneg参数错误")
            return False

        # ipv4
        if self.ipaddr.data:
            if not is_ipv4_address(self.ipaddr.data):
                self.ipaddr.errors.append(u'IPV4地址错误')
                return False
        # mask
        if self.mask.data:
            if not is_ipv4_address(self.mask.data):
                self.mask.errors.append(u"IPV4子网掩码格式错误")
                return False
        if (self.mask.data and not self.ipaddr.data) or (not self.mask.data and self.ipaddr.data):
            return False

        # ipv6
        if self.ipv6addr.data:
            rv = self.is_ipv6addr()
            if not rv:
                return False

        # The version doesn't support autoneg
        # if self.autoneg.data == 0:
        #     if self.speed.data == "":
        #         self.speed.errors.append(u'非自协商时速率参数不能为空')
        #         return False
        # 沙箱没有管理口和监听口的区分
        # if not IPAddress(self.mask.data).is_netmask():
        #     self.mask.errors.append(u"掩码格式错误")
        #     return False
        # if self.ipv6addr.data:
        #     rv = self.is_ipv6addr()
        #     if not rv:
        #         return False

        if self.http_allow.data not in NetWorkManager.proto_allow_dic:
            self.http_allow.errors.append(u"HTTP的配置不合法")
            return False
        if self.https_allow.data not in NetWorkManager.proto_allow_dic:
            self.https_allow.errors.append(u"HTTPS的配置不合法")
            return False
        if self.ssh_allow.data not in NetWorkManager.proto_allow_dic:
            self.ssh_allow.errors.append(u"SSH的配置不合法")
            return False
        return True


class NetWorkManager(object):
    iftype_dic = {0: u"管理口", 1: u"监听口"}  # sandbox only using iftype
    admin_state_dic = {0: "down", 1: "up"}
    autoneg_dic = {0: u"非自协商", 1: u"自协商"}
    speed_dic = {0: "unknown", 1: "10M", 2: "100M", 3: "1000M", 4: "10000M"}
    duplex_dic = {0: "unknown", 1: u"半双工", 2: u"全双工"}
    proto_allow_dic = {0: u"禁止", 1: u"允许"}

    convert_map = {
        'Duplex': {'Full': 2, 'Half': 1, 'Unknown! (255)': 0},
        'Speed': {'Unknown!': 0, '10Mb/s': 1, '100Mb/s': 2, '1000Mb/s': 3, '10000Mb/s': 4},
        'Link detected': {'yes': 1, 'no': 0},
        'Supports auto-negotiation': {'Yes': 1, 'No': 0},
        'Auto-negotiation': {'on': 1, 'off': 0}
    }

    router_add = "add"
    router_del = "del"

    @classmethod
    def _convert_orderdict_to_dict(cls, order_dic):
        dic = dict()
        for k, v in order_dic.iteritems():
            if isinstance(v, list):
                lis = list()
                for i in v:
                    lis.append(i)
                v = lis
            dic[k] = v
        return dic

    @classmethod
    def get_dns_server(cls):
        is_success, response = guish_rpc_client.get_dns_addr()
        # logging.warn(type(response))
        if not is_success:
            return False, response
        if "prior" not in response:
            response["prior"] = ""
        if "secondary" not in response:
            response["secondary"] = ""
        return True, cls._convert_orderdict_to_dict(response)

    @classmethod
    def set_dns_server(cls, main_server, secondary_server=None):
        param = {'prior': str(main_server), 'secondary': secondary_server}
        is_success, response = guish_rpc_client.set_dns_addr(param)
        if not is_success:
            return False, response
        return True, "ok"

    @classmethod
    def _format_interface_info_list(cls, data_list):
        result = list()
        for eth in data_list:
            ifname = eth.keys()[0]
            if ifname.startswith('vi'):
                continue
            dic = eth.get(ifname, {})
            dic["if_type"] = 0  # 由于沙箱没有区分管理口和监听口，所以强制设置为0(管理口)
            if "Link detected" not in dic:
                continue
            if "ifname" in dic and not dic["ifname"].startswith("eth"):
                continue

            dic["link"] = cls.convert_map['Link detected'][dic.pop('Link detected')]
            dic["admin"] = int(dic["admin"])
            dic["autoneg"] = cls.convert_map['Auto-negotiation'][dic.pop('Auto-negotiation')]
            dic["speed"] = cls.convert_map['Speed'][dic.pop('Speed')]
            dic["duplex"] = cls.convert_map['Duplex'][dic.pop('Duplex')]

            if dic["if_type"] not in cls.iftype_dic:
                return False, "the value of if_type is illegal"
            if dic.get("ifname", "").strip() == "":
                return False, "the value of ifname is illegal"
            if not dic["Supports auto-negotiation"].strip():
                return False, "the value of support-autoneg is illegal"
            if dic["admin"] not in cls.admin_state_dic:
                return False, "the value of admin is illegal"
            if dic["autoneg"] not in cls.autoneg_dic:
                return False, "the value of autoneg is illegal"
            if dic["speed"] not in cls.speed_dic:
                return False, "the value of speed is illegal"
            if dic["duplex"] not in cls.duplex_dic:
                return False, "the value of duplex is illegal"

            dic["support-autoneg"] = cls.convert_map['Supports auto-negotiation'][dic.pop('Supports auto-negotiation')]

            tmp_list = str(dic.pop("Supported link modes")).split(' ')
            dic["supported-speed"] = tmp_list
            # dic["cur_speed_duplex"] = dic["cur_speed_duplex"].strip()
            dic["supported-state"] = cls.admin_state_dic.keys()
            dic["speed"] = cls.speed_dic[dic["speed"]]
            dic["duplex"] = cls.duplex_dic[dic["duplex"]]

            if dic["if_type"] == 0:
                # ip
                if "ipaddr" not in dic or dic["ipaddr"].strip() == "":
                    # num = dic["ifname"].split('eth')[1]
                    # if num.isdigit():
                    #     dic["ipaddr"] = "192.168." + num + ".100"
                    # ip_type = 6
                    dic['ipaddr'] = ""
                if "mask" not in dic or dic["mask"].strip() == "":
                    dic["mask"] = ""
                if "gw" not in dic:
                    dic["gw"] = ""
                if "ipv6addr" not in dic:
                    dic["ipv6addr"] = ""
                if "gw_ipv6" not in dic:
                    dic["gw_ipv6"] = ""
                # service
                dic["https_allow"] = int(dic["https_allow"])
                if dic["https_allow"] not in cls.proto_allow_dic:
                    return False, "the value of https_allow is illegal"
                dic["http_allow"] = int(dic["http_allow"])
                if dic["http_allow"] not in cls.proto_allow_dic:
                    return False, "the value of http_allow is illegal"
                dic["ssh_allow"] = int(dic["ssh_allow"])
                if dic["ssh_allow"] not in cls.proto_allow_dic:
                    return False, "the value of ssh_allow is illegal"
            # dic['ip_type'] = ip_type
            result.append(cls._convert_orderdict_to_dict(dic))
        return True, result

    @classmethod
    def get_manager_interface(cls):
        is_success, response = guish_rpc_client.get_manager_interface()
        # logging.warn(response)
        if not is_success:
            return False, response
        return cls._format_interface_info_list(response)

    @classmethod
    def config_manager_interface(cls, if_type, ifname, admin, autoneg, speed, ipaddr,
                                 mask, gw, ipv6addr, https_allow, http_allow, ssh_allow):
        proto_allow_dic = {0: u"禁止", 1: u"允许"}
        if https_allow not in proto_allow_dic:
            return False, u"HTTPS的配置不合法"
        if http_allow not in proto_allow_dic:
            return False, u"HTTP的配置不合法"
        if ssh_allow not in proto_allow_dic:
            return False, u"SSH的配置不合法"
        if https_allow == 0 and http_allow == 0 and ssh_allow == 0:
            return False, u"至少开启一个服务"
        if_type = 0  # 由于沙箱没有区分管理口和监听口，所以强制设置为0(管理口)
        msg_dic = dict(if_type=str(if_type), ifname=ifname, admin=admin, autoneg=str(autoneg), speed=speed,
                                  ipaddr=ipaddr, mask=mask, gw=gw, ipv6addr=ipv6addr, gw_ipv6="",
                                  https_allow=str(https_allow), http_allow=str(http_allow), ssh_allow=str(ssh_allow))
        is_success, response = guish_rpc_client.set_manager_interface(msg_dic)
        if not is_success:
            return False, response
        return True, "ok"

    @classmethod
    def get_router(cls):
        is_success, response = guish_rpc_client.get_router()
        if not is_success:
            return False, response
        ret_list = []
        for r in response:
            r_dic = r.values()[0]
            if r_dic:
                ret_list.append({'destination': r_dic.get('daddr', '') or r_dic.get('daddrv6', ''),
                                 'gateway': r_dic.get('nexthop', '') or r_dic.get('nexthopv6', ''),
                                 'iface': r_dic.get('ifname', ''),
                                 'status': str(r_dic.get('status', ''))})
        return True, ret_list

    @classmethod
    def set_router(cls, op, destination, gateway, iface, iptype, routertype):
        # not_used(iface)
        routertype = str(routertype)
        if op == cls.router_add:
            cmd_code = '0'
            if 6 == iptype:
                tmp_dic = {'cmd': cmd_code, 'type': routertype,
                           'daddrv6': destination, 'nexthopv6': gateway}
            else:
                if routertype == '0':
                    destination = '0.0.0.0/0'
                    tmp_dic = {'cmd': cmd_code, 'type': routertype,
                               'daddr': destination, 'nexthop': gateway}
                else:
                    tmp_dic = {'cmd': cmd_code, 'type': routertype,
                               'daddr': destination, 'nexthop': gateway}
        else:
            cmd_code = '1'
            version = get_ipaddr_version(gateway)
            if version == 6:
                tmp_dic = {'cmd': cmd_code,
                           'daddrv6': destination, 'nexthopv6': gateway}
            else:
                tmp_dic = {'cmd': cmd_code,
                           'daddr': destination, 'nexthop': gateway}
        is_success, response = guish_rpc_client.set_router(tmp_dic)
        if not is_success:
            return False, response
        return True, "ok"


if __name__ == "__main__":
    print(1111)
