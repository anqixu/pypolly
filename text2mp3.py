#!/usr/bin/env python3
import argparse
import boto3
import pydub
import pydub.playback
import io

def text_to_mp3_stream(
    text='This is a test.',
    aws_region='us-east-1',
    polly_voice_id='Kimberly',
    mp3_sample_rate=22050):
  polly = boto3.client('polly', aws_region)
  response = polly.synthesize_speech(
    Text=text,
    OutputFormat='mp3',
    SampleRate=str(mp3_sample_rate),
    TextType='text',
    VoiceId=polly_voice_id)
  # For more voices, see: http://boto3.readthedocs.io/en/latest/reference/services/polly.html#Polly.Client.synthesize_speech
  # or http://docs.aws.amazon.com/polly/latest/dg/API_Voice.html

  stream = response["AudioStream"]
  mp3_bytes = stream.read()
  stream.close()
  return mp3_bytes

def save_mp3_stream(mp3_bytes, output_file):
  with(open(output_file, 'wb')) as f:
    f.write(mp3_bytes)

def play_mp3_stream(mp3_bytes):
  sound = pydub.AudioSegment.from_file(io.BytesIO(mp3_bytes), format="mp3")
  pydub.playback.play(sound)

'''
import contextlib # TODO: probably remove
if "AudioStream" in response:
    with contextlib.closing(response["AudioStream"]) as stream:
        data = stream.read()
        fo = open("pollytest.mp3", "wb+")
        fo.write(data)
        fo.close()

data = open('pollytest.mp3', 'rb').read()

song = pydub.AudioSegment.from_file(io.BytesIO(data), format="mp3")
pydub.playback.play(song)

stream = response["AudioStream"]
sound = pydub.AudioSegment.from_file(io.BytesIO(stream.read()), format="mp3")
pydub.playback.play(sound)
stream.close()
'''

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('text', help='Text to be spoken', type=str)
  parser.add_argument('--aws_region', help='AWS Region [us-east-1]', type=str, default='us-east-1')
  parser.add_argument('--polly_voice_id', help='AWS Polly Voice ID [Kimberly]', type=str, default='Kimberly')
  parser.add_argument('--mp3_sample_rate', help='MP3 Sample Rate [22050]', type=int, default=22050)
  return parser.parse_args()

def main():
  args = parse_args()
  mp3_stream = text_to_mp3_stream(text=args.text, aws_region=args.aws_region, polly_voice_id=args.polly_voice_id, mp3_sample_rate=args.mp3_sample_rate)
  play_mp3_stream(mp3_stream)
  save_mp3_stream(mp3_stream, 'polly_output.mp3')

main()
