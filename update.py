import collections
import json
import pathlib

import dandi.dandiapi

def update():
    file_path = pathlib.Path(__file__).parent / "blob_id_to_path.json"
    min_file_path = pathlib.Path(__file__).parent / "blob_id_to_path.min.json"
    blob_id_to_path: dict[str, dict[str, list[str]]] = collections.defaultdict(dict)

    client = dandi.dandiapi.DandiAPIClient()
    dandisets = list(client.get_dandisets())
    for dandiset in dandisets:
        dandiset_id = dandiset.identifier

        assets = dandiset.get_assets()
        for asset in assets:
            asset_path = pathlib.Path(asset.path)
            if ".nwb" not in asset_path.suffixes:
                continue

            blob_id = asset.zarr if ".zarr" in asset_path.suffixes else asset.blob
            if blob_id not in blob_id_to_path:
                blob_id_to_path[blob_id] = collections.defaultdict(list)

            blob_id_to_path[blob_id][dandiset_id].append(asset.path)

    with file_path.open(mode="w") as file_stream:
        json.dump(obj=blob_id_to_path, fp=file_stream, indent=2)
    with min_file_path.open(mode="w") as file_stream:
        json.dump(obj=blob_id_to_path, fp=file_stream)

if __name__ == "__main__":
    update()
