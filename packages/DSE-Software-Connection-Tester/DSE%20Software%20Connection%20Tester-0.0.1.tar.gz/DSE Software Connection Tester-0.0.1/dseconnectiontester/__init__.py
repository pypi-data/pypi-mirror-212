import subprocess
from os.path import exists
from typing import List
import logging
import http.client
from enum import Enum


class CustomLogger:
    def __init__(
            self,
            caller: str = 'Main',
            log_level: int = logging.INFO,
            date_format: str = '%d-%m-%Y %H:%M:%S',
            filename: str | None = None
    ):
        self.caller = caller
        self.log_level = log_level
        self.date_format = date_format
        self.filename = filename
        self.formatter = logging.Formatter(fmt=f'%(asctime)s | %(name)s | %(levelname)s: %(message)s', datefmt=date_format)
        self.logger = logging.getLogger(name=caller)
        self.logger.setLevel(level=log_level)
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(level=log_level)
        self.console_handler.setFormatter(fmt=self.formatter)
        self.logger.addHandler(hdlr=self.console_handler)
        if filename:
            self.file_handler = logging.FileHandler(filename=filename)
            self.file_handler.setLevel(level=log_level)
            self.file_handler.setFormatter(fmt=self.formatter)
            self.logger.addHandler(hdlr=self.file_handler)

    def instance(
            self,
            caller: str,
            log_level: int = logging.INFO,
            date_format: str = '%d-%m-%Y %H:%M:%S',
            filename: str | None = None):
        return CustomLogger(caller=caller, log_level=log_level, date_format=date_format, filename=filename)

    def debug(self, message: str):
        self.logger.debug(msg=message)

    def info(self, message: str):
        self.logger.info(msg=message)

    def warning(self, message: str):
        self.logger.warning(msg=message)

    def error(self, message: str):
        self.logger.error(msg=message)

    def critical(self, message: str):
        self.logger.critical(msg=message)


class DnsRecordType(Enum):
    A = 'A',
    AAAA = 'AAAA',
    AFSDB = 'AFSDB',
    ANY = 'ANY',
    APL = 'APL',
    AXFR = 'AXFR',
    CAA = 'CAA',
    CDNSKEY = 'CDNSKEY',
    CDS = 'CDS',
    CERT = 'CERT',
    CNAME = 'CNAME',
    CSYNC = 'CSYNC',
    DHCID = 'DHCID',
    DLV = 'DLV',
    DNAME = 'DNAME',
    DNSKEY = 'DNSKEY',
    DS = 'DS',
    EUI48 = 'EUI48',
    EUI64 = 'EUI64',
    HINFO = 'HINFO',
    HIP = 'HIP',
    IPSECKEY = 'IPSECKEY',
    IXFR = 'IXFR',
    KEY = 'KEY',
    KX = 'KX',
    LOC = 'LOC',
    MX = 'MX',
    NAPTR = 'NAPTR',
    NS = 'NS',
    NSEC = 'NSEC',
    NSEC3 = 'NSEC3',
    NSEC3PARAM = 'NSEC3PARAM',
    NULL = 'NULL',
    NXT = 'NXT',
    OPENPGPKEY = 'OPENPGPKEY',
    OPT = 'OPT',
    PTR = 'PTR',
    PX = 'PX',
    RKEY = 'RKEY',
    RP = 'RP',
    RRSIG = 'RRSIG',
    RT = 'RT',
    SIG = 'SIG',
    SMIMEA = 'SMIMEA',
    SOA = 'SOA',
    SRV = 'SRV',
    SSHFP = 'SSHFP',
    SVCB = 'SVCB',
    TA = 'TA',
    TKEY = 'TKEY',
    TLSA = 'TLSA',
    TSIG = 'TSIG',
    TXT = 'TXT',
    URI = 'URI',
    WKS = 'WKS',
    ZONEMD = 'ZONEMD',


class DnsLookupClient:
    def __init__(self, api_host: str, api_key: str, logger: CustomLogger | None):
        self.api_host = api_host
        self.api_key = api_key
        self.logger = logger.instance(
            caller=self.__class__.__name__,
            log_level=logger.log_level,
            date_format=logger.date_format,
            filename=logger.filename
        )

    def resolve_domain(self, domain: str, record_type: DnsRecordType) -> bool:
        if self.logger:
            self.logger.info(f'Trying to resolve domain `{domain}` from {self.api_host}.')
        headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.api_host
        }
        connection = http.client.HTTPSConnection(self.api_host)
        connection.request('GET', f'/simple?domain={domain}&recordType={record_type}', headers=headers)
        response = connection.getresponse()
        if response.status == 200:
            if self.logger:
                self.logger.info(f'Domain `{domain} successfully resolved from {self.api_host}`.')
            return True
        else:
            if self.logger:
                self.logger.warning(f'Domain `{domain} failed to resolve from {self.api_host}`.')
            return False


class DnsEntry:
    def __init__(self, domain: str, ip: str, record_type: DnsRecordType):
        self.resolvable: bool = False
        self.pingable: bool = False
        self.domain = domain
        self.ip = ip
        self.recordType = record_type


class FileParser:
    def __init__(self, file: str, logger: CustomLogger | None):
        self.file = file
        self.logger = logger.instance(
            caller=self.__class__.__name__,
            log_level=logger.log_level,
            date_format=logger.date_format,
            filename=logger.filename
        )

    def parse_dns_entries(self) -> List[DnsEntry]:
        if not exists(self.file):
            if self.logger:
                self.logger.critical(f'File `{self.file}` does not exist.')
            raise IOError(f'File {self.file} does not exist.')
        entries: List[DnsEntry] = list()
        if self.logger:
            self.logger.info(f'Trying to parse file `{self.file}`.')
        with open(self.file) as dns_entries:
            for dns_entry in dns_entries:
                if self.logger:
                    self.logger.info(f'Parsing row `{dns_entry.strip()}`.')
                entry_parts = dns_entry.strip().split(' ')
                entries.append(DnsEntry(entry_parts[0], entry_parts[1], DnsRecordType[entry_parts[2]]))
        if self.logger:
            self.logger.info(f'Parsed a total of {len(entries)} rows.')
        return entries


class ConnectionTester:
    def __init__(self, logger: CustomLogger | None):
        self.logger = logger.instance(
            caller=self.__class__.__name__,
            log_level=logger.log_level,
            date_format=logger.date_format,
            filename=logger.filename
        )

    def resolve_dns(self, domain: str) -> bool:
        if self.logger:
            self.logger.info(f'Trying to resolve domain `{domain}` locally.')
        process = subprocess.Popen(['nslookup', domain], stdout=subprocess.PIPE)
        output = process.communicate()[0].split('\n'.encode('utf-8'))
        for data in output:
            if domain.encode('utf-8') in data:
                if self.logger:
                    self.logger.info(f'Successfully resolved domain `{domain}` locally.')
                return True
        if self.logger:
            self.logger.warning(f'Failed to resolve domain `{domain}` locally.')
        return False

    def ping(self, ip: str) -> bool:
        if self.logger:
            self.logger.info(f'Trying to ping IP address `{ip}` locally.')
        process = subprocess.Popen(['ping', '-n', '1', ip], stdout=subprocess.PIPE)
        output = process.communicate()[0]
        if f'Reply from {ip}' in output.decode('utf-8'):
            if self.logger:
                self.logger.info(f'Successfully pinged IP address `{ip}`.')
            return True
        else:
            if self.logger:
                self.logger.warning(f'Failed to ping IP address `{ip}`.')
            return False
