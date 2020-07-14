# -*- coding:utf-8 -*-
import os
import logging
import time
import simplejson
import socket
import struct
import shutil
import sys
import re

from collections import OrderedDict

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

BASE_DIR = '/data1/json/analyses'
TMP_DIR = '/data1/tmp'
# BASE_DIR = '/data/sample_test'
OUTPUT_DIR = '/data/output/'

FILE_TYPE = {
    None: ' ',
    'generic': ' ',
    'exe': '1',
    'dll': '2',
    'sys': '4',
    'shellcode': '8',
    'js': '16',
    'vbs': '32',
    'doc': '64',
    'docx': '64',
    'xls': '128',
    'xlsx': '128',
    'ppt': '256',
    'pptx': '256',
    'pdf': '512',
    'photo': '1024',
    'swf': '2048',
    'ole': '4096',
    'ole2': '4096',
    'zip': '8192',
    'rar': '8192',
    '7z': '8192',
    'gz': '8192',
    'tar': '8192'
}

NETWORK_TYPE = {
    'tcp': 0x01,
    'udp': 0x02,
    'icmp': 0x04,
    'http': 0x08,
    'ftp': 0x10,
    'tftp': 0x20,
    'smtp': 0x40,
    'tls': 0x80,
    'ssh': 0x100,
    'telnet': 0x200,
    'ldap': 0x400,
    'netbios_name': 0x800,
    'netbios_dgram': 0x1000,
    'netbios_session': 0x2000,
    'imap': 0x4000,
    'msn': 0x8000,
    'jabber': 0x10000,
    'smb': 0x20000,
    'smb2': 0x40000,
    'dcerpc': 0x80000,
    'irc': 0x100000,
    'dns': 0x200000,
    'bgp': 0x400000,
    'modbus': 0x800000,
    'myhttp': 0x1000000,
    'template': 0x2000000,
    'pop': 0x4000000,
    'snmp': 0x8000000,
    'arp': 0x10000000,
    'rarp': 0x20000000
}

CALLER = {
    'nonpe_release_pe': 0x10000,
    'nonpe_run_pe': 0x20000,
    'suspicious_powershell': 0x40000
}

ANTI = {
    'antivm_': 0x10000000,
    'antisandbox_': 0x20000000
}

EXPLOIT = {
    'exploit_dep': 0x01,
    'exploit_eaf': 0x02,
    'exploit_heapspary': 0x04,
    'exploit_hotfix': 0x08,
    'exploit_rop': 0x20,
    'exploit_sehop': 0x40
}


class TransReport():

    def __init__(self, sample_path):
        # super(TransReport, self).__init__()
        self.split = '||'
        self.end = '||\n'
        self.sample_path = sample_path
        self.base_data_name = 'WA_MALCODE_BASE_DATA_DT@'
        self.black_data_name = 'WA_MALCODE_BLACK_DATA_DT@'
        self.dynamic_base_name = 'WA_MALCODE_DYNAMIC_BASE_DT@'
        self.dynamic_process_name = 'WA_MALCODE_DYNAMIC_PROCESS_DT@'
        self.dynamic_regset_name = 'WA_MALCODE_DYNAMIC_REGSET_DT@'
        self.dynamic_domains_name = 'WA_MALCODE_DYNAMIC_DOMAINS_DT@'
        self.dynamic_http_name = 'WA_MALCODE_DYNAMIC_HTTP_DT@'
        self.dynamic_tcp_name = 'WA_MALCODE_DYNAMIC_TCP_DT@'
        self.dynamic_udp_name = 'WA_MALCODE_DYNAMIC_UDP_DT@'
        self.dynamic_dns_name = 'WA_MALCODE_DYNAMIC_DNS_DT@'
        self.dynamic_data_name = 'WA_MALCODE_DYNAMIC_DATA_DT@'
        self.dynamic_create_name = 'WA_MALCODE_DYNAMIC_CREATE_DT@'

        self.dynamic_inject_name = 'WA_MALCODE_DYNAMIC_INJECT_DT@'
        self.dynamic_killproc_name = 'WA_MALCODE_DYNAMIC_KILLPROC_DT@'
        self.dynamic_suspendthr_name = 'WA_MALCODE_DYNAMIC_SUSPENDTHR_DT@'
        self.dynamic_privilege_name = 'WA_MALCODE_DYNAMIC_PRIVILEGE_DT@'
        self.dynamic_vmmk_name = 'WA_MALCODE_DYNAMIC_VMMK_DT@'
        self.dynamic_window_name = 'WA_MALCODE_DYNAMIC_WINDOW_DT@'

        self.dynamic_suspendproc_name = 'WA_MALCODE_DYNAMIC_SUSPENDPROC_DT@'
        self.dynamic_cc_name = 'WA_MALCODE_DYNAMIC_CC_DT@'
        self.dynamic_hidemodule_name = 'WA_MALCODE_DYNAMIC_HIDEMODULE_DT@'
        self.dynamic_filecopy_name = 'WA_MALCODE_DYNAMIC_FILECOPY_DT@'
        self.dynamic_filerename_name = 'WA_MALCODE_DYNAMIC_FILERENAME_DT@'
        self.dynamic_filemove_name = 'WA_MALCODE_DYNAMIC_FILEMOVE_DT@'
        self.dynamic_filedelete_name = 'WA_MALCODE_DYNAMIC_DELETE_DT@'
        self.dynamic_filerewrite_name = "WA_MALCODE_DYNAMIC_FILEREWRITE_DT@"
        self.dynamic_fileaccess_name = 'WA_MALCODE_DYNAMIC_FILEACCESS_DT@'
        self.dynamic_smtp_name = 'WA_MALCODE_DYNAMIC_SMTP_DT@'
        self.md5 = ''
        self.crc32 = ''

    def _write_to_file(self, output, base_name):
        file_name = OUTPUT_DIR + base_name + self.md5 + self.crc32
        with open(file_name, 'w+') as fd:
            fd.write(output)

        import stat  # add1
        os.chmod(file_name, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)  # add2
        os.rename(file_name, file_name + '_ok')

    def choose_package(self, file_type):
        if not file_type:
            return None

        if "DLL" in file_type:
            return "dll"
        elif "PE32" in file_type or "MS-DOS executable" in file_type:  # skyeye
            return "exe"
        elif "PDF" in file_type:
            return "pdf"

        # skyeye
        elif "Microsoft Word 2007+" in file_type:
            return "docx"
        elif "Rich Text Format" in file_type or \
                "Microsoft Word" in file_type or \
                "Microsoft Macintosh Word" in file_type or \
                "Microsoft Office Word" in file_type:
            return "doc"

        # skyeye
        elif "Microsoft Excel 2007+" in file_type:
            return "xlsx"
        elif "Microsoft Office Excel" in file_type or \
                "Microsoft Excel" in file_type:
            return "xls"
        # skyeye
        elif "Microsoft PowerPoint 2007+" in file_type:
            return "pptx"
        elif "Microsoft PowerPoint" in file_type or \
                "Microsoft Office PowerPoint" in file_type:  # skyeye
            return "ppt"
        elif "Zip" in file_type:
            return "zip"
        elif "gzip compressed" in file_type:  # skyeye
            return "gz"
        elif "tar archive" in file_type:
            return "tar"
        elif "7-zip" in file_type:  # skyeye
            return "7z"
        elif "Python script" in file_type:
            return "python"
        elif "RAR" in file_type:  # skyeye
            return "rar"
        elif file_type == "js":  # skyeye
            return "js"
        elif "Macromedia Flash" in file_type:
            return "swf"  # skyeye use ie open swf TODO review
            # return "wsf"
        elif "HTML" in file_type:
            return "ie"
        else:
            return "generic"

    def parse_base_data(self, report):
        try:
            output = ''
            output += self.md5 + self.crc32  # C_SIGN
            output += self.split + '3'  # C_SIGN_TYPE
            output += self.split + ' '  # C_ATTRIBUTE
            file_type = self.choose_package(report.get('target', {}).get('file', {}).get('type', ''))
            output += self.split + FILE_TYPE.get(file_type, ' ')  # C_FILE_TYPE
            output += self.split + ' '  # C_ATTR_TYPE
            output += self.split + ' '  # C_DEV_TYPE
            output += self.split + '%(score).2f' % {'score': report.get('info', {}).get('score', 0.0)}  # C_THREAT_VALUE
            output += self.split + ' '  # C_ZIP_TYPE
            output += self.split + ' '  # C_SIGNATURE_LEVEL
            output += self.end
            self._write_to_file(output, self.base_data_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def _get_cve_info(self, signatures):
        for item in signatures:
            if 'CVE-' in item.get('name', ''):
                return item.get('name', '')
        return ''

    def parse_black_data(self, report):
        try:
            cve = self._get_cve_info(report.get('signatures', []))
            if not cve:
                return
            output = ''
            output += self.md5 + self.crc32  # C_SIGN
            output += self.split + '3'  # C_SIGN_TYPE
            output += self.split + ' '  # C_TYPE
            output += self.split + ' '  # C_MALNAME
            output += self.split + cve  # C_CVE
            output += self.split + ' '  # C_FLAG
            output += self.split + '1'  # C_LEVEL
            output += self.end
            self._write_to_file(output, self.black_data_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def parse_dynamic_base(self, report):
        try:
            output = ''
            output += report.get('target', {}).get('file', {}).get('name', ' ')  # C_OBJ_NAME
            output += self.split + str(report.get('target', {}).get('file', {}).get('size', ' '))  # C_OBJ_SIZE
            file_type = self.choose_package(report.get('target', {}).get('file', {}).get('type', ''))
            output += self.split + FILE_TYPE.get(file_type, ' ')  # C_OBJ_TYPE
            output += self.split + self.md5 + self.crc32  # C_OBJ_ID
            output += self.split + ' '  # C_OBJ_CREATER
            output += self.split + ' '  # C_OBJ_SIGNATURED
            output += self.split + ' '  # C_IS_TRUST
            output += self.split + report.get('static', {}).get('organization', ' ')  # C_ISSUER
            output += self.split + ' '  # C_NOT_AFTER
            output += self.split + ' '  # C_NOT_BEFORE
            output += self.split + ' '  # C_SUBJECT
            output += self.split + ' '  # C_TIMESTAMP
            output += self.end
            self._write_to_file(output, self.dynamic_base_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def _dynamic_process_perline(self, started, pid):
        output = ''
        output += self.md5 + self.crc32  # C_OBJ_ID
        output += self.split + started  # C_OBJ_RUNTIME
        output += self.split + ' '  # C_OBJ_RUNMETHOD
        output += self.split + pid  # C_OBJ_PID
        output += self.split + ' '  # C_OBJ_PPID
        output += self.split + ' '  # C_OBJ_RUN_CREATER
        output += self.end
        return output

    def parse_dynamic_process(self, report):
        try:
            started = int(report.get('info', {}).get('started', 0))
            started = str(started) if started else ' '
            processtree = report.get('behavior', {}).get('processtree', [])

            if not processtree:
                return

            output = ''
            for item in processtree:
                pid = item.get('pid', 0)
                pid = str(pid) if pid else ' '
                output += self._dynamic_process_perline(started, pid)

            self._write_to_file(output, self.dynamic_process_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def _dynamic_regeset_perline(self, op_type, keyname):
        output = ''
        output += self.md5 + self.crc32  # C_OBJ_ID
        output += self.split + op_type  # C_OP_TYPE
        output += self.split + ' '  # C_TIME
        output += self.split + ' '  # C_ISAUTORUN
        output += self.split + ' '  # C_RUNTYPE
        output += self.split + keyname  # C_KEYNAME
        output += self.split + ' '  # C_VALUENAME
        output += self.split + ' '  # C_VALUETYPE
        output += self.split + ' '  # C_KEYVALUE
        output += self.split + ' '  # C_OLDKEYVALUE
        output += self.end
        return output

    def parse_dynamic_regeset(self, report):  # T_DYNAMIC_OBJ_REGSET
        try:
            generic = report.get('behavior', {}).get('generic', [])
            if len(generic) == 0:
                return

            output = ''
            for item in generic:
                regkey_opened = item.get('summary', {}).get('regkey_opened', [])
                regkey_written = item.get('summary', {}).get('regkey_written', [])
                regkey_deleted = item.get('summary', {}).get('regkey_deleted', [])
                i_total = len(regkey_opened) + len(regkey_written) + len(regkey_deleted)

                if i_total == 0:
                    continue

                for i_opened in regkey_opened:
                    output += self._dynamic_regeset_perline('1', i_opened)

                for i_written in regkey_written:
                    output += self._dynamic_regeset_perline('2', i_written)

                for i_deleted in regkey_deleted:
                    output += self._dynamic_regeset_perline('4', i_deleted)

                self._write_to_file(output, self.dynamic_regset_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def _dynamic_domains_perline(self, ip, domain):
        output = ''
        output += self.md5 + self.crc32  # C_OBJ_ID
        output += self.split + ip  # C_IPV4
        output += self.split + ' '  # C_IPV6
        output += self.split + domain  # C_DOMAIN
        output += self.end
        return output

    def parse_dynamic_domains(self, report):
        try:
            domains = report.get('network', {}).get('domains', [])
            if len(domains) == 0:
                return

            output = ''
            for i_dom in domains:
                ip_str = str(i_dom.get('ip', ''))
                ip = ''
                if ip_str:
                    ip_str = ip_str.split(',')[0]
                    ip = str(socket.ntohl(struct.unpack("I", socket.inet_aton(ip_str))[0]))
                domain = i_dom.get('domain', ' ')
                if not ip and not domain:
                    continue
                if not domain:
                    domain = ' '
                if not ip:
                    ip = ' '
                output += self._dynamic_domains_perline(ip, domain)
            self._write_to_file(output, self.dynamic_domains_name)
        except Exception as err:
            logging.error('{0}'.format(err))

    def _dynamic_http_perline(self, http):
        output = ''
        output += self.md5 + self.crc32  # C_OBJ_ID
        output += self.split + http.get('uri', ' ')  # C_URL
        body = http.get('body', ' ')
        output += self.split + body if body else self.split + ' '  # C_BODY
        output += self.split + http.get('user-agent', ' ')  # C_USER-AGENT
        port = http.get('port', 0)
        output += self.split + str(port) if port else self.split + ' '  # C_PORT
        output += self.split + http.get('host', ' ')  # C_HOST
        output += self.split + http.get('version', ' ')  # C_VERSION
        output += self.split + ' '  # C_DST_IPV4
        output += self.split + ' '  # C_DST_IPV6
        output += self.split + http.get('path', ' ')  # C_PATH
        output += self.split + http.get('data', ' ')  # C_DATA
        output += self.split + http.get('method', ' ')  # C_METHOD
        output += self.end
        return output

    def parse_dynamic_http(self, report):
        try:
            http = report.get('network', {}).get('http', [])
            if not http:
                return

            output = ''
            for item in http:
                output += self._dynamic_http_perline(item)

            self._write_to_file(output, self.dynamic_http_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def _dynamic_tcp_perline(self, tcp):
        output = ''
        output += self.md5 + self.crc32  # C_OBJ_ID
        src = socket.ntohl(struct.unpack("I", socket.inet_aton(str(tcp.get('src', ''))))[0])
        output += self.split + str(src)  # C_SRC_IPV4
        output += self.split + ' '  # C_SRC_IPV6
        if str(tcp.get('dst', '')).startswith('192.168'):
            return ''
        dst = socket.ntohl(struct.unpack("I", socket.inet_aton(str(tcp.get('dst', ''))))[0])
        output += self.split + str(dst)  # C_DST_IPV4
        output += self.split + ' '  # C_DST_IPV6
        sport = tcp.get('sport', 0)
        output += self.split + str(sport) if sport else ' '  # C_SPORT
        dport = tcp.get('dport', 0)
        output += self.split + str(dport) if dport else ' '  # C_DPORT
        output += self.end
        return output

    def parse_dynamic_tcp(self, report):
        try:
            tcp = report.get('network', {}).get('tcp', [])
            if not tcp:
                return

            output = ''
            for item in tcp:
                output += self._dynamic_tcp_perline(item)

            self._write_to_file(output, self.dynamic_tcp_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def _dynamic_udp_perline(self, udp):
        output = self.md5 + self.crc32  # C_OBJ_ID
        src = socket.ntohl(struct.unpack("I", socket.inet_aton(str(udp.get('src', ''))))[0])
        output += self.split + str(src)  # C_SRC_IPV4
        output += self.split + ' '  # C_SRC_IPV6
        if str(udp.get('dst', '')).startswith('192.168'):
            return ''
        dst = socket.ntohl(struct.unpack("I", socket.inet_aton(str(udp.get('dst', ''))))[0])
        output += self.split + str(dst)  # C_DST_IPV4
        output += self.split + ' '  # C_DST_IPV6
        sport = udp.get('sport', 0)
        output += self.split + str(sport) if sport else ' '  # C_SPORT
        dport = udp.get('dport', 0)
        output += self.split + str(dport) if dport else ' '  # C_DPORT
        output += self.end
        return output

    def parse_dynamic_udp(self, report):
        try:
            udp = report.get('network', {}).get('udp', [])
            if not udp:
                return

            output = ''
            for item in udp:
                output += self._dynamic_udp_perline(item)

            self._write_to_file(output, self.dynamic_udp_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def _dynamic_dns_perline(self, dns):
        output = ''
        request = dns.get('request', ' ')  # C_REQUEST
        answers = dns.get('answers', [])
        if not answers:
            if request != ' ':
                output += self.md5 + self.crc32  # C_OBJ_ID
                output += self.split + request  # C_REQUEST
                output += self.split + ' '  # C_ANSWERS
                output += self.split + ' '  # C_COUNTS
                output += self.split + ' '  # C_TYPE
                output += self.end
            return output

        for item in answers:
            output += self.md5 + self.crc32  # C_OBJ_ID
            output += self.split + request  # C_REQUEST
            output += self.split + item.get('data', ' ')  # C_ANSWERS
            output += self.split + ' '  # C_COUNTS
            ans_type = item.get('type')  # C_TYPE
            if ans_type == 'A':
                output += self.split + '1'
            elif ans_type == 'CNAME':
                output += self.split + '5'
            else:
                output += self.split + ' '
            output += self.end

        return output

    def parse_dynamic_dns(self, report):
        try:
            dns = report.get('network', {}).get('dns', [])
            if not dns:
                return

            output = ''
            for item in dns:
                output += self._dynamic_dns_perline(item)

            self._write_to_file(output, self.dynamic_dns_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def _get_network_summary(self, network):
        network_type = 0

        for k, v in NETWORK_TYPE.items():
            if network.get(k):
                network_type |= v

        if network_type != 0:
            return str(network_type)

        return ' '

    def _get_dynamic_caller(self, signatures):
        caller = 0
        for item in signatures:
            for k, v in CALLER.items():
                if k in item.get('name', ''):
                    caller |= v

        if caller != 0:
            return str(caller)

        return ' '

    def _get_dynamic_anti(self, signatures):
        anti = 0
        for item in signatures:
            for k, v in ANTI.items():
                if k in item.get('name', ''):
                    anti |= v

        if anti != 0:
            return str(anti)

        return ' '

    def _get_exploit(self, signatures):
        exploit = 0
        for item in signatures:
            for k, v in EXPLOIT.items():
                if k in item.get('name', ''):
                    exploit |= v

        if exploit != 0:
            return str(exploit)

        return ' '

    def parse_dynamic_data(self, report):
        try:
            output = ''
            output += self.md5 + self.crc32  # C_ HASH
            output += self.split + '3'  # C_SIGN_TYPE
            output += self.split + ' '  # C_RELATION
            output += self.split + ' '  # C_NOWINDOW
            output += self.split + ' '  # C_INJECT
            output += self.split + ' '  # C_KEYLOG
            output += self.split + ' '  # C_ATTACK
            output += self.split + ' '  # C_NETFLAG
            output += self.split + self._get_network_summary(report.get('network', {}))  # C_PROTO
            output += self.split + ' '  # C_EXPHEUR
            output += self.split + ' '  # C_AUTORUN
            output += self.split + ' '  # C_SCOPY
            output += self.split + ' '  # C_FILEUP
            output += self.split + ' '  # C_SYSSET
            output += self.split + ' '  # C_ROOTKIT
            output += self.split + self._get_dynamic_caller(report.get('signatures', []))  # C_CALLER
            output += self.split + self._get_dynamic_anti(report.get('signatures', []))  # C_ANTI
            output += self.split + self._get_exploit(report.get('signatures', []))  # C_EXPLOIT
            output += self.split + ' '  # YYY
            output += self.end
            self._write_to_file(output, self.dynamic_data_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def _dynamic_create_perline(self, drop, time_s):
        output = ''
        output += self.md5 + self.crc32  # C_OBJ_ID
        output += self.split + drop.get('md5', '').lower() + drop.get('crc32', '').lower()  # C_Created_OBJ_ID
        output += self.split + str(time_s)  # C_Created_TIME
        output += self.end

        return output

    def parse_dynamic_create(self, report):  # T_DYNAMIC_OBJ_CREATE
        try:
            dropped = report.get('dropped', [])
            if not dropped:
                return

            time_str = report.get('info', {}).get('machine', {}).get('shutdown_on', '')
            time_s = 0
            if time_str:
                time_a = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                time_s = int(time.mktime(time_a))

            output = ''
            for item in dropped:
                output += self._dynamic_create_perline(item, time_s)

            self._write_to_file(output, self.dynamic_create_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    #  添加表
    #  behavior.processes.calls.XXX
    def _get_output_from_call_perline(self, col_dict, call, process):
        output = ''
        for f, col in col_dict.iteritems():

            if col_dict.keys().index(f) == 0:
                self.split = ''

            if col.get('default'):
                output += self.split + col.get('default')
            # elif col.get('range'):
            #     range_list = col.get('range')
            #     output += self.split + range_list[random.randint(0, len(range_list) - 1)]

            # 直接从calls取
            elif col.get('arg') in ["time", "tid", "return_value", "status", "category"]:
                output += self.split + str(call.get(col.get('arg'), ' '))

            # 返回上一级process 取  pid, process_name,time,process_path等字段， 使用首字母大写表示
            elif col.get('arg') in ["Pid", "Process_name", "Time", "Process_path", "Tid"]:
                output += self.split + str(process.get(col.get('arg').lower(), ' '))

            # 在calls.arguments中获取调用api的参数
            else:
                output += self.split + str(call.get('arguments', {}).get(col.get('arg'), ' '))

            if col_dict.keys().index(f) == 0:
                self.split = '||'

        output += self.end

        return output

    def _save_output_by_filter_field(self, report, col_dict, filter_field, table_name, indicators=None):
        try:
            processes = report.get('behavior', {}).get('processes', [])
            if not processes:
                return

            output = ''
            for process in processes:
                calls = process.get('calls', [])
                if not calls:
                    continue

                for call in calls:
                    if str(call.get(filter_field[0], ' ')) not in filter_field[1]:
                        continue

                    #  通过category过滤时，增加对argument中参数的过滤
                    window_name = call.get('arguments', {}).get("window_name", "").lower()
                    class_name = call.get('arguments', {}).get("class_name", "").lower()
                    if filter_field[0] == 'category' and (
                            window_name in indicators or class_name in indicators):
                        output += self._get_output_from_call_perline(col_dict, call, process)

                    elif filter_field[0] == 'api':
                        output += self._get_output_from_call_perline(col_dict, call, process)

            if not output:
                return

            self._write_to_file(output, table_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    #  进程注入
    def parse_dynamic_inject(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_INJECTED_ID'] = {'arg': '', 'default': ' '}
        col_dict['C_INJECTED_METHOD'] = {'arg': '', 'default': ' '}
        col_dict['C_PROCESS_NAME'] = {'arg': 'process_name', 'default': ''}
        col_dict['C_PID'] = {'arg': '', 'default': ' '}
        col_dict['C_PROCFLAG'] = {'arg': '', 'default': '%d' % 0x00000000}
        col_dict['C_PROCTKN'] = {'arg': '', 'default': ' '}

        filter_apinames = ["api", ["Process32NextW", "Process32FirstW"]]

        self._save_output_by_filter_field(report, col_dict, filter_apinames, self.dynamic_inject_name)

    #  杀死其他进程
    def parse_dynamic_killproc(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_KILLED_NAME'] = {'arg': '', 'default': ' '}
        col_dict['C_PROC_IS_SYS'] = {'arg': '', 'default': '%d' % 0x00000000}
        col_dict['C_KILL_TIME'] = {'arg': 'time', 'default': ''}
        col_dict['C_PID'] = {'arg': 'Pid', 'default': ''}
        col_dict['C_KILLED_PID'] = {'arg': '', 'default': ' '}

        filter_apinames = ["api", ["NtTerminateProcess"]]

        self._save_output_by_filter_field(report, col_dict, filter_apinames, self.dynamic_killproc_name)

    #  挂起其他线程
    def parse_dynamic_suspendthr(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_SUSPENED_NAME'] = {'arg': '', 'default': ' '}
        col_dict['C_PROC_IS_SYS'] = {'arg': '', 'default': '%d' % 0x00000000}
        col_dict['C_SUSPENED_TIME'] = {'arg': 'time', 'default': ''}
        col_dict['C_PID'] = {'arg': 'Pid', 'default': ''}
        col_dict['C_SUSPENED_PID'] = {'arg': '', 'default': ' '}

        filter_apinames = ["api", ["NtResumeThread", "NtSuspendThread"]]

        self._save_output_by_filter_field(report, col_dict, filter_apinames, self.dynamic_suspendthr_name)

    #  提升进程权限
    def parse_dynamic_privilege(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_PROCESSNAME'] = {'arg': 'process_name', 'default': ''}
        col_dict['C_PROC_IS_SYS'] = {'arg': '', 'default': ' '}
        col_dict['C_SECVALUE'] = {'arg': '', 'default': ' '}

        filter_apinames = ["api", ["SeAssignPrimaryTokenPrivilege",
                                   "SeBackupPrivilege",
                                   "SeCreateGlobalPrivilege",
                                   "SeCreateTokenPrivilege",
                                   "SeDebugPrivilege",
                                   "SeEnableDelegationPrivilege",
                                   "SeMachineAccountPrivilege",
                                   "SeManageVolumePrivilege",
                                   "SeLoadDriverPrivilege",
                                   "SeRemoteShutdownPrivilege",
                                   "SeRestorePrivilege",
                                   "SeSecurityPrivilege",
                                   "SeShutdownPrivilege",
                                   "SeTakeOwnershipPrivilege",
                                   "SeTcbPrivilege",
                                   "SeTrustedCredManAccessPrivilege"]]

        self._save_output_by_filter_field(report, col_dict, filter_apinames, self.dynamic_privilege_name)

    #  键盘鼠标模拟数据
    def parse_dynamic_vmmk(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_MOUSECOUNT'] = {'arg': '', 'default': ' '}
        col_dict['C_KEYINPUT'] = {'arg': '', 'default': ' '}
        col_dict['C_PID'] = {'arg': 'Pid', 'default': ''}

        filter_apinames = ["api", ["mouse_event", "keybd_event"]]

        self._save_output_by_filter_field(report, col_dict, filter_apinames, self.dynamic_window_name)

    #  窗口状态数据
    def parse_dynamic_window(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_PID'] = {'arg': 'Pid', 'default': ''}
        col_dict['C_TYPE'] = {'arg': '', 'default': ' '}
        col_dict['C_MAXSIZE'] = {'arg': '', 'default': ' '}

        filter_categories = ["category", ["ui"]]
        indicators = [indicator.lower() for indicator in [
            "OLLYDBG",
            "WinDbgFrameClass",
            "pediy06",
            "GBDYLLO",
            "PROCEXPL",
            "Autoruns",
            "gdkWindowTopLevel",
            "API_TRACE_MAIN",
            "TCPViewClass",
            "RegmonClass",
            "FilemonClass",
            "Regmonclass",
            "Filemonclass",
            "PROCMON_WINDOW_CLASS",
            "TCPView - Sysinternals: www.sysinternals.com",
            "File Monitor - Sysinternals: www.sysinternals.com",
            "Process Monitor - Sysinternals: www.sysinternals.com",
            "Registry Monitor - Sysinternals: www.sysinternals.com",
            "Wget [100%%] http://tristan.ssdcorp.net/guid",
            "C:\\Program Files\\Wireshark\\dumpcap.exe",
            "C:\\wireshark\\dumpcap.exe",
            "C:\\SandCastle\\tools\\FakeServer.exe",
            "C:\\\\Python27\\\\python.exe",
            "start.bat - C:\Manual\auto.bat",
            "Fortinet Sunbox",
            "PEiD v0.95",
            "Total Commander 7.0 - Ahnlab Inc.",
            "Total Commander 6.53 - GRISOFT, s.r.o.",
            "Total Commander 7.56a - Avira Soft",
            "Total Commander 7.56a - ROKURA SRL",
            "C:\\strawberry\\perl\\bin\\perl.exe",
            "ThunderRT6FormDC",
            "TfrmMain",
            "Afx:400000:b:10011:6:350167",
            "TApplication",
            "SmartSniff",
            "ConsoleWindowClass",
            "18467-41"
        ]]

        self._save_output_by_filter_field(report, col_dict, filter_categories, self.dynamic_window_name, indicators)

    # behavior.generic.summary.XXX
    def _get_filename_from_filepath(self, filepath):
        """
        获取'\\'路径中的文件名
        :param filepath: 文件路径
        :return: 文件名(带扩展名)
        """
        if filepath.find('\\'):
            return filepath.rsplit('\\', 1)[1]
        return ' '

    def _is_match_filter_reg(self, item, filter_reg):
        """
        判断一个字符串是否符合正则表达式列表
        :param item: 字符串
        :param filter_reg: 列表(元素为正则表达式)
        :return:
        """
        for reg in filter_reg:
            if re.search(reg, str(item), flags=re.IGNORECASE):
                return True

        return False

    def _get_fileopt_info_perline(self, col_dict, fileopt_item, gen):
        output = ''
        if not fileopt_item:
            return ''
        for f, col in col_dict.iteritems():

            if col_dict.keys().index(f) == 0:
                self.split = ''

            if col.get('default'):
                    output += self.split + col.get('default')
            # elif col.get('range'):
            #     range_list = col.get('range')
            #     output += self.split + range_list[random.randint(0, len(range_list) - 1)]

            elif col.get('arg') in ["newfilepath", "oldfilepath"] and isinstance(fileopt_item, list):
                if len(fileopt_item) == 2:
                    index = 1 if col.get('arg') == "newfilepath" else 0
                    filepath = fileopt_item[index]
                    output += self.split + str(filepath) if filepath else ' '
                else:
                    output += self.split + ' '

            elif col.get('arg') == "filepath":
                output += self.split + str(fileopt_item) if fileopt_item else ' '

            # 返回上一层 generic 获取pid, process_name等字段
            elif col.get('arg') in ["Pid", "Process_name", "Process_path", "Old_name", "New_name"]:
                output += self.split + str(gen.get(col.get('arg').lower(), ' '))
            else:
                output += self.split + ' '

            if col_dict.keys().index(f) == 0:
                self.split = '||'

        output += self.end

        return output

    def _save_output_by_fileopt(self, report, col_dict, file_opt, table_name, filter_reg=None):
        try:
            generic = report.get('behavior', {}).get('generic', [])
            if not generic:
                return

            output = ''
            for gen in generic:
                fileopt_list = gen.get('summary', {}).get(file_opt, [])
                if not fileopt_list:
                    continue

                for item in fileopt_list:

                    # 包含reg
                    if filter_reg:
                        if self._is_match_filter_reg(item, filter_reg):

                            # 获取指定cmd 的参数信息，并添加到gen中
                            if filter_reg == ["\s+rename\s+", "\s+ren\s+"]:
                                x = re.search("\s+(rename|ren)\s+(\S+)\s+(\S+)", item)
                                if x:
                                    gen['old_name'] = x.group(2) if x.group(2) else ' '
                                    gen['new_name'] = x.group(3) if x.group(3) else ' '
                                else:
                                    continue

                            output += self._get_fileopt_info_perline(col_dict, item, gen)

                        else:
                            continue

                    # 不包含reg
                    else:
                        output += self._get_fileopt_info_perline(col_dict, item, gen)

            if not output:
                return

            self._write_to_file(output, table_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    #  挂起其他进程
    def parse_dynamic_suspendproc(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_SUSPENED_NAME'] = {'arg': '', 'default': ' '}
        col_dict['C_PROC_IS_SYS'] = {'arg': '', 'default': '%d' % 0x00000000}
        col_dict['C_SUSPENED_TIME'] = {'arg': '', 'default': ' '}
        col_dict['C_PID'] = {'arg': 'Pid', 'default': ''}
        col_dict['C_SUSPENED_PID'] = {'arg': '', 'default': ' '}

        file_opt = "command_line"
        filter_reg = ["\s+pssuspend\s+"]

        self._save_output_by_fileopt(report, col_dict, file_opt, self.dynamic_suspendproc_name, filter_reg)

    #  CC 攻击数据
    def parse_dynamic_cc(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_IPV4'] = {'arg': '', 'default': ' '}
        col_dict['C_IPV6'] = {'arg': '', 'default': ' '}
        col_dict['C_DOMAIN'] = {'arg': '', 'default': ' '}
        col_dict['C_PID'] = {'arg': 'Pid', 'default': ''}
        col_dict['C_PORT'] = {'arg': '', 'default': ' '}

        file_opt = "command_line"
        filter_reg = [".*ddos.*"]

        self._save_output_by_fileopt(report, col_dict, file_opt, self.dynamic_cc_name, filter_reg)

    #  隐藏文件
    def parse_dynamic_hidemodule(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_HIDED_ID'] = {'arg': '', 'default': ' '}
        col_dict['C_HIDEDFILENAME'] = {'arg': '', 'default': ' '}
        col_dict['C_HIDEBUFF'] = {'arg': '', 'default': ' '}

        file_opt = "regkey_written"

        filter_reg = [
            ".*\\\\Software\\\\(Wow6432Node\\\\)?Microsoft\\\\Windows\\\\CurrentVersion\\\\Explorer\\\\Advanced\\\\Hidden$",
            ".*\\\\Software\\\\(Wow6432Node\\\\)?Microsoft\\\\Windows\\\\CurrentVersion\\\\Explorer\\\\Advanced\\\\ShowSuperHidden$",
            ".*\\\\Software\\\\(Wow6432Node\\\\)?Microsoft\\\\Windows\\\\CurrentVersion\\\\Explorer\\\\Advanced\\\\SuperHidden$",
        ]

        self._save_output_by_fileopt(report, col_dict, file_opt, self.dynamic_hidemodule_name, filter_reg)

    #  文件自拷贝
    def parse_dynamic_filecopy(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_COPY_TYPE'] = {'arg': '', 'default': '%d' % 0x00000001}
        col_dict['C_SRCFILENAME'] = {'arg': 'oldfilepath', 'default': ''}
        col_dict['C_DECFILENAME'] = {'arg': 'newfilepath', 'default': ''}

        file_opt = "file_copied"

        self._save_output_by_fileopt(report, col_dict, file_opt, self.dynamic_filecopy_name)

    # 文件名变更
    def parse_dynamic_filerename(self,report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_SRCFILENAME'] = {'arg': 'Old_name', 'default': ''}
        col_dict['C_DECFILENAME'] = {'arg': 'New_name', 'default': ''}
        col_dict['C_TIME'] = {'arg': '', 'default': ' '}
        col_dict['C_IS_SYS_FILE'] = {'arg': '', 'default': '%d' % 0x00000000}

        file_opt = "command_line"
        filter_reg = ["\s+rename\s+", "\s+ren\s+"]

        self._save_output_by_fileopt(report, col_dict, file_opt, self.dynamic_filerename_name, filter_reg)

    #  文件移动
    def parse_dynamic_filemove(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_SRCFILENAME'] = {'arg': 'oldfilepath', 'default': ''}
        col_dict['C_DECFILENAME'] = {'arg': 'newfilepath', 'default': ''}
        col_dict['C_TIME'] = {'arg': '', 'default': ' '}
        col_dict['C_IS_SYS_FILE'] = {'arg': '', 'default': ' '}

        file_opt = "file_moved"

        self._save_output_by_fileopt(report, col_dict, file_opt, self.dynamic_filemove_name)

    #  文件删除
    def parse_dynamic_filedelete(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_SRCFILENAME'] = {'arg': 'filepath', 'default': ''}
        col_dict['C_IS_SYS_FILE'] = {'arg': '', 'default': ' '}

        file_opt = "file_deleted"

        self._save_output_by_fileopt(report, col_dict, file_opt, self.dynamic_filedelete_name)

    # 文件被重写
    def parse_dynamic_filerewrite(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_MODIFY_FILE_TYPE'] = {'arg': '', 'default': ' '}
        col_dict['C_NEW_FILE_TYPE'] = {'arg': '', 'default': ' '}
        col_dict['C_MODIFY_FILE_HIDE_ATTR'] = {'arg': '', 'default': ' '}
        col_dict['C_FILENAME'] = {'arg': 'filepath', 'default': ''}
        col_dict['C_MODIFY_OBJ_TYPE'] = {'arg': '', 'default': ' '}

        file_opt = "file_recreated"

        self._save_output_by_fileopt(report, col_dict, file_opt, self.dynamic_filerewrite_name)

    # 文件访问数据
    def parse_dynamic_fileaccess(self, report):
        col_dict = OrderedDict()
        col_dict['C_SIGN'] = {'arg': '', 'default': self.md5 + self.crc32}
        col_dict['C_FILE_TYPE'] = {'arg': '', 'default': ' '}
        col_dict['C_ISSEARCHEDFILENAME'] = {'arg': '', 'default': ' '}
        col_dict['C_FILENAME'] = {'arg': 'filepath', 'default': ''}
        col_dict['C_NETFLAG'] = {'arg': '', 'default': ' '}

        file_opt = "file_read"

        self._save_output_by_fileopt(report, col_dict, file_opt, self.dynamic_fileaccess_name)

    # smtp通信数据
    def _dynamic_smtp_perline(self, smtp):
        output = ''
        output += self.md5 + self.crc32  # C_SIGN

        src_ipv4 = str(smtp.get('src', ''))
        src = socket.ntohl(struct.unpack("I", socket.inet_aton(src_ipv4))[0]) if src_ipv4 else ' '
        output += self.split + str(src)  # C_SRC_IPV4
        output += self.split + ' '  # C_SRC_IPV6

        if str(smtp.get('dst', '')).startswith('192.168'):
            return ''
        dst_ipv6 = smtp.get('dst', '')
        dst = socket.ntohl(struct.unpack("I", socket.inet_aton(dst_ipv6))[0]) if dst_ipv6 else ' '
        output += self.split + str(dst)  # C_DST_IPV4
        output += self.split + ' '  # C_DST_IPV6

        sport = smtp.get('sport', '')
        output += self.split + str(sport) if sport else ' '  # C_SPORT
        dport = smtp.get('dport', '')
        output += self.split + str(dport) if dport else ' '  # C_DPORT

        output += self.split + ' '  # C_FROM

        # c_to = smtp.get('to', '')
        # output += self.splic + ';'.join(c_to) if c_to else ' '  # C_TO
        output += self.splic + ' '  # C_TO
        output += self.end
        return output

    def parse_dynamic_smtp(self, report):
        try:
            smtp = report.get('network', {}).get('smtp', [])
            if not smtp:
                return

            output = ''
            for item in smtp:
                output += self._dynamic_smtp_perline(item)

            self._write_to_file(output, self.dynamic_smtp_name)
        except Exception as err:
            logging.warn('{0}'.format(err))

    def run(self):
        try:
            report_path = self.sample_path + '/reports/report.json'
            logging.debug('report_path:{0}'.format(report_path))
            with open(report_path, 'rb') as fd:
                report_json = simplejson.load(fd)
                target = report_json.get('target', {}).get('file', {})

                if not target:
                    return

                self.md5 = target.get('md5', '').lower()
                self.crc32 = target.get('crc32', '').lower()

                self.parse_base_data(report_json)
                self.parse_black_data(report_json)
                self.parse_dynamic_base(report_json)
                self.parse_dynamic_process(report_json)
                self.parse_dynamic_regeset(report_json)
                self.parse_dynamic_domains(report_json)
                self.parse_dynamic_http(report_json)
                self.parse_dynamic_tcp(report_json)
                self.parse_dynamic_udp(report_json)
                self.parse_dynamic_dns(report_json)
                self.parse_dynamic_data(report_json)
                self.parse_dynamic_create(report_json)

                self.parse_dynamic_inject(report_json)
                self.parse_dynamic_killproc(report_json)
                self.parse_dynamic_suspendthr(report_json)
                self.parse_dynamic_privilege(report_json)
                self.parse_dynamic_vmmk(report_json)
                self.parse_dynamic_window(report_json)

                self.parse_dynamic_suspendproc(report_json)
                self.parse_dynamic_cc(report_json)
                self.parse_dynamic_hidemodule(report_json)
                self.parse_dynamic_filecopy(report_json)
                self.parse_dynamic_filerename(report_json)
                self.parse_dynamic_filemove(report_json)
                self.parse_dynamic_filedelete(report_json)
                self.parse_dynamic_filerewrite(report_json)
                self.parse_dynamic_fileaccess(report_json)
                self.parse_dynamic_smtp(report_json)
        except Exception as err:
            logging.exception('{0}'.format(err))


def get_new_samples():
    ret_lists = []
    for lists in os.listdir(BASE_DIR):
        path = os.path.join(BASE_DIR, lists)
        if os.path.isdir(path) and not os.path.islink(path):
            ret_lists.append(path)

    return ret_lists


def main():
    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.isdir(BASE_DIR):
        os.makedirs(BASE_DIR)

    # if not os.path.isdir(TMP_DIR):  # For test
    #     os.mkdir(TMP_DIR)

    while True:
        # get new report
        samples = get_new_samples()
        # logging.warn('samples: %s ' % samples)
        for sample_path in samples:
            if sample_path and os.path.exists(sample_path + '/reports/report.json'):
                trans = TransReport(sample_path)
                trans.run()

                # move report to OUTPUT_DIR
                ori_report = sample_path + '/reports/report.json'
                dst_report = OUTPUT_DIR + trans.md5 + trans.crc32 + '.json'
                import stat
                os.chmod(ori_report, stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)
                shutil.move(ori_report, dst_report)

                # delete this report
                shutil.rmtree(sample_path)
                # shutil.move(sample_path, TMP_DIR)  # For test

        time.sleep(1)


# def test():
#     sample_path = '/data/output1/hiddenfile.json'
#     trans = TransReport(sample_path)
#     trans.run()

if __name__ == '__main__':
    main()