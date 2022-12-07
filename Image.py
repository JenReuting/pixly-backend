import uuid


class Image():
    



    ########## helper functions ###############

    ALLOWED_EXTENSIONS={"jpg", "jpeg", "gif", "png"}

    def allowed_file(filename):
        return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

    def get_unique_key(filename):
        ext = filename.rsplit(".", 1)[1].lower()
        uuid_key = uuid.uuid4().hex
        return f"{uuid_key}.{ext}"
