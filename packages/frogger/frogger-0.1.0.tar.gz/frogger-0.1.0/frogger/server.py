import argparse
import json
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Union

from fastapi import FastAPI

# from frogger.config import load_config
from frogger.utils.manage import ModelManager
from frogger.utils.synthesizer import Synthesizer

app = FastAPI(title="Frogger", description="Frogger API", version="0.1.0")

def create_argparser():
    def convert_boolean(x):
        return x.lower() in ["true", "1", "yes"]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--list_models",
        type=convert_boolean,
        nargs="?",
        const=True,
        default=False,
        help="list available pre-trained tts and vocoder models.",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="tts_models/en/ljspeech/tacotron2-DDC",
        help="Name of one of the pre-trained tts models in format <language>/<dataset>/<model_name>",
    )
    parser.add_argument("--vocoder_name", type=str, default=None, help="name of one of the released vocoder models.")

    # Args for running custom models
    parser.add_argument("--config_path", default=None, type=str, help="Path to model config file.")
    parser.add_argument(
        "--model_path",
        type=str,
        default=None,
        help="Path to model file.",
    )
    parser.add_argument(
        "--vocoder_path",
        type=str,
        help="Path to vocoder model file. If it is not defined, model uses GL as vocoder. Please make sure that you installed vocoder library before (WaveRNN).",
        default=None,
    )
    parser.add_argument("--vocoder_config_path", type=str, help="Path to vocoder model config file.", default=None)
    parser.add_argument("--speakers_file_path", type=str, help="JSON file for multi-speaker model.", default=None)
    parser.add_argument("--port", type=int, default=5002, help="port to listen on.")
    parser.add_argument("--use_cuda", type=convert_boolean, default=False, help="true to use CUDA.")
    return parser


# parse the args
# args = create_argparser().parse_args()

# path = Path(__file__).parent / "../.models.json"
path = Path(__file__).parent / ".models.json"
manager = ModelManager(models_file=path)

# if args.list_models:
#     manager.list_models()
#     sys.exit()

logger = logging.getLogger("frogger")

# update in-use models to the specified released models.
model_path = None
config_path = None
speakers_file_path = None
vocoder_path = None
vocoder_config_path = None

# CASE1: list pre-trained TTS models
# if args.list_models:
#     manager.list_models()
#     sys.exit()

# # CASE2: load pre-trained model paths
# if args.model_name is not None and not args.model_path:
#     model_path, config_path, model_item = manager.download_model(args.model_name)
#     args.vocoder_name = model_item["default_vocoder"] if args.vocoder_name is None else args.vocoder_name
model_name = "tts_models/en/vctk/vits"
vocoder_name = None

if model_name is not None and not model_path:
    model_path, config_path, model_item = manager.download_model(model_name)
    vocoder_name = model_item["default_vocoder"] if vocoder_name is None else vocoder_name

if vocoder_name is not None and not vocoder_path:
    vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

if model_path is not None:
    model_path = model_path
    config_path = config_path
    speakers_file_path = speakers_file_path

# if args.vocoder_path is not None:
#     vocoder_path = args.vocoder_path
#     vocoder_config_path = args.vocoder_config_path

# load models
synthesizer = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    tts_speakers_file=speakers_file_path,
    tts_languages_file=None,
    vocoder_checkpoint=vocoder_path,
    vocoder_config=vocoder_config_path,
    encoder_checkpoint="",
    encoder_config="",
    # use_cuda=args.use_cuda,
    use_cuda=False,
)


def style_wav_uri_to_dict(style_wav: str) -> Union[str, dict]:
    """Transform an uri style_wav, in either a string (path to wav file to be use for style transfer)
    or a dict (gst tokens/values to be use for styling)

    Args:
        style_wav (str): uri

    Returns:
        Union[str, dict]: path to file (str) or gst style (dict)
    """
    if style_wav:
        if os.path.isfile(style_wav) and style_wav.endswith(".wav"):
            return style_wav  # style_wav is a .wav file located on the server

        style_wav = json.loads(style_wav)
        return style_wav  # style_wav is a gst dictionary with {token1_id : token1_weigth, ...}
    return None



@app.get("/tts")
async def tts_local(text: str | None = None, voice: str = "p243", language_idx: str = "", style_wav: str = ""):
    if text is None:
        return "No text provided", 400
    
    speaker_idx = voice
    style_wav = style_wav_uri_to_dict(style_wav)
    print(f" > Model input: {text}")
    print(f" > Speaker Idx: {speaker_idx}")
    print(f" > Language Idx: {language_idx}")
    wavs = synthesizer.tts(text, speaker_name=speaker_idx, language_name=language_idx, style_wav=style_wav)
    out = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    print(f" > Saving output to {out.name}")
    synthesizer.save_wav(wavs, out)
    return out.name


@app.get("/models", response_model=list[str])
async def get_models():
    return manager.list_models()

@app.get('/speakers', response_model=list[str])
async def get_speakers():
    return ["p243", "p245"]
