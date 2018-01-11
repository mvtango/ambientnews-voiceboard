#! /usr/bin/env python

import os
from boto3 import Session
import sys
import logging
from fire import Fire

logger=logging.getLogger(__name__)


if "AWS_PROFILE" in os.environ :
    session = Session(profile_name=os.environ.get("AWS_PROFILE"))
elif "AWS_ACCESS_KEY_ID" in os.environ :
    session = Session(aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                      aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
                      region_name="eu-west-1")
    logger.debug("credentials: SECRET {}...{}, KEY {AWS_ACCESS_KEY_ID}".format(os.environ["AWS_SECRET_ACCESS_KEY"][0],os.environ["AWS_SECRET_ACCESS_KEY"][-1],**os.environ))
else :
    logger.error("Please set AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID or AWS_PROFILE to provide the server with credentials")
    sys.exit(1)


polly = session.client("polly")


def synthesize(voice="Vicki") :
    "STDIN: Text or SSML, STDOUT: mp3"

    param=dict(OutputFormat="mp3",VoiceId=voice)
    textbuffer=sys.stdin.read()
    if '<speak' in textbuffer :
        param["TextType"]="ssml"
    else :
        param["TextType"]="text"
    param["Text"]=textbuffer
    result=polly.synthesize_speech(**param)
    sys.stdout.buffer.write(result["AudioStream"].read())


if __name__=="__main__" :
    Fire(synthesize)



