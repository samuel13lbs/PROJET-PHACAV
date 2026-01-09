from matplotlib.colors import ListedColormap

def terrain_colormap():
    return ListedColormap([
        "#07284a",  # océan profond
        "#144a74",  # océan
        "#1e7f3f",  # plaines
        "#88a63a",  # collines
        "#c2b280",  # plateaux
        "#8b5a2b",  # montagnes
        "#ffffff"   # sommets
    ])