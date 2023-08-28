from win10toast import ToastNotifier


class Notification:

    def __init__(self, title, message, duration):
        self.__title_message = title
        self.__content = message
        self.__duration = duration
        self.__icon_img = None

    def sendNotification(self):
        new_notif = ToastNotifier()
        new_notif.show_toast(self.__title_message, self.__content, self.__icon_img, self.__duration)
