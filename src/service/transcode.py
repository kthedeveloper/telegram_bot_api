import av

def transcode_audio(input_file_path: str, output_file_path: str):
    with av.open(input_file_path) as file_in:
        in_stream = file_in.streams.audio[0]
        with av.open(output_file_path, 'w', format='wav') as file_out:
            out_stream = file_out.add_stream(
                'pcm_s16le', # Signed PCM 16bit
                rate=16000,
                layout='mono'
            )
            for frame in file_in.decode(in_stream):
                for packet in out_stream.encode(frame):
                    file_out.mux(packet)
            for packet in out_stream.encode():
                file_out.mux(packet)