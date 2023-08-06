from dataclasses import field, dataclass

import requests
import aiohttp
from sqlsprinkler import API


@dataclass
class Zone:
    """ This class represents a SQL Sprinkler zone. """
    host = "none"
    name: str = field(default_factory=str)
    gpio: int = field(default_factory=int)
    time: int = field(default_factory=int)
    enabled: bool = field(default_factory=bool)
    auto_off: bool = field(default_factory=bool)
    system_order: int = field(default_factory=int)
    state: bool = field(default_factory=bool)
    id: int = field(default_factory=int)
    session = requests.Session()


    async def _async_set_state(self, state: bool):
        url = f"{self.host}/{API.ZONE_URL}"
        payload = {"id":self.id, "state": state}
        async with aiohttp.ClientSession() as session:
            async with session.put(url,json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Could not turn on zone {id}, HTTP status: {response.status}, payload: {payload}")
                else:
                    self.state = state


    async def async_turn_on(self) -> None:
        await self._async_set_state(True)


    async def async_turn_off(self) -> None:
        await self._async_set_state(False)


    def turn_on(self) -> None:
        """
        Turns the zone on.
        :return: None
        """
        self.state = True
        # send request to API_ZONE_URL with ID and state
        url = "{}/{}"
        self.session.put(f"{self.host}/{API.ZONE_URL}", json={"id": self.id, "state": self.state})


    def turn_off(self) -> None:
        """
        Turns the zone off.
        :return: None
        """
        self.state = False
        # send request to API_ZONE_URL with ID and state
        self.session.put(f"{self.host}/{API.ZONE_URL}", json={"id": self.id, "state": self.state})

    def update(self) -> None:
        """
        Updates the state of the zone.
        :return: None
        """
        # send request to API_ZONE_INFO_URL with ID
        url = "{}/{}/{}".format(self.host, API.ZONE_INFO_URL, self.id)
        response = self.session.get(url)
        if response.status_code != 200:
            raise Exception("Failed to update zone {}".format(self.id))
        response = response.json()
        self.name = response['name']
        self.gpio = response['gpio']
        self.time = response['time']
        self.enabled = response['enabled']
        self.auto_off = response['auto_off']
        self.system_order = response['system_order']
        self.state = response['state']


    async def async_update(self) -> None:
        url = "{}/{}/{}".format(self.host, API.ZONE_INFO_URL, self.id)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as request:
                response = await request.json()
                self.name = response['name']
                self.gpio = response['gpio']
                self.time = response['time']
                self.enabled = response['enabled']
                self.auto_off = response['auto_off']
                self.system_order = response['system_order']
                self.state = response['state']
                print("Updating zone {}".format(self.id))

    def enable(self):
        self.enabled = True
        self.update_other(self)

    def disable(self):
        self.enabled = False
        self.update_other(self)

    def set_time(self, time: int) -> None:
        self.time = time
        self.update_other(self)

    def set_gpio(self, gpio: int) -> None:
        self.gpio = gpio
        self.update_other(self)

    def set_name(self, name: str) -> None:
        self.name = name
        self.update_other(self)

    def set_auto_off(self, auto_off: bool) -> None:
        self.auto_off = auto_off
        self.update_other(self)

    def set_system_order(self, system_order: int) -> None:
        self.system_order = system_order
        self.update_other(self)

    async def async_enable(self):
        self.enabled = True
        await self.async_update_other(self)

    async def async_disable(self):
        self.enabled = False
        await self.async_update_other(self)

    async def async_set_time(self, time: int) -> None:
        self.time = time
        await self.async_update_other(self)

    async def async_set_gpio(self, gpio: int) -> None:
        self.gpio = gpio
        await self.async_update_other(self)

    async def async_set_name(self, name: str) -> None:
        self.name = name
        await self.async_update_other(self)

    async def async_set_auto_off(self, auto_off: bool) -> None:
        self.auto_off = auto_off
        await self.async_update_other(self)

    async def async_set_system_order(self, system_order: int) -> None:
        self.system_order = system_order
        await self.async_update_other(self)


    def update_other(self, other) -> None:
        """
        Updates the state of the zone.
        :param other: The zone to update with.
        :return: None
        """
        self.name = other.name
        self.gpio = other.gpio
        self.time = other.time
        self.enabled = other.enabled
        self.auto_off = other.auto_off
        self.system_order = other.system_order

        # send request to API_ZONE_UPDATE_URL with name, gpio, time, enabled, auto_off, system_order
        zone_json = {
                "id": self.id,
                "Name": self.name,
                "GPIO": self.gpio,
                "Time": self.time,
                "Enabled": self.enabled,
                "Autooff": self.auto_off,
                "SystemOrder": self.system_order
                }
        req = self.session.put(f"{self.host}/{API.ZONE_UPDATE_URL}", json=zone_json)
        if req.status_code != 200:
            raise Exception(f"Zone did not update successfully ({req.status_code}). Payload: {zone_json}")

    async def async_update_other(self,other) -> None:
        url = f"{self.host}/{API.ZONE_UPDATE_URL}"
        payload = {
                "id": self.id,
                "Name": self.name,
                "GPIO": self.gpio,
                "Time": self.time,
                "Enabled": self.enabled,
                "Autooff": self.auto_off,
                "SystemOrder": self.system_order
                }
 
        async with aiohttp.ClientSession() as session:
            async with session.put(url,json=payload) as request:
                status = request.status
                if status != 200:
                     raise Exception(f"Zone did not update successfuly! HTTP status: {status}, Payload: {payload}")
 
