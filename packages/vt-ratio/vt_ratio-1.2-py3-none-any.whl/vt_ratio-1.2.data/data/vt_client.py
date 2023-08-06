import vt
from utils import calculate_sha256_hash
from vt_api_key.vt_api_key import vt_api_key


def vt_exists(filepath, client):
    try:
        new_file = open(filepath, 'rb').read()
        hash_new_file = calculate_sha256_hash(new_file)
        try:
            file = client.get_object(f"/files/{hash_new_file}")
            if file.get("last_analysis_stats"):
                return file.get("last_analysis_stats")
            else:
                return False
        except vt.error.APIError:
            return False
    except KeyboardInterrupt:
        raise


def vt_scan(filepath):
    try:
        client = vt.Client(str(vt_api_key))
        result = vt_exists(filepath, client)
        if result:
            client.close()
            return result
        else:
            with open(filepath, "rb") as f:
                analysis = client.scan_file(f, wait_for_completion=True)
                analysis_result = analysis.to_dict()
                client.close()
                return analysis_result['attributes']['stats']
    except KeyboardInterrupt:
        raise
