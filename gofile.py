import requests

def upload_to_gofile(file_path):
    try:
        with open(file_path, "rb") as f:
            files = {'file': f}
            r = requests.post("https://upload.gofile.io/uploadfile", files=files)
        r.raise_for_status()
        data = r.json()
        if data.get("status") != "ok":
            raise Exception("Upload status not ok")
        return data["data"]["downloadPage"]
    except Exception as e:
        print(f"❌ Failed to upload to Gofile: {e}")
        return None
