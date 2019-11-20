from django.contrib.auth import get_user_model
from post_office import mail
from friends import utils


User = get_user_model()


class Mailer:
    @staticmethod
    def new_follower(followee, follower):
        mail.send(
                followee.email,  # List of email addresses also accepted
                'students@propulsionacademy.com',
                template='new_follower_notify',
                context={'followee_name': followee.username,
                         'follower_name': follower.username},
                priority='medium',
        )

    @staticmethod
    def pending_friend_request(receiver, sender):
        mail.send(
                receiver.email,
                'students@propulsionacademy.com',
                subject='Friend Request',
                template='pending_friend_request_notify',
                context={'receiver_name': receiver.username,
                         'sender_name': sender.username},
                priority='medium'
            )

    @staticmethod
    def friend_request_accepted(receiver, sender):
        mail.send(
                sender.email,
                'students@propulsionacademy.com',
                template='accepted_friend_request_notify',
                context={'receiver_name': receiver.username,
                         'sender_name': sender.username},
                priority='medium'
            )

    @staticmethod
    def friend_post_notification(poster, friend):
        mail.send(
            friend.email,
            'students@propulsionacademy.com',
            template='friend_post_notify',
            context={'friend_name': friend.username,
                     'poster_name': poster.username},
            priority='medium'
        )

    @staticmethod
    def multi_friend_post_notification(posting_user):
        friend_user_ids = utils.get_all_friend_user_ids_from(posting_user)
        friend_users = User.objects.filter(id__in=friend_user_ids)

        for friend_user in friend_users:
            Mailer.friend_post_notification(posting_user, friend_user)

    @staticmethod
    def send_registration_validation_code(email, code):
        mail.send(
            email,
            'students@propulsionacademy.com',
            template='send_validation_code',
            context={'validation_code': code},
            priority='now'
        )

