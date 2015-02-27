# Home Assistant Vera Component
Provides basic integration between home-assistant and Vera Z-Wave controllers.

This is a custom component designed to interface between [Home Assistant](https://github.com/balloob/home-assistant) and [Vera Z-Wave](http://getvera.com/controllers/veralite/) home automation controllers.

## Installation

Clone this repository to you local machine and copy the `light', `switch` and `external` directories into the `home-assistant/config/custom-components` directory.

## Configuation

The following are the settings you can add to your home-assistant.conf file to configure the component

### Lights
The `device_data` parameter is optional, if not specified all switches found on the Vera will be included as lights.  If it is present only the Z-Wave switches specified will be included as lights.  The `name` parameter is optional and if present will override the name specified in the Vera controller in the home-assistant UI.  The `id` parameter should be set to the switch's Vera device id.
	[light]
	platform=vera
	device_data=[{"id" : 12, "name": "Lounge Light"}]
	vera_controller_url=http://<your vera ip>:3480/

### Switches
The `device_data` parameter is optional. The `name` parameter is optional and if present will override the name specified in the Vera controller in the home-assistant UI.
	[switch]
	platform=vera
	device_data=[{"id" : 12, "name": "Lounge Light"}]
	vera_controller_url=http://<your vera ip>:3480/