from app_types import Context


def build_instaces_names(c: Context, prefix="App", suffix="", showId=True, separator=" "):
    """Build the names of the instances"""
    names = []
    for i in range(c["n_istances"]):
        if c["preset"]:
            if c["preset"]["instances"][i]["showId"]:
                names += [
                    f"{c['preset']['instances'][i]['prefix']}{separator}{i}{separator}{c['preset']['instances'][i]['suffix']}"
                ]
            else:
                names += [
                    f"{c['preset']['instances'][i]['prefix']}{separator}{c['preset']['instances'][i]['suffix']}"
                ]
        else:
            if showId:
                names += [f"{prefix}{separator}{i}{separator}{suffix}"]
            else:
                names += [f"{prefix}{separator}{suffix}"]
    return names
