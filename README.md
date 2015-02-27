# Home Assistant Vera Component
Provides basic integration between home-assistant and Vera Z-Wave controllers.

This is a custom component designed to interface between [Home Assistant](https://github.com/balloob/home-assistant) and Vera Z-Wave home automation controllers.

## Configuation

The following are the settings you can add to your home-assistant.conf file to configure the component

### Lights
	[light]
	platform=vera
	device_data=[{"id" : 12, "name": "Lounge Light"}]
	vera_controller_url=http://<your vera ip>:3480/