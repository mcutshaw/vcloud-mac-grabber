#!/usr/bin/python3
import requests
import base64
import threading
import datetime
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree
import configparser

class vcloud:
    def __init__(self,config):
        self.config = config
        self.user = config['Main']['User']
        self.passwd = config['Main']['Password']
        self.host = config['Main']['Host']
        self.org = config['Main']['Org']

        self.api='https://%s/api' % self.host
        self.session_url='%s/sessions' % self.api
        self.query_url='%s/query' % self.api

        self.headers={'Accept': 'application/*+xml;version=30.0'}

        self._set_auth_token()

    def _set_auth_token(self):
        auth_str = '%s@%s:%s' % (self.user, self.org, self.passwd)
        auth=base64.b64encode(auth_str.encode()).decode('utf-8')
        self.headers['Authorization'] = 'Basic %s' % auth
        resp = requests.post(url=self.session_url, headers=self.headers)
        del self.headers['Authorization']
        self.headers['x-vcloud-authorization'] = resp.headers['x-vcloud-authorization']

    def getVappHrefs(self):
        l = []
        w = []
        for key in self.config['Vapps']:
            w.append(self.config['Vapps'][key])
        for x in range(1,100):
            resp = requests.get(url=self.api+'/vApps/query?page='+ str(x),headers=self.headers)
            xml_content = resp.text 
            root = ElementTree.fromstring(xml_content)
            if 'majorErrorCode' in root.attrib:
                break
            for child in root:
                if 'numberOfVMs' in child.attrib:
                    if child.attrib['name'] in w:
                        l.append((child.attrib['name'],child.attrib['href']))
        return l

    def getVMs(self, vapp):
        resp = requests.get(url=vapp[1],headers=self.headers)
        xml_content = resp.text 
        root = ElementTree.fromstring(xml_content)
        for child in root:
            if 'Children' in child.tag:
                return [ subchild.attrib['href'] for subchild in child ]

    def getMAC(self, vm):
        resp = requests.get(url=vm,headers=self.headers)
        xml_content = resp.text 
        root = ElementTree.fromstring(xml_content)
        name = root.attrib['name']

        resp = requests.get(url=vm+'/networkConnectionSection',headers=self.headers)
        xml_content = resp.text 
        root = ElementTree.fromstring(xml_content)
        for item in root[2]:
            if 'MACAddress' in item.tag:
                return (name,item.text)
           
        