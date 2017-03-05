#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

"""
@author:yangzhou
@contact:@yangzhou@antiy.cn
@create:2016-04-13 16:05
"""

__author__ = 'Yangzhou'
__version__ = '0.1'


class OpenStackClient:
    def __init__(self, user, password, auth_url, region_name, project_name, auth_version='2.0_password'):
        """
        init function
        create open_stack connection
        :return:
        """
        self.user = user
        self.password = password
        self.auth_url = auth_url
        self.region_name = region_name
        self.project_name = project_name
        self.auth_version = auth_version

        provider = get_driver(Provider.OPENSTACK)
        self.conn = provider(self.user, self.password,
                             ex_force_auth_url=self.auth_url,
                             ex_force_auth_version=self.auth_version,
                             ex_tenant_name=self.project_name,
                             ex_force_service_region=self.region_name)

    def create_instance(self, instance_dict, override=False):
        """
        :param instance_dict:
        :param override:
        :return:
        """
        instance_name = instance_dict.get('prefix')
        image_name = instance_dict.get('image')
        flavor_name = instance_dict.get('flavor')
        network_name_list = instance_dict.get('network')
        key_pair_name = instance_dict.get('keypair')
        ex_user_data = instance_dict.get('userdata')

        image = [temp_image for temp_image in self.conn.list_images() if temp_image.name == image_name][0]
        flavor = [temp_flavor for temp_flavor in self.conn.list_sizes() if temp_flavor.name == flavor_name][0]
        network = []
        for network_name in network_name_list:
            for temp_network in self.conn.ex_list_networks():
                if temp_network.name == network_name:
                    network.append(temp_network)

        instance_exists = False
        for instance in self.conn.list_nodes():
            # 检查同名实例是否存在，存在的话，判断是否覆盖该镜像重新创建
            if instance.name == instance_name:
                temp_instance = instance
                # 判断是否覆
                if override:
                    try:
                        self.conn.destroy_node(temp_instance)
                    except Exception as e:
                        return 2, 'Delete %s failed, err_info:%s' % (instance.name, e.message)
                else:
                    instance_exists = True
        #  创建实例
        if not instance_exists:
            try:
                self.conn.create_node(name=instance_name,
                                      image=image,
                                      size=flavor,
                                      networks=network,
                                      ex_keyname=key_pair_name,
                                      ex_userdata=ex_user_data)
            except Exception as e:
                return 2, 'Create %s failed, err_info:%s' % (instance_name, e.message)
            return 1, 'Create %s success' % instance_name
        else:
            return 3, 'Remain %s instance' % instance.name

    def list_key_pair(self):
        """
        列出已经导入的公钥
        :return:
        """
        key_pair_list = []
        for key_pair in self.conn.list_key_pairs():
            key_pair_list.append(key_pair)
        return key_pair_list

    def check_ssh(self, keypair_name, pub_key_file):
        """
        检查ssh公钥是否已经导入
        :param pub_key_file:
        :return:
        """
        key_pair_exists = False
        for key_pair in self.conn.list_key_pairs():
            if key_pair.name == keypair_name:
                key_pair_exists = True

        if key_pair_exists:
            return False
        else:
            self.conn.import_key_pair_from_file(keypair_name, pub_key_file)
            return True

    def list_images(self):
        """
        列出所有的镜像及快照
        :return:获取成功 返回True和镜像及快照list 获取失败，返回False，和错误信息
        """
        images_list = []
        images = self.conn.list_images()
        for image in images:
            images_list.append(image)
        return True, images_list

    def list_flavors(self):
        """
        列出所有云主机类型
        :return:获取成功 返回True和云主机类型list 获取失败，返回False，和错误信息
        """
        flavors_list = []
        try:
            flavors = self.conn.list_sizes()
            for flavor in flavors:
                flavors_list.append(flavor)
        except Exception as e:
            err_info = 'err_info:%s' % e.message
            return False, err_info
        return True, flavors_list

    def list_networks(self):
        """
        列出所有网络
        :return:获取成功 返回True和网络list 获取失败，返回False，和错误信息
        """
        networks_list = []
        try:
            networks = self.conn.ex_list_networks()
            for network in networks:
                networks_list.append(network)
        except Exception as e:
            err_info = 'err_info:%s' % e.message
            return False, err_info
        return True, networks_list

    def list_security(self):
        """
        列出当前所有安全组信息
        :return:
        """
        security_group_list = []
        try:
            for security_group in self.conn.ex_list_security_groups():
                security_group_list.append(security_group)
        except Exception as e:
            err_info = 'err_info:%s' % e.message
            return False,  err_info
        return True, security_group_list

    def list_all_node(self):
        """

        :return:
        """
        all_node = []
        for node in self.conn.list_nodes():
            all_node.append(node)
        return all_node

    def delete_node(self, instance_name):
        """
        删除实例
        :param instance_name:
        :return:
        """
        for instance in self.conn.list_nodes():
            if instance.name == instance_name:
                delete_instance = instance
                try:
                    self.conn.destroy_node(delete_instance)
                except Exception as e:
                    return False, e.message
                return True, 'delete success'
        return False, 'No this instance'