import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    service = IOTService()

    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    devices = [hue_light, speaker, toilet]
    connect = [service.register_device(device) for device in devices]
    hue_id, speaker_id, toilet_id = await asyncio.gather(*connect)
    device_ids = [hue_id, speaker_id, toilet_id]

    wake_up_program = [
        Message(hue_id, MessageType.SWITCH_ON),
        Message(speaker_id, MessageType.SWITCH_ON),
        Message(toilet_id, MessageType.OPEN),

    ]

    parallel_action_program = [
        Message(hue_id, MessageType.CHANGE_COLOR),
        Message(
            speaker_id,
            MessageType.PLAY_SONG,
            "Rick Astley - Never Gonna Give You Up"
        ),
    ]

    sequence_action_program = [
        Message(toilet_id, MessageType.FLUSH),
        Message(toilet_id, MessageType.CLEAN),
    ]

    sleep_program = [
        Message(hue_id, MessageType.SWITCH_OFF),
        Message(speaker_id, MessageType.SWITCH_OFF),
        Message(toilet_id, MessageType.CLOSE),
    ]

    await service.run_parallel(wake_up_program)
    await service.run_parallel(parallel_action_program)
    await service.run_sequence(sequence_action_program)
    await service.run_parallel(sleep_program)

    disconnect = [service.unregister_device(device) for device in device_ids]
    await asyncio.gather(*disconnect)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
