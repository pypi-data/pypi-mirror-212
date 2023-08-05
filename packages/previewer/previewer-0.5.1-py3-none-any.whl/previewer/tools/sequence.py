from pathlib import Path
from typing import Iterable, Optional

from wand.image import Image

from ..logger import DEBUG


def create_sequence(
    frames: Iterable[Image],
    output_file: Path,
    delay: int = 50,
    gif_optimize: bool = True,
    aba_loop: Optional[str] = None,
):
    """
    Create a gif with the given images
    """
    with Image() as gif:
        queue = []
        for frame in frames:
            gif.sequence.append(frame)
            if aba_loop is not None:
                queue.append(frame.clone())
        if aba_loop is not None:
            # if A-B-A mode, add image in reverse order
            queue.reverse()
            if aba_loop == "aba" and len(queue) > 2:
                # skip first and last to prevent 2 identical consecutive frames
                queue.pop(0).destroy()
                queue.pop(-1).destroy()
            for frame in queue:
                gif.sequence.append(frame)
                # ba frames are reated
                frame.destroy()

        # Gif only optimisation
        if gif_optimize:
            gif.optimize_transparency()

        DEBUG("set gif delay to %d", delay)
        for frame in gif.sequence:
            frame.delay = delay
        gif.save(filename=output_file)
