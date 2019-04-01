import wx
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from JdSpider.jd_spider import jd_user_cookie
from TaobaoSpider.taobao_spider import taobao_user_cookie


class CreateFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(CreateFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        self.pnl = wx.Panel(self)

        # set the icon
        self.icon = wx.Icon('resource/icon/TEEX.jpg', wx.BITMAP_TYPE_JPEG)
        self.SetIcon(self.icon)

        # create button
        self.makeButton()

        # create status bar
        statusBar = self.CreateStatusBar()
        statusBar.SetFieldsCount(2)
        statusBar.SetStatusWidths([-5, -1])

    def makeButton(self):
        # add taobao button
        pic_tb = wx.Image('resource/icon/tb.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        btn_tb = wx.BitmapButton(self.pnl, -1, pic_tb, pos=(25, 25), size=(100, 100))
        wx.StaticText(self.pnl, -1, '淘宝', pos=(59, 130))  # The size of a Chinese character is 16px
        self.Bind(wx.EVT_BUTTON, self.OnClickTaobao, btn_tb)

        # add jingdong button
        pic_jd = wx.Image('img/icon/jd.bmp', wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        btn_jd = wx.BitmapButton(self.pnl, -1, pic_jd, pos=(150, 25), size=(100, 100))
        wx.StaticText(self.pnl, -1, '京东', pos=(184, 130))
        self.Bind(wx.EVT_BUTTON, self.OnClickJingdong, btn_jd)

    def Automation(self, url):
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(options=option)
        url = str(url)
        self.driver.maximize_window()
        self.driver.get(url)

    def getCookie(self, login):
        while True:
            try:
                if self.driver.get_log('driver')[0]['level'] == "WARNING":
                    self.SetStatusText("浏览器已关闭！", 1)
                    return 0
            except:
                pass
            time.sleep(1)
            try:
                # if not login -> exception
                self.driver.find_element_by_css_selector(login)
            except Exception as e:
                print(e)
            else:
                cookie_list = self.driver.get_cookies()
                self.driver.close()

                res = ''
                for cookie in cookie_list:
                    res += cookie.get('name') + '=' + cookie.get('value').replace('\"', '') + ';'
                print(res)
                return res

    def promptStart(self):
        self.SetStatusText("爬取中...", 1)

    def promptEnd(self):
        self.SetStatusText("爬取完成！", 1)

    def fail(self):
        self.SetStatusText("爬取失败！", 1)

    def OnClickTaobao(self, event):
        self.promptStart()
        url = 'https://world.taobao.com/markets/all/login'
        self.Automation(url)
        login_element = "[class='logout']"
        cookie = self.getCookie(login_element)
        if cookie:
            try:
                taobao_user_cookie(cookie)
            except:
                self.fail()
            else:
                self.promptEnd()

    def OnClickJingdong(self, event):
        self.promptStart()
        url = 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F'
        self.Automation(url)
        login_element = "[class='user_logout']"
        cookie = self.getCookie(login_element)
        if cookie:
            try:
                jd_user_cookie(cookie)
            except:
                self.fail()
            else:
                self.promptEnd()


if __name__ == '__main__':
    """When this module is run (not imported) then create the app, the
    frame, show it, and start the event loop."""
    app = wx.App()
    frm = CreateFrame(None, title='TEEX', size=(900, 600))
    frm.Show()
    app.MainLoop()
