import struct

FSB5_HEADER_SIZE = 0x3C
NAME_TABLE_SIZE = 0x20
SAMPLE_HEADER_SIZE = 0x20
TOTAL_SUBSONGS = 1
SAMPLE_RATE = 44100
CHANNELS = 2
LOOP_FLAG = 0
LOOP_START = 0
LOOP_END = 0
CODEC = 0x06
NAME_TABLE = b"MenAtWork"

def create_fsb5_header(sample_data_size):
    header = struct.pack('<4sI', b'FSB5', 0x01) 
    header += struct.pack('<I', TOTAL_SUBSONGS)
    header += struct.pack('<I', SAMPLE_HEADER_SIZE)
    header += struct.pack('<I', NAME_TABLE_SIZE)
    header += struct.pack('<I', sample_data_size)
    header += struct.pack('<I', CODEC)
    header += struct.pack('<I', 0)
    header += struct.pack('<I', 0)
    header += struct.pack('<I', 0)
    header += struct.pack('<I', 0)
    header += struct.pack('<I', 0)
    header += struct.pack('<I', 0)
    return header

def create_name_table():
    name_table = NAME_TABLE.ljust(NAME_TABLE_SIZE, b'\x00')
    return name_table

def create_stream_header(sample_data_size):
    stream_header = struct.pack('<Q', 0)
    stream_header += struct.pack('<I', sample_data_size)
    stream_header += struct.pack('<I', LOOP_START)
    stream_header += struct.pack('<I', LOOP_END)
    stream_header += struct.pack('<I', LOOP_FLAG)
    stream_header += struct.pack('<I', SAMPLE_RATE)
    stream_header += struct.pack('<I', CHANNELS)
    return stream_header

def create_fsb5_file(dsp_audio_data):
    sample_data_size = len(dsp_audio_data)
    fsb5_header = create_fsb5_header(sample_data_size)
    name_table = create_name_table()
    stream_header = create_stream_header(sample_data_size)

    with open('output.fsb5', 'wb') as fsb5_file:
        fsb5_file.write(fsb5_header) 
        fsb5_file.write(name_table) 
        fsb5_file.write(stream_header)
        fsb5_file.write(dsp_audio_data)

with open('menAtWorkDownUnder.dsp', 'rb') as f:
    dsp_audio_data = f.read()
    
if len(dsp_audio_data) != 0xA9C000:
    raise ValueError(f"Expected DSP audio data length of 0xA9C000, but got {len(dsp_audio_data):#x}")

create_fsb5_file(dsp_audio_data)
