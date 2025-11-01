import os

from comopy import HDLStage, IRStage, JobPipeline, RawModule, TranslatorStage


def translate_sv(top: RawModule) -> str:
    pipeline = JobPipeline(HDLStage(), IRStage(), TranslatorStage())
    pipeline(top)
    return top.translator.emit()


def write_sv(sv: str, filename: str):
    dir = os.path.dirname(__file__)
    path = f"{dir}/{filename}"
    with open(path, "w") as f:
        f.write(sv)
        f.write("\n")
