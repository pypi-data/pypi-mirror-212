import io
from PIL import Image

class NumberRecognitionService:
    get_number_link = None

    def get_number(self, photo):
        pass

class MailRecService(NumberRecognitionService):
    pass


class ImgCutter:
    size = None

    def cut_photo(self, photo):
        if not self.size:
            return photo
        img = Image.open(io.BytesIO(photo))
        # left, upper, right, lower
        # 2592*1944
        im_r = img.crop(self.size)
        im_r.show()
        img_byte_arr = io.BytesIO()
        im_r.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr