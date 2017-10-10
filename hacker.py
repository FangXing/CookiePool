import time,os

class CaptchaHacker(object):

    #解析验证码，输入图片
    def resolve(self,img):
        raise NotImplementedError


class ManualCaptchaHacker(CaptchaHacker):

    def resolve(self,img):
        img_file_name = time.strftime('%Y%m%d%H%M%S', time.localtime())+'.jpg'
        currpath = os.getcwd()

        captcha_img_path = os.path.join(currpath,'yzm')
        if not os.path.exists(captcha_img_path):
            os.makedirs(captcha_img_path)

        with open(os.path.join(captcha_img_path,img_file_name),'wb') as f:
            f.write(img)
        code =  input('输入看到的验证码:文件名称：'+img_file_name)
        if code:
            return code
        return None


