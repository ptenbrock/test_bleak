#/usr/bin/env python3

import asyncio
from bleak import BleakScanner, BleakClient

#async def discover():
#    devices = await BleakScanner.discover()
#    for d in devices:
#        print(d)

dev = None
adv = None

def detection_callback(device, advertisement_data):
    global dev, adv
    if device.name == "Timeular Tracker":
        print(device.address, "RSSI:", device.rssi, advertisement_data)
        dev = device
        adv = advertisement_data
    # dev_list.append((device, advertisement_data))

async def discover():
    global scanner
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(5.0)
    await scanner.stop()

    for d in scanner.discovered_devices:
        print(d)

def active_side_indicator(char_handle, data):
    print(f"Active side: Handle '{char_handle}', data '{data}'")

def battery_indicator(char_handle, data):
    print(f"Battery: Handle '{char_handle}', data '{data}'")

async def connection(address):
    async with BleakClient(address) as client:
        print("Connected")
        # answer = await client.read_gatt_char(int("0x0013", 16))
        # answer1 = await client.read_gatt_char(12)
        # answer2 = await client.read_gatt_char(18)
        # answer = await client.read_gatt_char()
        # answer4 = await client.read_gatt_char()
        # indicate_req = bytes([0x20, 0x00])
        # answer5 = await client.write_gatt_descriptor("c7e70012-c847-11e6-8175-8c89a55d403c",
        #                                        indicate_req)
        services = await client.get_services()

        active_side_uuid = "c7e70012-c847-11e6-8175-8c89a55d403c"
        model_number_uuid = '00002a24-0000-1000-8000-00805f9b34fb'
        serial_number_uuid = '00002a25-0000-1000-8000-00805f9b34fb'
        firmware_revision_uuid = '00002a26-0000-1000-8000-00805f9b34fb'

        answer5 = await client.start_notify(active_side_uuid, active_side_indicator)
        # answer6 = await client.start_notify(active_side_uuid, battery_indicator)

        # active_side_char = services.get_characteristic(active_side_uuid)
        # active_side_descriptor = active_side_char.descriptors[0]

        answer1 = await client.read_gatt_char(firmware_revision_uuid)
        answer2 = await client.read_gatt_char(model_number_uuid)
        answer3 = await client.read_gatt_char(serial_number_uuid)

        # answer3 = await client.read_gatt_descriptor(active_side_descriptor.handle)
        answer4 = await client.read_gatt_char(active_side_uuid)
        # answer5 = await client.write_gatt_descriptor(active_side_descriptor.handle,
        #                                              indicate_req)

        await asyncio.sleep(5.0)

def main():
    asyncio.run(discover())
    # asyncio.run(connection(dev.address), debug = True)
    asyncio.run(connection("C2:0D:2F:B3:D8:FF"), debug = True)



if __name__ == "__main__":
    main()
    print("Hello, world!")

