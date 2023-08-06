# -*- coding: utf-8 -*-
import pathlib
import threading
import time
from ctypes import CDLL, POINTER, Structure, c_char_p, c_float, c_int32, c_void_p
from typing import Callable, List, Optional

library_path = pathlib.Path(__file__).parent.resolve() / "libggml-falcon.so"
clibrary = CDLL(str(library_path))


class falcon_hparams(Structure):
    """
    Hyperparameters of GPT-NeoX model in GGML backend.
    """

    _fields_ = [
        ("n_vocab", c_int32),
        ("n_ctx", c_int32),
        ("n_embd", c_int32),
        ("n_head", c_int32),
        ("n_layer", c_int32),
        ("n_rot", c_int32),
        ("par_res", c_int32),
        ("ftype", c_int32),
    ]


class falcon_model(Structure):
    """
    GPT-NeoX model in GGML backend.
    """

    _fields_ = [
        ("hparams", falcon_hparams),
        ("ln_f_g", c_void_p),
        ("ln_f_b", c_void_p),
        ("wte", c_void_p),
        ("lmh_g", c_void_p),
        ("layers", c_void_p),
        ("memory_k", c_void_p),
        ("memory_v", c_void_p),
        ("ctx", c_void_p),
        ("tensors", c_void_p),
    ]


def load_model(model_path: str):
    """
    Load the Falcon model from the given model path.

    Args:
        model_path (str): Path to the model file.

    Returns:
        POINTER(falcon_model): Pointer to the loaded model.
    """
    func = clibrary.load_model
    func.argtypes = [c_char_p]
    func.restype = POINTER(falcon_model)

    return func(model_path.encode("utf-8"))


def free_model(model):
    """
    Free the memory allocated for the Falcon model.

    Args:
        model (POINTER(falcon_model)): Pointer to the model.

    Returns:
        int: Status code indicating success (0) or failure.
    """

    func = clibrary.free_model
    func.argtypes = [POINTER(falcon_model)]
    func.restype = c_int32

    return func(model)


def generate(
    model,
    tokens: List[int],
    n_predict: int = 200,
    n_threads: int = 6,
    seed: int = -1,
    n_batch: int = 8,
    top_k: int = 40,
    top_p: float = 0.9,
    temp: float = 0.9,
    eos_token: int = 11,
    stream_callback: Optional[Callable[[List[int]], None]] = None,
):
    """
    Generate tokens using the Falcon model.

    Args:
        model(POINTER(falcon_model)): The Falcon model.
        tokens (List[int]): List of input tokens.
        n_predict (int): Number of tokens to predict. Defaults to 200.
        n_threads (int, optional): Number of threads to use for processing. Defaults to 6.
        seed (int, optional): The seed for the random number generator. Defaults to -1.
        n_batch (int, optional): Batch size for prompt processing. Defaults to 8.
        top_k (int, optional): Top-k sampling parameter. Defaults to 40.
        top_p (float, optional): Top-p sampling parameter. Defaults to 0.9.
        temp (float, optional): Temperature parameter. Defaults to 0.9.
        stream_callback (Optional[Callable[[List[int]], None]]): Optional callback function to receive generated tokens.

    Returns:
        List[int]: List of generated tokens.
    """
    func = clibrary.generate
    func.argtypes = [
        POINTER(falcon_model),  # model
        POINTER(c_int32),  # input tokens array
        c_int32,  # input tokens length
        POINTER(c_int32),  # output tokens array
        c_int32,  # n_predict
        c_int32,  # n_threads
        c_int32,  # seed
        c_int32,  # n_batch
        c_int32,  # top_k
        c_float,  # top_p
        c_float,  # temp
    ]

    # Convert input tokens to a C-compatible array
    input_tokens_len = len(tokens)
    input_tokens_arr = (c_int32 * input_tokens_len)()
    for i in range(input_tokens_len):
        input_tokens_arr[i] = tokens[i]

    # Create an array for output tokens and initialize with zeros
    # Add a last end_of_text token (0) at the end
    output_tokens_len = n_predict + 1
    output_tokens_arr = (c_int32 * (output_tokens_len))()
    for i in range(output_tokens_len):
        output_tokens_arr[i] = eos_token

    # Initialize thread_stop_event if stream_callback is provided
    thread_stop_event: Optional[threading.Event] = None
    if stream_callback:
        thread_stop_event = threading.Event()

        # Define a thread to handle streaming of generated tokens
        def stream_thread():
            len = 0
            while True:
                time.sleep(0.5)
                tokens = [output_tokens_arr[i] for i in range(output_tokens_len)]
                curr_len = tokens.index(eos_token)
                if curr_len > len:
                    stream_callback(tokens[len:curr_len])
                    len = curr_len

                if thread_stop_event.is_set():
                    break

        # Start the stream_thread
        threading.Thread(target=stream_thread).start()

    # Start tokens generation on GGML backend
    func(
        model,
        input_tokens_arr,
        input_tokens_len,
        output_tokens_arr,
        n_predict,
        n_threads,
        seed,
        n_batch,
        top_k,
        top_p,
        temp,
    )

    # Stop the stream_thread if it was started
    if thread_stop_event is not None:
        time.sleep(1)
        thread_stop_event.set()

    # Retrieve the generated tokens and return them
    output_tokens = [output_tokens_arr[i] for i in range(output_tokens_len)]
    return output_tokens[: output_tokens.index(eos_token) + 1]
