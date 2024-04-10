import subprocess
import json
import sys
import os

def get_audio_tracks(input_file):
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', input_file]
    output = subprocess.check_output(cmd, universal_newlines=True)
    data = json.loads(output)
    audio_tracks = [stream['index'] for stream in data['streams'] if stream['codec_type'] == 'audio']
    return audio_tracks

def play_video(input_file, audio_tracks):
    if len(audio_tracks) >= 2:
        lavfi_complex = ' '.join([f"[aid{track+1}]" for track in range(len(audio_tracks))])
        lavfi_complex += f' amix=inputs={len(audio_tracks)} [ao]'
        cmd = f'mpv --lavfi-complex="{lavfi_complex}" "{input_file}"'
    elif len(audio_tracks) == 1:
        cmd = f'mpv "{input_file}"'
    else:
        cmd = f'mpv --no-audio "{input_file}"'

    # Print the command
    print(cmd)

    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = sys.argv[0]

    if not os.path.isfile(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)

    audio_tracks = get_audio_tracks(input_file)
    play_video(input_file, audio_tracks)
