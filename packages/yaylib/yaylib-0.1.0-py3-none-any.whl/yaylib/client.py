from typing import Union, Dict, List

from .api import API
from .api.call import *
from .api.cassandra import *
from .api.chat import *
from .api.group import *
from .api.login import *
from .api.misc import *
from .api.post import *
from .api.review import *
from .api.thread import *
from .api.user import *

from .config import *
from .errors import *
from .models import *
from .utils import *


class Client(API):
    """
    Client( \
        access_token=None, proxy=None, timeout=60, \
        base_path=current_path, loglevel_stream=logging.INFO, \
        host=Configs.YAY_PRODUCTION_HOST \
    )

    ---

    #### Yay! API v3 Client

    """

    # -CALL

    def bump_call(self, call_id: int, participant_limit: int = None):
        return bump_call(self, call_id, participant_limit)

    def get_user_active_call(self, user_id: int) -> Post:
        return get_user_active_call(self, user_id)

    def get_bgms(self) -> List[Bgm]:
        return get_bgms(self)

    def get_call(self, call_id: int) -> ConferenceCall:
        return get_call(self, call_id)

    def get_call_invitable_users(self, call_id: int, **params) -> UsersByTimestampResponse:
        # @Nullable @Query("user[nickname]")
        """

        Parameters:
        ---------------
            - from_timestamp: int - (optional)

        """
        return UsersByTimestampResponse(self, call_id, **params)

    def get_call_status(self, opponent_id: int) -> CallStatusResponse:
        return get_call_status(self, opponent_id)

    def get_games(self, **params) -> GamesResponse:
        """

        Parameters:
        ---------------
            - number: int - (optional)
            - ids: List[int] - (optional)
            - from_id: int - (optional)

        """
        return get_games(self, **params)

    def get_genres(self, **params) -> GenresResponse:
        """

        Parameters:
        ---------------
            - number: int - (optional)
            - from: int - (optional)

        """
        return get_genres(self, **params)

    def get_group_calls(self, **params) -> PostsResponse:
        return get_group_calls(self, **params)

    def invite_to_call_bulk(self, call_id: int, group_id: int = None):
        """

        Parameters:
        ---------------
            - call_id: int - (required)
            - group_id: int - (optional)

        """
        return invite_to_call_bulk(self, call_id, group_id)

    def invite_users_to_call(self, call_id: int, user_ids: List[int]):
        """

        Parameters:
        ---------------
            - call_id: int - (required)
            - user_ids: List[int] - (required)

        """
        return invite_users_to_call(self, call_id, user_ids)

    def invite_users_to_chat_call(
            self,
            chat_room_id: int,
            room_id: int,
            room_url: str
    ):
        return invite_users_to_chat_call(self, chat_room_id, room_id, room_url)

    def kick_and_ban_from_call(self, call_id: int, user_id: int):
        return kick_and_ban_from_call(self, call_id, user_id)

    def notify_anonymous_user_leave_agora_channel(
            self,
            conference_id: int,
            agora_uid: str
    ):
        return notify_anonymous_user_leave_agora_channel(
            self, conference_id, agora_uid
        )

    def notify_user_leave_agora_channel(self, conference_id: int, user_id: int):
        return notify_user_leave_agora_channel(self, conference_id, user_id)

    def send_call_screenshot(
            self,
            screenshot_filename: str,
            conference_id: int
    ):
        return send_call_screenshot(self, screenshot_filename, conference_id)

    def set_call(
            self,
            call_id: int,
            joinable_by: str,
            game_title: str = None,
            category_id: str = None
    ):
        return set_call(self, call_id, joinable_by, game_title, category_id)

    def set_user_role(
            self,
            call_id: int,
            user_id: int,
            role: str
    ):
        return set_user_role(self, call_id, user_id, role)

    def start_call(
            self,
            conference_id: int,
            call_sid: str
    ) -> ConferenceCall:
        return start_call(self, conference_id, call_sid)

    def stop_call(
            self,
            conference_id: int,
            call_sid: str
    ):
        return stop_call(self, conference_id, call_sid)

    # -CASSANDRA

    def get_user_activities(self, **params) -> ActivitiesResponse:
        """

        Parameters:
        ---------------
            - important: bool - (required)
            - from_timestamp: int - (optional)
            - number: int - (optional)

        """
        return get_user_activities(self, **params)

    def get_user_merged_activities(self, from_timestamp: int = None) -> ActivitiesResponse:
        return get_user_merged_activities(self, from_timestamp)

    def received_notification(self, pid: str, type: str, opened_at: int = None):
        return received_notification(self, pid, type, opened_at)

    # -CHAT

    def accept_request(self, chat_room_ids: List[int]):
        return accept_request(self, chat_room_ids)

    def check_unread_status(self, from_time: int) -> UnreadStatusResponse:
        return check_unread_status(self, from_time)

    def create_group_chat(
            self,
            name: str,
            with_user_ids: List[int],
            icon_filename: str = None,
            background_filename: str = None
    ) -> CreateChatRoomResponse:
        return create_group_chat(
            self,
            name,
            with_user_ids,
            icon_filename,
            background_filename
        )

    def create_private_chat(
            self,
            with_user_id: int,
            matching_id: int = None,
            hima_chat: bool = False
    ) -> CreateChatRoomResponse:
        return create_private_chat(
            self,
            with_user_id,
            matching_id,
            hima_chat
        )

    def delete_background(self, room_id: int):
        return delete_background(self, room_id)

    def delete_message(self, room_id: int, message_id: int):
        return delete_message(self, room_id, message_id)

    def edit_chat_room(
            self,
            chat_room_id: int,
            name: str,
            icon_filename: str = None,
            background_filename: str = None
    ):
        return edit_chat_room(
            self,
            chat_room_id,
            name,
            icon_filename,
            background_filename
        )

    def get_chatable_users(
            self,
            from_follow_id: int = None,
            from_timestamp: int = None,
            order_by: str = None
    ) -> FollowUsersResponse:
        return get_chatable_users(from_follow_id, from_timestamp, order_by)

    def get_gifs_data(self) -> List[GifImageCategory]:
        return get_gifs_data(self)

    def get_hidden_chat_rooms(self, **params) -> ChatRoomsResponse:
        """

        Parameters:
        ---------------

            - from_timestamp: int - (optional)
            - number: int - (optional)

        """
        return get_hidden_chat_rooms(self, **params)

    def get_main_chat_rooms(self, from_timestamp: int = None) -> ChatRoomsResponse:
        return get_main_chat_rooms(self, from_timestamp)

    def get_messages(self, chat_room_id: int, **params) -> List[Message]:
        """

        Parameters:
        ---------------
            - from_message_id: int - (optional)
            - to_message_id: int - (optional)

        """
        return get_messages(self, chat_room_id, **params)

    # def get_notification_settings(self, chat_room_id: int) -> Settings:
    #     return get_notification_settings(self, chat_room_id)

    def get_request_chat_rooms(self, from_timestamp: int = None) -> ChatRoomsResponse:
        return get_request_chat_rooms(self, from_timestamp)

    def get_chat_room(self, chat_room_id: int) -> ChatRoom:
        return get_chat_room(self, chat_room_id)

    def get_sticker_packs(self) -> List[StickerPack]:
        return get_sticker_packs(self)

    def get_total_chat_requests(self) -> int:
        return get_total_chat_requests(self)

    def hide_chat(self, chat_room_id: int):
        return hide_chat(self, chat_room_id)

    def invite_to_chat(self, chat_room_id: int, user_ids: List[int]):
        return invite_to_chat(self, chat_room_id, user_ids)

    def kick_users_from_chat(self, chat_room_id: int, user_ids: List[int]):
        return kick_users_from_chat(self, chat_room_id, user_ids)

    def pin_chat(self, room_id: int):
        return pin_chat(self, room_id)

    def read_attachment(
            self,
            room_id: int,
            attachment_msg_ids: List[int]
    ):
        # TODO: check if this works
        return read_attachment(self, room_id, attachment_msg_ids)

    def read_message(self, chat_room_id: int, message_id: int):
        return read_message(self, chat_room_id, message_id)

    def read_video_message(
            self,
            room_id: int,
            video_msg_ids: List[int]
    ):
        return read_video_message(self, room_id, video_msg_ids)

    def refresh_chat_rooms(self, from_time: int = None) -> ChatRoomsResponse:
        return refresh_chat_rooms(self, from_time)

    def remove_chat_rooms(self, chat_room_ids: List[int]):
        return remove_chat_rooms(self, chat_room_ids)

    def report_chat_room(
        self,
        chat_room_id: int,
        opponent_id: int,
        category_id: int,
        reason: str = None,
        screenshot_filename: str = None,
        screenshot_2_filename: str = None,
        screenshot_3_filename: str = None,
        screenshot_4_filename: str = None
    ):
        return report_chat_room(
            self,
            chat_room_id,
            opponent_id,
            category_id,
            reason,
            screenshot_filename,
            screenshot_2_filename,
            screenshot_3_filename,
            screenshot_4_filename
        )

    def send_media_screenshot_notification(self, room_id: int):
        return send_media_screenshot_notification(self, room_id)

    def send_message(
            self,
            chat_room_id: int,
            message_type: str,
            call_type: str = None,
            text: str = None,
            font_size: int = None,
            gif_image_id: int = None,
            attachment_file_name: str = None,
            sticker_pack_id: int = None,
            video_file_name: str = None
    ) -> MessageResponse:
        return send_message(
            self,
            chat_room_id,
            message_type,
            call_type,
            text,
            font_size,
            gif_image_id,
            attachment_file_name,
            sticker_pack_id,
            video_file_name
        )

    # def set_notification_settings(
    #     self,
    #     chat_room_id: int,
    #     notification_chat: int
    # ) -> Settings:
    #     return set_notification_settings(self)

    def unhide_chat(self, chat_room_ids: int):
        return unhide_chat(self, chat_room_ids)

    def unpin_chat(self, chat_room_id: int):
        return unpin_chat(self, chat_room_id)

    # -GROUP

    def accept_moderator_offer(self, group_id: int):
        return accept_moderator_offer(self, group_id)

    def accept_ownership_offer(self, group_id: int):
        return accept_ownership_offer(self, group_id)

    def accept_group_join_request(self, group_id: int, user_id: int):
        return accept_group_join_request(self, group_id, user_id)

    def add_related_groups(self, group_id: int, related_group_id: List[int]):
        return add_related_groups(self, group_id, related_group_id)

    def ban_group_user(self, group_id: int, user_id: int):
        return ban_group_user(self, group_id, user_id)

    def check_unread_status(self, from_time: int = None) -> UnreadStatusResponse:
        return check_unread_status(self, from_time)

    def create_group(
            self,
            topic: str,
            description: str = None,
            secret: bool = None,
            hide_reported_posts: bool = None,
            hide_conference_call: bool = None,
            is_private: bool = None,
            only_verified_age: bool = None,
            only_mobile_verified: bool = None,
            call_timeline_display: bool = None,
            allow_ownership_transfer: bool = None,
            allow_thread_creation_by: str = None,
            gender: int = None,
            generation_groups_limit: int = None,
            group_category_id: int = None,
            cover_image_filename: str = None,
            sub_category_id: str = None,
            hide_from_game_eight: bool = None,
            allow_members_to_post_media: bool = None,
            allow_members_to_post_url: bool = None,
            guidelines: str = None,
    ) -> CreateGroupResponse:
        return create_group(
            self,
            topic,
            description,
            secret,
            hide_reported_posts,
            hide_conference_call,
            is_private,
            only_verified_age,
            only_mobile_verified,
            call_timeline_display,
            allow_ownership_transfer,
            allow_thread_creation_by,
            gender, generation_groups_limit,
            group_category_id,
            cover_image_filename,
            sub_category_id,
            hide_from_game_eight,
            allow_members_to_post_media,
            allow_members_to_post_url,
            guidelines
        )

    def create_pin_group(self, group_id: int):
        return create_pin_group(self, group_id)

    def decline_moderator_offer(self, group_id: int):
        return decline_moderator_offer(self, group_id)

    def decline_ownership_offer(self, group_id: int):
        return decline_ownership_offer(self, group_id)

    def decline_group_join_request(self, group_id: int, user_id: int):
        return decline_ownership_offer(self, group_id, user_id)

    def delete_pin_group(self, group_id: int):
        return delete_pin_group(self, group_id)

    def get_banned_group_members(self, group_id: int, page: int = None) -> UsersResponse:
        return get_banned_group_members(self, group_id, page)

    def get_group_categories(self, **params) -> GroupCategoriesResponse:
        """

        Parameters:
        ----------

            - page: int - (optional)
            - number: int - (optional)

        """
        return get_group_categories(self, **params)

    def get_create_group_quota(self) -> CreateGroupQuota:
        return get_create_group_quota(self)

    def get_group(self, group_id: int) -> GroupResponse:
        return get_group(self, group_id)

    # def get_group_notification_settings(self, group_id: int) -> GroupNotificationSettingsResponse:
    #     return get_group_notification_settings(self, group_id)

    def get_groups(self, **params) -> GroupsResponse:
        """

        Parameters:
        ----------

            - group_category_id: int = None
            - keyword: str = None
            - from_timestamp: int = None
            - sub_category_id: int = None

        """
        return get_groups(self, **params)

    def get_invitable_users(self, group_id: int, **params) -> UsersByTimestampResponse:
        """

        Parameters:
        ----------

            - from_timestamp: int - (optional)
            - user[nickname]: str - (optional)

        """
        return get_invitable_users(self, group_id, **params)

    def get_joined_statuses(self, ids: List[int]) -> dict:
        return get_joined_statuses(self, ids)

    def get_group_member(self, group_id: int, user_id: int) -> GroupUserResponse:
        return get_group_member(self, group_id, user_id)

    def get_group_members(self, group_id: int, **params) -> GroupUsersResponse:
        """

        Parameters:
        ----------

            - id: int - (required)
            - mode: str - (optional)
            - keyword: str - (optional)
            - from_id: int - (optional)
            - from_timestamp: int - (optional)
            - order_by: str - (optional)
            - followed_by_me: bool - (optional)

        """
        return get_group_members(self, group_id, **params)

    def get_my_groups(self, from_timestamp: None) -> GroupsResponse:
        return get_my_groups(self, from_timestamp)

    def get_relatable_groups(self, group_id: int, **params) -> GroupsRelatedResponse:
        """

        Parameters:
        ----------

            - group_id: int - (required)
            - keyword: str - (optional)
            - from: str - (optional)

        """
        return get_relatable_groups(self, group_id, **params)

    def get_related_groups(self, group_id: int, **params) -> GroupsRelatedResponse:
        """

        Parameters:
        ----------

            - group_id: int - (required)
            - keyword: str - (optional)
            - from: str - (optional)

        """
        return get_related_groups(self, group_id, **params)

    def get_user_groups(self, **params) -> GroupsResponse:
        """

        Parameters:
        ----------

            - user_id: int - (required)
            - page: int - (optional)

        """
        return get_user_groups(self, **params)

    def invite_users_to_group(self, group_id: int, user_ids: List[int]):
        return invite_users_to_group(self, group_id, user_ids)

    def join_group(self, group_id: int):
        return join_group(self, group_id)

    def leave_group(self, group_id: int):
        return leave_group(self, group_id)

    def post_gruop_social_shared(self, group_id: int, sns_name: str):
        return post_gruop_social_shared(self, group_id, sns_name)

    def remove_group_cover(self, group_id: int):
        return remove_group_cover(self, group_id)

    def remove_moderator(self, group_id: int, user_id: int):
        return remove_moderator(self, group_id, user_id)

    def remove_related_groups(self, group_id: int, related_group_ids: List[int]):
        return remove_related_groups(self, group_id, related_group_ids)

    def report_group(
            self,
            group_id: int,
            category_id: int,
            reason: str = None,
            opponent_id: int = None,
            screenshot_filename: str = None,
            screenshot_2_filename: str = None,
            screenshot_3_filename: str = None,
            screenshot_4_filename: str = None,
    ):
        return report_group(
            self,
            group_id,
            category_id,
            reason,
            opponent_id,
            screenshot_filename,
            screenshot_2_filename,
            screenshot_3_filename,
            screenshot_4_filename
        )

    def send_moderator_offers(self, group_id: int, user_ids: List[int]):
        return send_moderator_offers(self, group_id, user_ids)

    def send_ownership_offer(self, group_id: int, user_id: int):
        return send_ownership_offer(self, group_id, user_id)

    # def set_group_notification_settings(
    #         self,
    #         group_id: int,
    #         notification_group_post: int = None,
    #         notification_group_join: int = None,
    #         notification_group_request: int = None,
    #         notification_group_message_tag_all: int = None,
    # ) -> AdditionalSettingsResponse:
    #     return set_group_notification_settings(self)

    def set_group_title(self, group_id: int, title: str):
        return set_group_title(self, group_id, title)

    def take_over_group_ownership(self, group_id: int):
        return take_over_group_ownership(self, group_id)

    def unban_group_member(self, group_id: int, user_id: int):
        return unban_group_member(self, group_id, user_id)

    def update_group(
            self,
            group_id: int,
            topic: str,
            description: str = None,
            secret: bool = None,
            hide_reported_posts: bool = None,
            hide_conference_call: bool = None,
            is_private: bool = None,
            only_verified_age: bool = None,
            only_mobile_verified: bool = None,
            call_timeline_display: bool = None,
            allow_ownership_transfer: bool = None,
            allow_thread_creation_by: str = None,
            gender: int = None,
            generation_groups_limit: int = None,
            group_category_id: int = None,
            cover_image_filename: str = None,
            sub_category_id: str = None,
            hide_from_game_eight: bool = None,
            allow_members_to_post_media: bool = None,
            allow_members_to_post_url: bool = None,
            guidelines: str = None,
    ) -> GroupResponse:
        return update_group(
            group_id,
            topic,
            description,
            secret,
            hide_reported_posts,
            hide_conference_call,
            is_private,
            only_verified_age,
            only_mobile_verified,
            call_timeline_display,
            allow_ownership_transfer,
            allow_thread_creation_by,
            gender,
            generation_groups_limit,
            group_category_id,
            cover_image_filename,
            sub_category_id,
            hide_from_game_eight,
            allow_members_to_post_media,
            allow_members_to_post_url,
            guidelines,
        )

    def visit_group(self, group_id: int):
        return visit_group(self, group_id)

    def withdraw_moderator_offer(self, group_id: int, user_id: int):
        return withdraw_moderator_offer(self, group_id, user_id)

    def withdraw_ownership_offer(self, group_id: int, user_id: int):
        return withdraw_ownership_offer(self, group_id, user_id)

    # -LOGIN

    def change_email(
            self,
            email: str,
            password: str,
            email_grant_token: str = None
    ) -> LoginUpdateResponse:
        return change_email(self, email, password, email_grant_token)

    def change_password(
            self,
            current_password: str,
            new_password: str
    ) -> LoginUpdateResponse:
        return change_password(self, current_password, new_password)

    # def connect_account_with_sns(self):
    #     return connect_account_with_sns(self)

    # def disconnect_account_with_sns(self):
    #     return disconnect_account_with_sns(self)

    def get_token(
            self,
            grant_type: str,
            refresh_token: str = None,
            email: str = None,
            password: str = None
    ) -> TokenResponse:
        return get_token(
            self,
            grant_type,
            refresh_token,
            email,
            password
        )

    def login_with_email(self, email: str, password: str) -> LoginUserResponse:
        return login_with_email(self, email, password)

    # def login_with_sns(self):
    #     return login_with_sns(self)

    def logout(self):
        return logout(self)

    # def migrate_token(self):
    #     return migrate_token(self)

    # def register_device_token(self):
    #     return register_device_token(self)

    def resend_confirm_email(self):
        return resend_confirm_email(self)

    def restore_user(self, user_id: int) -> LoginUserResponse:
        return restore_user(self, user_id)

    def revoke_tokens(self):
        return revoke_tokens(self)

    def save_account_with_email(
            self,
            email: str,
            password: str = None,
            current_password: str = None,
            email_grant_token: str = None
    ) -> LoginUpdateResponse:
        return save_account_with_email(
            self,
            email,
            password,
            current_password,
            email_grant_token,
        )

    # -MISC

    def accept_policy_agreement(self, type: str):
        return accept_policy_agreement(self, type)

    def generate_sns_thumbnail(self, **params):
        """

        Parameters:
        ----------

            - resource_type: str - (Required)
            - resource_id: int - (Required)

        """
        return generate_sns_thumbnail(self, **params)

    def get_email_verification_presigned_url(self, email: str, locale: str, intent: str = None) -> str:
        return get_email_verification_presigned_url(self, email, locale, intent)

    def get_file_upload_presigned_urls(self, file_names: List[str]) -> List[PresignedUrl]:
        return get_file_upload_presigned_urls(self, file_names)

    # def get_id_checker_presigned_url(
    #         self,
    #         model: str,
    #         action: str,
    #         **params
    # ) -> str:
    #     return get_id_checker_presigned_url(self, model, action, **params)

    def get_old_file_upload_presigned_url(self, video_file_name: str) -> str:
        return get_old_file_upload_presigned_url(self, video_file_name)

    def get_policy_agreements(self) -> PolicyAgreementsResponse:
        return get_policy_agreements(self)

    def get_promotions(self, **params) -> List[Promotion]:
        """

        Parameters:
        ----------

            - page: int - (Optional)
            - number: int - (Optional)

        """
        return get_promotions(self, **params)

    def get_vip_game_reward_url(self, device_type: str) -> str:
        return get_vip_game_reward_url(self, device_type)

    def get_web_socket_token(self) -> str:
        return get_web_socket_token(self)

    def verify_device(
            self,
            app_version: str,
            device_uuid: str,
            platform: str,
            verification_string: str
    ) -> VerifyDeviceResponse:
        # TODO: check platform, verification_string
        return verify_device(
            self,
            app_version,
            device_uuid,
            platform,
            verification_string
        )

    # -POST

    def add_bookmark(self, user_id: int, post_id: int) -> BookmarkPostResponse:
        return add_bookmark(self, user_id, post_id)

    def add_group_highlight_post(self, group_id: int, post_id: int):
        return add_group_highlight_post(self, group_id, post_id)

    def create_call_post(
            self,
            text: str = None,
            font_size: int = None,
            color: int = None,
            group_id: int = None,
            call_type: str = None,
            category_id: int = None,
            game_title: str = None,
            joinable_by: str = None,
            message_tags: str = "[]",
            attachment_filename: str = None,
            attachment_2_filename: str = None,
            attachment_3_filename: str = None,
            attachment_4_filename: str = None,
            attachment_5_filename: str = None,
            attachment_6_filename: str = None,
            attachment_7_filename: str = None,
            attachment_8_filename: str = None,
            attachment_9_filename: str = None,
    ) -> ConferenceCall:
        return create_call_post(
            self,
            text,
            font_size,
            color,
            group_id,
            call_type,
            category_id,
            game_title,
            joinable_by,
            message_tags,
            attachment_filename,
            attachment_2_filename,
            attachment_3_filename,
            attachment_4_filename,
            attachment_5_filename,
            attachment_6_filename,
            attachment_7_filename,
            attachment_8_filename,
            attachment_9_filename
        )

    def create_group_pin_post(self, post_id: int, group_id: int):
        return create_group_pin_post(self, post_id, group_id)

    def create_pin_post(self, post_id: int):
        return create_pin_post(self, post_id)

    def mention(self, user_id: int) -> str:
        return mention(self, user_id)

    def create_post(
            self,
            text: str = None,
            font_size: int = 0,
            color: int = 0,
            in_reply_to: int = None,
            group_id: int = None,
            post_type: str = None,
            mention_ids: List[int] = None,
            choices: List[str] = None,
            shared_url: Dict[str, str | int] = None,
            message_tags: str = "[]",
            attachment_filename: str = None,
            attachment_2_filename: str = None,
            attachment_3_filename: str = None,
            attachment_4_filename: str = None,
            attachment_5_filename: str = None,
            attachment_6_filename: str = None,
            attachment_7_filename: str = None,
            attachment_8_filename: str = None,
            attachment_9_filename: str = None,
            video_file_name: str = None,
    ) -> Post:
        return create_post(
            self,
            text,
            font_size,
            color,
            in_reply_to,
            group_id,
            post_type,
            mention_ids,
            choices,
            shared_url,
            message_tags,
            attachment_filename,
            attachment_2_filename,
            attachment_3_filename,
            attachment_4_filename,
            attachment_5_filename,
            attachment_6_filename,
            attachment_7_filename,
            attachment_8_filename,
            attachment_9_filename,
            video_file_name
        )

    def create_repost(
            self,
            post_id: int,
            text: str = None,
            font_size: int = None,
            color: int = None,
            in_reply_to: int = None,
            group_id: int = None,
            post_type: str = None,
            mention_ids: List[int] = None,
            choices: List[str] = None,
            shared_url: Dict[str, Union[str, int]] = None,
            message_tags: str = "[]",
            attachment_filename: str = None,
            attachment_2_filename: str = None,
            attachment_3_filename: str = None,
            attachment_4_filename: str = None,
            attachment_5_filename: str = None,
            attachment_6_filename: str = None,
            attachment_7_filename: str = None,
            attachment_8_filename: str = None,
            attachment_9_filename: str = None,
            video_file_name: str = None,
    ) -> Post:
        return create_repost(
            self,
            post_id,
            text,
            font_size,
            color,
            in_reply_to,
            group_id,
            post_type,
            mention_ids,
            choices,
            shared_url,
            message_tags,
            attachment_filename,
            attachment_2_filename,
            attachment_3_filename,
            attachment_4_filename,
            attachment_5_filename,
            attachment_6_filename,
            attachment_7_filename,
            attachment_8_filename,
            attachment_9_filename,
            video_file_name,
        )

    def create_share_post(
            self,
            shareable_type: str,
            shareable_id: int,
            text: str = None,
            font_size: int = None,
            color: int = None,
            group_id: int = None,
    ) -> Post:
        return create_share_post(
            self,
            shareable_type,
            shareable_id,
            text,
            font_size,
            color,
            group_id
        )

    def create_thread_post(
            self,
            post_id: int,
            text: str = None,
            font_size: int = None,
            color: int = None,
            in_reply_to: int = None,
            group_id: int = None,
            post_type: str = None,
            mention_ids: List[int] = None,
            choices: List[str] = None,
            shared_url: Dict[str, Union[str, int]] = None,
            message_tags: str = "[]",
            attachment_filename: str = None,
            attachment_2_filename: str = None,
            attachment_3_filename: str = None,
            attachment_4_filename: str = None,
            attachment_5_filename: str = None,
            attachment_6_filename: str = None,
            attachment_7_filename: str = None,
            attachment_8_filename: str = None,
            attachment_9_filename: str = None,
            video_file_name: str = None,
    ) -> Post:
        return create_thread_post(
            self,
            post_id,
            text,
            font_size,
            color,
            in_reply_to,
            group_id,
            post_type,
            mention_ids,
            choices,
            shared_url,
            message_tags,
            attachment_filename,
            attachment_2_filename,
            attachment_3_filename,
            attachment_4_filename,
            attachment_5_filename,
            attachment_6_filename,
            attachment_7_filename,
            attachment_8_filename,
            attachment_9_filename,
            video_file_name,
        )

    def delete_all_post(self):
        return delete_all_post(self)

    def delete_group_pin_post(self, group_id: int):
        return delete_group_pin_post(self, group_id)

    def delete_pin_post(self, post_id: int):
        return delete_pin_post(self, post_id)

    def get_bookmark(self, user_id: int, *, from_str: str = None) -> PostsResponse:
        return get_bookmark(self, user_id, from_str)

    def get_timeline_calls(self, **params) -> PostsResponse:
        """

        Parameters:
        ----------

            - group_id: int = None
            - from_timestamp: int = None
            - number: int = None
            - category_id: int = None
            - call_type: str = "voice"
            - include_circle_call: bool = None
            - cross_generation: bool = None
            - exclude_recent_gomimushi: bool = None
            - shared_interest_categories: bool = None

        """
        return get_timeline_calls(self, **params)

    def get_conversation(self, conversation_id: int, **params) -> PostsResponse:
        """

        Parameters:
        ----------

            - conversation_id: int
            - group_id: int = None
            - thread_id: int = None
            - from_post_id: int = None
            - number: int = 50
            - reverse: bool = True

        """
        return get_conversation(self, conversation_id, **params)

    def get_conversation_root_posts(self, post_ids: List[int]) -> PostsResponse:
        return get_conversation_root_posts(self, post_ids)

    def get_following_call_timeline(self, **params) -> PostsResponse:
        """

        Parameters:
        ----------

            - from_timestamp: int = None
            - number: int = None
            - category_id: int = None
            - call_type: str = None
            - include_circle_call: bool = None
            - exclude_recent_gomimushi: bool = None

        """
        return get_following_call_timeline(self, **params)

    def get_following_timeline(self, **params) -> PostsResponse:
        """

        Parameters:
        ----------

            - from_str: str = None
            - only_root: bool = None
            - order_by: str = None
            - number: int = None
            - mxn: int = None
            - reduce_selfie: bool = None
            - custom_generation_range: bool = None

        """
        return get_following_timeline(self, **params)

    def get_group_highlight_posts(self, group_id: int, **params) -> PostsResponse:
        """

        Parameters:
        ----------

            - group_id: int
            - from_post: int = None
            - number: int = None

        """
        return get_group_highlight_posts(self, group_id, **params)

    def get_group_timeline_by_keyword(self, group_id: int, keyword: str, **params) -> PostsResponse:
        """

        Parameters:
        ----------

            - group_id: int
            - keyword: str
            - from_post_id: int = None
            - number: int = None
            - only_thread_posts: bool = False

        """
        return get_group_timeline_by_keyword(self, group_id, keyword, **params)

    def get_group_timeline(self, group_id: int, **params) -> PostsResponse:
        """

        Parameters:
        ----------

            - group_id: int
            - from_post_id: int
            - reverse: bool
            - post_type: str
            - number: int
            - only_root: bool

        """
        return get_group_timeline(self, group_id, **params)

    def get_timeline_by_hashtag(self, hashtag: str, **params) -> PostsResponse:
        """

        Parameters:
        ----------

            - hashtag: str - (required)
            - from_post_id: int - (optional)
            - number: int - (optional)

        """
        return get_timeline_by_hashtag(self, hashtag, **params)

    def get_my_posts(self, **params) -> PostsResponse:
        """

        Parameters:
        ---------------

            - from_post_id: int - (optional)
            - number: int - (optional)
            - include_group_post: bool - (optional)

        """
        return get_my_posts(self, **params)

    def get_post(self, post_id: int) -> Post:
        return get_post(self, post_id)

    def get_post_likers(self, post_id: int, **params) -> PostLikersResponse:
        """

        Parameters:
        ---------------

            - from_id: int - (optional)
            - number: int - (optional)

        """
        return get_post_likers(self, post_id, **params)

    def get_post_reposts(self, post_id: int, **params: int) -> PostsResponse:
        """

        Parameters:
        ---------------

            - post_id: int - (required)
            - from_post_id: int - (optional)
            - number: int - (optional)

        """
        return get_post_reposts(self, post_id, **params)

    def get_posts(self, post_ids: List[int]) -> PostsResponse:
        return get_posts(self, post_ids)

    def get_recommended_post_tags(
        self, tag: str = None, save_recent_search: bool = False
    ) -> PostTagsResponse:
        return get_recommended_post_tags(self, tag, save_recent_search)

    def get_recommended_posts(self, **params) -> PostsResponse:
        """

        Parameters:
        ---------------

            - experiment_num: int
            - variant_num: int
            - number: int

        """
        return get_recommended_posts(self, **params)

    def get_timeline_by_keyword(self, keyword: str = None, **params) -> PostsResponse:
        """

        Parameters:
        ---------------

            - keyword: str
            - from_post_id: int
            - number: int

        """
        return get_timeline_by_keyword(self, keyword, **params)

    def get_timeline(self, **params: int | str | bool) -> PostsResponse:
        # - from: str - (optional)
        """

        Parameters:
        ---------------

            - noreply_mode: bool - (optional)
            - from_post_id: int - (optional)
            - number: int - (optional)
            - order_by: str - (optional)
            - experiment_older_age_rules: bool - (optional)
            - shared_interest_categories: bool - (optional)
            - mxn: int - (optional)
            - en: int - (optional)
            - vn: int - (optional)
            - reduce_selfie: bool - (optional)
            - custom_generation_range: bool - (optional)

        """
        return get_timeline(self, **params)

    def get_url_metadata(self, url: str) -> SharedUrl:
        return get_url_metadata(self, url)

    def get_user_timeline(self, user_id: int, **params) -> PostsResponse:
        """

        Parameters:
        ---------------

            - from_post_id: int - (optional)
            - number: int - (optional)
            - post_type: str - (optional)

        """
        return get_user_timeline(self, user_id, **params)

    def like_posts(self, post_ids: List[int]) -> LikePostsResponse:
        return like_posts(self, post_ids)

    def remove_bookmark(self, user_id: int, post_id: int):
        return remove_bookmark(self, user_id, post_id)

    def remove_group_highlight_post(self, group_id: int, post_id: int):
        return remove_group_highlight_post(self, group_id, post_id)

    def remove_posts(self, post_ids: List[int]):
        return remove_posts(self, post_ids)

    def report_post(
            self,
            post_id: int,
            opponent_id: int,
            category_id: int,
            reason: str = None,
            screenshot_filename: str = None,
            screenshot_2_filename: str = None,
            screenshot_3_filename: str = None,
            screenshot_4_filename: str = None
    ):
        return report_post(
            self,
            post_id,
            opponent_id,
            category_id,
            reason,
            screenshot_filename,
            screenshot_2_filename,
            screenshot_3_filename,
            screenshot_4_filename
        )

    def unlike_post(self, post_id: int):
        return unlike_post(self, post_id)

    def update_post(
            self,
            post_id: int,
            text: str = None,
            font_size: int = None,
            color: int = None,
            message_tags: str = "[]",
    ) -> Post:
        return update_post(
            self, post_id, text, font_size, color, message_tags
        )

    def update_recommendation_feedback(
        self, post_id: int, feedback_result: str, *,
        experiment_num: int, variant_num: int,
    ):
        return update_recommendation_feedback(
            self, post_id, feedback_result, experiment_num, variant_num
        )

    def validate_post(self, text: str, *, group_id: int = None, thread_id: int = None) -> ValidationPostResponse:
        return validate_post(self, text, group_id, thread_id)

    def view_video(self, video_id: int):
        return view_video(self, video_id)

    def vote_survey(self, survey_id: int, choice_id: int) -> Survey:
        return vote_survey(self, survey_id, choice_id)

    # -REVIEW

    def create_review(self, user_id: int, comment: str):
        return create_review(self, user_id, comment)

    def create_reviews(self, user_ids: List[int], comment: str):
        return create_reviews(self, user_ids, comment)

    def delete_reviews(self, review_ids: List[int]):
        return delete_reviews(self, review_ids)

    def get_my_reviews(self, from_id: int = None) -> ReviewsResponse:
        return get_my_reviews(self, from_id)

    def get_reviews(self, user_id: int, from_id: int = None) -> ReviewsResponse:
        return get_reviews(self, user_id, from_id)

    def pin_review(self, review_id: int):
        return pin_review(self, review_id)

    def unpin_review(self, review_id: int):
        return unpin_review(self, review_id)

    # -THREAD

    def add_post_to_thread(self, post_id: int, thread_id: int) -> ThreadInfo:
        return add_post_to_thread(self, post_id, thread_id)

    def convert_post_to_thread(
            self,
            post_id: int,
            title: str = None,
            thread_icon_filename: str = None
    ) -> ThreadInfo:
        return convert_post_to_thread(
            self,
            post_id,
            title,
            thread_icon_filename
        )

    def create_thread(
            self,
            group_id: int,
            title: str,
            thread_icon_filename: str
    ) -> ThreadInfo:
        return create_thread(
            self,
            group_id,
            title,
            thread_icon_filename
        )

    def get_group_thread_list(self, group_id: int, from_str: str = None, **params) -> GroupThreadListResponse:
        """

        Parameters:
        ----------

            - group_id: int
            - from_str: str = None
            - join_status: str = None

        """
        return get_group_thread_list(self, group_id, from_str, **params)

    def get_thread_joined_statuses(self, ids: List[int]) -> dict:
        return get_thread_joined_statuses(self, ids)

    def get_thread_posts(self, thread_id: int, from_str: str = None, **params) -> PostsResponse:
        """

        Parameters:
        ----------

            - post_type: str
            - number: int = None
            - from_str: str = None

        """
        return get_thread_posts(self, thread_id, from_str, **params)

    def join_thread(self, thread_id: int, user_id: int):
        return join_thread(self, thread_id, user_id)

    def leave_thread(self, thread_id: int, user_id: int):
        return leave_thread(self, thread_id, user_id)

    def remove_thread(self, thread_id: int):
        return remove_thread(self, thread_id)

    def update_thread(
            self,
            thread_id: int,
            title: str,
            thread_icon_filename: str
    ):
        return update_thread(
            self,
            thread_id,
            title,
            thread_icon_filename
        )

    # -USER

    def create_user(
            self,
            nickname: str,
            birth_date: str,
            gender: int = -1,
            country_code: str = "JP",
            biography: str = None,
            prefecture: str = None,
            profile_icon_filename: str = None,
            cover_image_filename: str = None,
            # @Nullable @Part("sns_info") SignUpSnsInfoRequest signUpSnsInfoRequest,
            email: str = None,
            password: str = None,
            email_grant_token: str = None,
            en: int = None,
            vn: int = None
    ) -> CreateUserResponse:
        """
        birth_date: 2000-01-01の形式
        """
        return create_user(
            self,
            nickname,
            birth_date,
            gender,
            country_code,
            biography,
            prefecture,
            profile_icon_filename,
            cover_image_filename,
            email,
            password,
            email_grant_token,
            en,
            vn
        )

    def delete_contact_friends(self):
        return delete_contact_friends(self)

    def delete_footprint(self, user_id: int, footprint_id: int):
        return delete_footprint(self, user_id, footprint_id)

    def destroy_user(self):
        return destroy_user(self)

    def follow_user(self, user_id: int):
        return follow_user(self, user_id)

    def follow_users(self, user_ids: List[int]):
        return follow_users(self, user_ids)

    def get_active_followings(self, **params) -> ActiveFollowingsResponse:
        """

        Parameters:
        ----------

            - only_online: bool
            - from_loggedin_at: int = None

        """
        return get_active_followings(self, **params)

    # def get_additional_settings(self) -> Settings:
    #     return get_additional_settings(self)

    def get_app_review_status(self) -> AppReviewStatusResponse:
        return get_app_review_status(self)

    def get_contact_status(self, mobile_numbers: List[str]) -> ContactStatusResponse:
        return get_contact_status(self, mobile_numbers)

    # def get_default_settings(self) -> TimelineSettings:
    #     return get_default_settings(self)

    def get_follow_recommendations(self, **params) -> FollowRecommendationsResponse:
        """

        Parameters:
        ----------

            - from_timestamp: int = None,
            - number: int = None,
            - sources: List[str] = None

        """
        return get_follow_recommendations(self, **params)

    def get_follow_request(self, from_timestamp: int = None) -> UsersByTimestampResponse:
        return get_follow_request(self, from_timestamp)

    def get_follow_request_count(self) -> int:
        return get_follow_request_count(self)

    def get_following_users_born(self, birthdate: int = None) -> UsersResponse:
        return get_following_users_born(self, birthdate)

    def get_footprints(self, **params) -> List[Footprint]:
        """

        Parameters:
        ----------

            - from_id: int = None
            - number: int = None
            - mode: str = None

        """
        return get_footprints(self, **params)

    def get_fresh_user(self, user_id: int) -> UserResponse:
        return get_fresh_user(self, user_id)

    def get_hima_users(self, **params) -> List[UserWrapper]:
        """

        Parameters:
        ----------

            - from_hima_id: int = None
            - number: int = None

        """
        return get_hima_users(self, **params)

    def get_initial_recommended_users_to_follow(self, **params) -> UsersResponse:
        return get_initial_recommended_users_to_follow(self, **params)

    def get_recommended_users_to_follow_for_profile(
            self, user_id: int, **params
    ) -> UsersResponse:
        """

        Parameters:
        ----------

            - user_id: int - (Required)
            - number: int - (Optional)
            - page: int - (Optional)

        """
        return get_recommended_users_to_follow_for_profile(
            self, user_id, **params
        )

    def get_refresh_counter_requests(self) -> RefreshCounterRequestsResponse:
        return get_refresh_counter_requests(self)

    def get_social_shared_users(self, **params) -> SocialShareUsersResponse:
        """

        Parameters:
        ----------

            - sns_name: str - (Required)
            - number: int - (Optional)
            - from_id: int - (Optional)

        """
        return get_social_shared_users(self, **params)

    def get_timestamp(self) -> UserTimestampResponse:
        return get_timestamp(self)

    def get_user(self, user_id: int) -> User:
        return get_user(self, user_id)

    def get_user_custom_definitions(self) -> UserCustomDefinitionsResponse:
        return get_user_custom_definitions(self)

    def get_user_email(self, user_id: int) -> str:
        return get_user_email(self, user_id)

    def get_user_followers(self, user_id: int, **params) -> FollowUsersResponse:
        """

        Parameters:
        ----------

            - user_id: int
            - from_follow_id: int = None
            - followed_by_me: int = None

        """
        return get_user_followers(self, user_id, **params)

    def get_user_followings(self, user_id: int, **params) -> FollowUsersResponse:
        """

        Parameters:
        ----------

            - user_id: int
            - from_follow_id: int = None
            - from_timestamp: int = None
            - order_by: str = None

        """
        return get_user_followings(self, user_id, **params)

    def get_user_from_qr(self, qr: str) -> UserResponse:
        return get_user_from_qr(self, qr)

    # def get_user_interests(self):
    #     return get_user_interests(self)

    def get_user_without_leaving_footprint(self, user_id: int) -> UserResponse:
        return get_user_without_leaving_footprint(self, user_id)

    def get_users(self, user_ids: List[int]) -> UsersResponse:
        return get_users(self, user_ids)

    def get_users_from_uuid(self, uuid: str) -> UsersResponse:
        return get_users_from_uuid(self, uuid)

    def post_social_shared(self, sns_name: str):
        return post_social_shared(self, sns_name)

    def record_app_review_status(self):
        return record_app_review_status(self)

    def reduce_kenta_penalty(self, user_id: int):
        return reduce_kenta_penalty(self, user_id)

    def refresh_counter(self, counter: str):
        return refresh_counter(self, counter)

    def remove_user_avatar(self):
        return remove_user_avatar(self)

    def remove_user_cover(self):
        return remove_user_cover(self)

    def report_user(
            self,
            user_id: int,
            category_id: int,
            reason: str = None,
            screenshot_filename: str = None,
            screenshot_2_filename: str = None,
            screenshot_3_filename: str = None,
            screenshot_4_filename: str = None
    ):
        return report_user(
            self,
            user_id,
            category_id,
            reason,
            screenshot_filename,
            screenshot_2_filename,
            screenshot_3_filename,
            screenshot_4_filename
        )

    def reset_password(self, email: str, email_grant_token: str, password: str):
        return reset_password(self, email, email_grant_token, password)

    def search_lobi_users(self, **params) -> UsersResponse:
        """

        Parameters:
        ----------

            - nickname: str = None
            - number: int = None
            - from_str: str = None

        """
        return search_lobi_users(self ** params)

    def search_users(self, **params) -> UsersResponse:
        """

        Parameters:
        ----------

            - gender: int = None
            - nickname: str = None
            - title: str = None
            - biography: str = None
            - from_timestamp: int = None
            - similar_age: bool = None
            - not_recent_gomimushi: bool = None
            - recently_created: bool = None
            - same_prefecture: bool = None
            - save_recent_search: bool = None

        """
        return search_users(self, **params)

    def set_additional_setting_enabled(self, mode: str, on: int = None):
        return set_additional_setting_enabled(self, mode, on)

    def set_follow_permission_enabled(
            self, nickname: str, is_private: bool = None
    ):
        return set_follow_permission_enabled(self, nickname, is_private)

    def set_setting_follow_recommendation_enabled(self, on: bool):
        return set_setting_follow_recommendation_enabled(self, bool)

    def take_action_follow_request(self, target_id: int, action: str):
        return take_action_follow_request(self, target_id, action)

    def turn_on_hima(self):
        return turn_on_hima(self)

    def unfollow_user(self, user_id: int):
        return unfollow_user(self, user_id)

    def update_invite_contact_status(self, mobile_number: str):
        return update_invite_contact_status(self, mobile_number)

    def update_language(self, language: str):
        return update_language(self, language)

    def update_user(
            self,
            nickname: str,
            biography: str = None,
            prefecture: str = None,
            gender: int = None,
            country_code: str = None,
            profile_icon_filename: str = None,
            cover_image_filename: str = None,
            username: str = None,
    ):
        return update_user(
            self, nickname, biography, prefecture, gender, country_code,
            profile_icon_filename, cover_image_filename, username
        )

    # def update_user_interests(self):
    #     return update_user_interests(self)

    # def upload_contacts_friends(self):
    #     return upload_contacts_friends(self)

    def upload_twitter_friend_ids(self, twitter_friend_ids: List[str]):
        return upload_twitter_friend_ids(self, twitter_friend_ids)

    def block_user(self, user_id: int):
        return block_user(self, user_id)

    def get_blocked_user_ids(self) -> BlockedUserIdsResponse:
        return get_blocked_user_ids(self)

    def get_blocked_users(self, from_id: int = None) -> BlockedUsersResponse:
        return get_blocked_users(self, from_id)

    def unblock_user(self, user_id: int):
        return unblock_user(self, user_id)

    def get_hidden_users_list(self, **params: Union[str, int]) -> HiddenResponse:
        """

        Parameters:
        ----------

            - from: str = None
            - number: int = None

        """
        return get_hidden_users_list(self, **params)

    def hide_user(self, user_id: int):
        return hide_user(self, user_id)

    def unhide_users(self, user_ids: List[int]):
        return unhide_users(self, user_ids)
