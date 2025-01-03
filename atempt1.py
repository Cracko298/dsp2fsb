import struct
import os

DSP_HEADER_SIZE = 0x60  # 96 bytes

def parse_dsp_header(header_data):
    """Parse the DSP header into a structured dictionary."""
    if len(header_data) != DSP_HEADER_SIZE:
        raise ValueError(f"Invalid DSP header size: {len(header_data)} bytes. Expected {DSP_HEADER_SIZE} bytes.")

    # Correct 96-byte DSP header structure
    fields = struct.unpack(
        ">IIIIHHIIII16hHHHH5h10x",
        header_data
    )
    return {
        "sample_count": fields[0],
        "nibble_count": fields[1],
        "sample_rate": fields[2],
        "loop_flag": fields[3],
        "format": fields[4],
        "loop_start_offset": fields[5],
        "loop_end_offset": fields[6],
        "initial_offset": fields[7],
        "coef": fields[8:24],
        "gain": fields[24],
        "initial_ps": fields[25],
        "initial_hist1": fields[26],
        "initial_hist2": fields[27],
        "loop_ps": fields[28],
        "loop_hist1": fields[29],
        "loop_hist2": fields[30],
    }


def build_fsb5_header(dsp_header, sample_data_size):
    """Build the complete FSB5 header with main and stream headers."""
    # Main FSB5 Header (24 bytes)
    fsb5_magic = b"FSB5"
    version = 1  # FSB5 version
    total_sounds = 1  # Single sound
    sample_header_size = 0x10  # Size of one sample stream header
    name_table_size = 0  # No name table
    codec_id = 6  # DSP ADPCM codec
    flags = 0  # No special flags

    fsb5_header = struct.pack(
        "<4sIIIIII",
        fsb5_magic,
        version,
        total_sounds,
        sample_header_size,
        name_table_size,
        sample_data_size,
        codec_id,
    )

    # Subsound Stream Header (16 bytes)
    sample_count = dsp_header["sample_count"]
    sample_rate = dsp_header["sample_rate"]
    loop_flag = dsp_header["loop_flag"]

    subsound_header = struct.pack(
        "<Q",
        (sample_count << 34)  # Sample count (30 bits)
        | (0 << 7)  # Data offset (aligned to start of data)
        | (1 << 5)  # Channels (1 = mono, 2 = stereo, etc.)
        | (sample_rate << 1)  # Sample rate (30 bits)
        | (1 if loop_flag else 0),  # Loop flag (1 bit)
    )

    # Padding the stream header to 0x10 bytes
    subsound_header += struct.pack("<I", 0)  # Reserved (zero)

    return fsb5_header + subsound_header


def convert_dsp_to_fsb5(input_dsp, output_fsb5):
    """Convert DSP to FSB5 format."""
    with open(input_dsp, "rb") as dsp_file:
        dsp_header_data = dsp_file.read(DSP_HEADER_SIZE)  # DSP header (96 bytes)
        dsp_data = dsp_file.read()  # Remaining DSP data

    if len(dsp_header_data) != DSP_HEADER_SIZE:
        raise ValueError(f"Invalid DSP file: Header is {len(dsp_header_data)} bytes, expected {DSP_HEADER_SIZE} bytes.")

    dsp_header = parse_dsp_header(dsp_header_data)
    fsb5_header = build_fsb5_header(dsp_header, len(dsp_data))

    with open(output_fsb5, "wb") as fsb_file:
        fsb_file.write(fsb5_header)
        fsb_file.write(dsp_data)


# Main Execution
if __name__ == "__main__":
    input_dsp = "menAtWorkDownUnder.dsp"
    output_fsb5 = "menAtWorkDownUnder.fsb"  # Replace with desired output file name

    if not os.path.exists(input_dsp):
        print(f"Error: Input DSP file '{input_dsp}' not found.")
    else:
        try:
            convert_dsp_to_fsb5(input_dsp, output_fsb5)
            print(f"Converted '{input_dsp}' to '{output_fsb5}'.")
        except Exception as e:
            print(f"Error: {e}")
