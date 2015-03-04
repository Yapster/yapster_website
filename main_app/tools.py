import boto
import boto.rds
import boto.ec2.cloudwatch
from django.conf import settings
from pydub import AudioSegment
import json
import requests

def boto_init_s3(bucket_name):
    """
    Init boto s3 with credentials
    :param bucket_name: name of the bucket wanted
    :return: return the bucket obtain
    """
    c = boto.connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    b = c.get_bucket(bucket_name)

    return b

def to_cut(file, duration_slice=60000.0):
    try:
        mime = file.content_type.split("/")
    except IndexError:
        return False
    if mime[0] == "audio":
        file_version = AudioSegment.from_file(file, mime[1])
        nb = len(file_version) / duration_slice
        return nb
    return 0

def is_valid(file):
    """
    Check if the file uploaded is valid. Meaning sound file less than 30 min
    :param file:
    :return: True if valid. Else false (DUUH?!?!)
    """
    try:
        mime = file.content_type.split("/")
    except IndexError:
        return False
    if mime[0] == "audio":
        file_version = AudioSegment.from_file(file, mime[1])
        split_into_yaps(file_version)
        original_to_upload = file_version.export()
        upload_file_to_s3(original_to_upload, "1", "original." + mime[1], test=0)
        if mime == "audio":
            return True

    # name = 'E:/Projects/yapster_website/assets/1.mp3'
    #f = open(name, 'rb')
    return False


def split_into_yaps(audio_seg, duration_slice=60000.0):
    """
    Split a to big audio_seg into list of audio segs
    :param audio_seg : AudioSegment file to split
    :param duration_slice: Size of each part sliced, except last one obviously
    :return: list of AudioSegment
    """

    duration = len(audio_seg)
    rest = duration % duration_slice
    slice_number = duration // duration_slice - 1
    i = 0
    def get_interval(sub_audio, start, end):
        sub_audio = sub_audio[:end]
        if start != end:
            sub_audio = sub_audio[-start:]
        return sub_audio
    while slice_number >= i:
        new_file = get_interval(audio_seg, duration_slice, (i + 1) * duration_slice)
        to_upload = new_file.export("/" + str(i) + ".mp3")
        upload_file_to_s3(to_upload, "1", str(i) + ".mp3")
        i += 1
    if rest:
        new_file = audio_seg[-rest:]
        to_upload = new_file.export("/" + str(i) + ".mp3")
        upload_file_to_s3(to_upload, "1", str(i) + ".mp3")
    return


#TODO: Change Absolute path
def upload_file_to_s3(file, user_id, name, test=1):
    """
    Store the file, building path_bucket with file_type and user_id
    """
    b = boto_init_s3("yapster")
    if b:
        path_bucket = "yapsterusers/uid/" + user_id + "/yaps/1/audio/" + name
        k = b.get_key(path_bucket)
        if not k:
            try:
                k = b.new_key(path_bucket)
                k.set_contents_from_file(file)
            except:
                return "error occured"
    return ""


def yapster_api_post_request(path, params):
    headers = {'content-type': 'application/json'}
    if params == {}:
        return requests.get(path, headers=headers)
    return requests.post(path, data=json.dumps(params), headers=headers)


def get_profile_pix_path(path):
    c = boto.connect_s3(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    b = c.get_bucket('yapster')
    if b:
        try:
            s3_file_path = b.get_key(path)
            return s3_file_path.generate_url(expires_in=600)
        except:
            return ""
    return ""