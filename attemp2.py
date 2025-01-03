import struct

# Constants for FSB5
FSB5_HEADER_SIZE = 0x3C  # Base header size for FSB5 version 0x01
NAME_TABLE_SIZE = 0x20    # Example size for name table
SAMPLE_HEADER_SIZE = 0x20  # Example size for sample header
TOTAL_SUBSONGS = 1          # Number of subsongs
SAMPLE_RATE = 44100         # Example sample rate
CHANNELS = 2                # Example number of channels
LOOP_FLAG = 0               # No loop
LOOP_START = 0              # Loop start sample
LOOP_END = 0                # Loop end sample
CODEC = 0x06                # PCM16 codec
NAME_TABLE = b"SampleName"  # Example name for the audio stream

def create_fsb5_header(sample_data_size):
    # Create FSB5 header
    header = struct.pack('<4sI', b'FSB5', 0x01)  # FSB5 ID and version
    header += struct.pack('<I', TOTAL_SUBSONGS)  # Total subsongs
    header += struct.pack('<I', SAMPLE_HEADER_SIZE)  # Sample header size
    header += struct.pack('<I', NAME_TABLE_SIZE)  # Name table size
    header += struct.pack('<I', sample_data_size)  # Sample data size
    header += struct.pack('<I', CODEC)  # Codec
    header += struct.pack('<I', 0)  # Reserved
    header += struct.pack('<I', 0)  # Reserved
    header += struct.pack('<I', 0)  # Reserved
    header += struct.pack('<I', 0)  # Reserved
    header += struct.pack('<I', 0)  # Reserved
    header += struct.pack('<I', 0)  # Reserved
    return header

def create_name_table():
    # Create name table with valid data
    name_table = NAME_TABLE.ljust(NAME_TABLE_SIZE, b'\x00')  # Fill with name
    return name_table

def create_stream_header(sample_data_size):
    # Create stream header
    stream_header = struct.pack('<Q', 0)  # Sample mode (to be calculated)
    stream_header += struct.pack('<I', sample_data_size)  # Sample data size
    stream_header += struct.pack('<I', LOOP_START)  # Loop start
    stream_header += struct.pack('<I', LOOP_END)  # Loop end
    stream_header += struct.pack('<I', LOOP_FLAG)  # Loop flag
    stream_header += struct.pack('<I', SAMPLE_RATE)  # Sample rate
    stream_header += struct.pack('<I', CHANNELS)  # Channels
    return stream_header

def create_fsb5_file(dsp_audio_data):
    # Calculate sample data size based on DSP audio data
    sample_data_size = len(dsp_audio_data)

    # Create FSB5 header
    fsb5_header = create_fsb5_header(sample_data_size)
    
    # Create name table
    name_table = create_name_table()
    
    # Create stream header
    stream_header = create_stream_header(sample_data_size)

    # Create FSB5 file
    with open('output.fsb5', 'wb') as fsb5_file:
        fsb5_file.write(fsb5_header)  # Write FSB5 header
        fsb5_file.write(name_table)    # Write name table
        fsb5_file.write(stream_header)  # Write stream header
        fsb5_file.write(dsp_audio_data) # Write DSP audio data

# Example DSP audio data (replace with your actual audio data)
# Assuming you have your DSP audio data in a variable named `dsp_audio_data`
# For example, if your data is in a binary file, you can read it like this:
with open('menAtWorkDownUnder.dsp', 'rb') as f:
    dsp_audio_data = f.read()  # Read your DSP audio data

# Ensure the length of the audio data is 0xA9C000
if len(dsp_audio_data) != 0xA9C000:
    raise ValueError(f"Expected DSP audio data length of 0xA9C000, but got {len(dsp_audio_data):#x}")

# Create FSB5 file from your DSP audio data
create_fsb5_file(dsp_audio_data)