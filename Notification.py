from win10toast import ToastNotifier


class Notification:
    __title_message = ''
    __content = ''
    __duration = 3
    __icon_img = None

    # def __init__(self, title, message, icon, duration):
    #     self.__title_message = title
    #     self.__content = message
    #     self.__icon_img = icon
    #     self.__duration = duration

    def __init__(self, title, message, duration):
        self.__title_message = title
        self.__content = message
        self.__duration = duration

    # def __init__(self, title, message):
    #     self.__title_message = title
    #     self.__content = message

    def sendNotification(self):
        new_notif = ToastNotifier()
        new_notif.show_toast(self.__title_message, self.__content, self.__icon_img, self.__duration)
