__author__ = 'jamespcole'

import json
import time

import requests

"""
Vera Controller Python API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This lib is designed to simplify communication with Vera Z-Wave controllers
"""

class VeraController(object):

	def __init__(self, baseUrl):
		self.BASE_URL = baseUrl	
		self.devices = []

	def get_simple_devices_info(self): 

		simpleRequestUrl = self.BASE_URL + "/data_request?id=sdata"
		j = requests.get(simpleRequestUrl).json()

		self.categories = {}
		cats = j.get('categories')

		for cat in cats:
			self.categories[cat.get('id')] = cat.get('name')

		self.device_id_map = {}

		devs = j.get('devices')
		for dev in devs:
			dev['categoryName'] = self.categories.get(dev.get('category'))
			self.device_id_map[dev.get('id')] = dev


	def get_devices(self, categoryFilter=''):	

		# the Vera rest API is a bit rough so we need to make 2 calls to get all the info e need
		self.get_simple_devices_info()

		arequestUrl = self.BASE_URL + "/data_request?id=status&output_format=json"
		j = requests.get(arequestUrl).json()

		self.devices = []
		items = j.get('devices')

		for item in items:
			item['deviceInfo'] = self.device_id_map.get(item.get('id'))
			if item.get('deviceInfo') and item.get('deviceInfo').get('categoryName') == 'Switch':
				self.devices.append(VeraSwitch(item, self))
			else:
				self.devices.append(VeraDevice(item, self))

		if categoryFilter == '':
			return self.devices
		else:
			devices = []
			for item in self.devices:
				if item.category == categoryFilter:
					devices.append(item)
			return devices



class VeraDevice(object):

	def __init__(self, aJSonObj, veraController):
		self.jsonState = aJSonObj
		self.deviceId = self.jsonState.get('id')
		self.veraController = veraController
		self.name = ''
		if self.jsonState.get('deviceInfo'):
			self.category = self.jsonState.get('deviceInfo').get('categoryName')
			self.name = self.jsonState.get('deviceInfo').get('name')			
		else:
			self.category = ''

		if not self.name:
			if self.category:
				self.name = 'Vera ' + self.category + ' ' + str(self.deviceId)
			else:
				self.name = 'Vera Device ' + str(self.deviceId)


	def set_value(self, name, value):
		for item in self.jsonState.get('states'):
			if item.get('variable') == name:
				serviceName = item.get('service')
				payload = {'id': 'lu_action', 'output_format': 'json', 'DeviceNum': self.deviceId, 'serviceId': serviceName, 'action': 'Set' + name, 'new' + name + 'Value': value}
				requestUrl = self.veraController.BASE_URL + "/data_request"
				r = requests.get(requestUrl, params=payload)
				item['value'] = value

	def get_value(self, name):
		for item in self.jsonState.get('states'):
			if item.get('variable') == name:
				return item.get('value')
		return None

	def refresh_value(self, name):
		for item in self.jsonState.get('states'):
			if item.get('variable') == name:
				serviceName = item.get('service')
				payload = {'id': 'variableget', 'output_format': 'json', 'DeviceNum': self.deviceId, 'serviceId': serviceName, 'Variable': name}
				requestUrl = self.veraController.BASE_URL + "/data_request"
				r = requests.get(requestUrl, params=payload)
				item['value'] = r.text
				return item.get('value')
		return None


class VeraSwitch(VeraDevice):

	def __init__(self, aJSonObj, veraController):
		super().__init__(aJSonObj, veraController)

	def switch_on(self):
		self.set_value('Target', 1)

	def switch_off(self):
		self.set_value('Target', 0)

	def is_switched_on(self):
		self.refresh_value('Status')
		val = self.get_value('Status')
		if val == '1':
			return True
		else:
			return False