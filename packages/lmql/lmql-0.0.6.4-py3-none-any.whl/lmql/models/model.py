from lmql.models.lmtp.utils import rename_model_args

class LMQLModel:
    def __init__(self, model_identifier, model=None, **kwargs):
        self.model_identifier = model_identifier
        self.kwargs = kwargs

        # if this is a fixed reference to an existing model
        self.model = model

global inprocess_models
inprocess_models = {}

def inprocess(model_name, use_existing_configuration=False, **kwargs):
    """
    Loads a 'transformers' model in-process.

    This is useful when you don't want to spawn a separate 'lmql serve-model' process.

    The returned in-process models are cached so that subsequent calls with the same arguments will return the same object.

    Args:
        model_name (str): Name of the model to load, as it occurs in the HuggingFace Transformers registry. (e.g. gpt2)
        
        use_existing_configuration (bool): If True, will return an existing in-process model with the same model name, but possibly different arguments.
        
        kwargs: Additional arguments to pass to the serve-model command line. (see lmql serve-model --help)
                For this, use keys as they occur in the command line, e.g. 'port' for '--port' and for
                boolean flags, use True/False as values, e.g. 'cuda=True' for '--cuda'.
    Return:
        InProcessServer: An object representing the loaded model, can be passed in the 'from' clause of a query.
    """
    try:
        import transformers
        from .lmtp.lmtp_dcmodel import lmtp_model
    except ImportError:
        raise NotImplementedError("Your installation of LMQL does not support local models via inprocess(). Please make sure you have 'transformers' installed.")

    assert not model_name.startswith("openai/"), "openai/ models cannot be loaded with inprocess=True, they always use the remote API."

    # extract/reassign renamed like 'cuda'
    kwargs = rename_model_args(kwargs)

    if "endpoint" in kwargs:
        print("info: 'endpoint' argument is ignored for inprocess=True/local: models.")

    cmdline_args = f"{model_name} "
    for k,v in kwargs.items():
        if type(v) is bool:
            cmdline_args += f"--{k} "
        else:
            cmdline_args += f"--{k} {v} "

    if cmdline_args in inprocess_models:
        print("info: reusing existing in-process model.")
        model = inprocess_models[cmdline_args]
        return LMQLModel(model_name, model=model)
    
    if use_existing_configuration:
        # find existing match for model_name only
        for cmdargs, p in inprocess_models.items():
            if cmdargs.split(" ")[0] == model_name:
                return LMQLModel(model_name, model=p)
    
    model = lmtp_model(model_name, inprocess=True, **kwargs)
    inprocess_models[cmdline_args] = model
    return LMQLModel(model_name, model=model)

def model(model_identifier, **kwargs):
    # handle inprocess models
    is_inprocess = kwargs.pop("inprocess", False) or model_identifier.startswith("local:")
    if is_inprocess and model_identifier.startswith("local:"):
        model_identifier = model_identifier[6:]

    if is_inprocess:
        return inprocess(model_identifier, **kwargs)
    else:
        return LMQLModel(model_identifier, **kwargs)