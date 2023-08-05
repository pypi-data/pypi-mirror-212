from typing import Union, Any
from pydantic import BaseModel as BM
from .enums import CHAT_START_ID
from .event_objects import *

class WrongEventException(Exception):
    pass

class BaseEvent(BM):
    raw:dict
    group_id:int
    v:str
    object:Any # ЗАГЛУШКА

    @property
    def type(self):
        return type(self)

class MessageNew(BaseEvent):
    object:MessageNewObject
    from_chat:bool = False
    from_user:bool = False
    from_group:bool = False
    chat_id:int|None = None

    def __init__(self, **data):
        super().__init__(**data)

        peer_id = self.object.message.peer_id
        if peer_id < 0:
            self.from_group = True
        elif peer_id > CHAT_START_ID:
            self.from_chat = True
        else: self.from_user = True

        if self.from_chat:
            self.chat_id = peer_id - CHAT_START_ID



class MessageReply(BaseEvent):
    object:MessageReplyObject

class MessageEdit(BaseEvent):
    object:MessageEditObject

class MessageAllow(BaseEvent):
    object:MessageAllowObject

class MessageDeny(BaseEvent):
    object:MessageDenyObject

class MessageTypingState(BaseEvent):
    object:MessageTypingStateObject

class MessageEvent(BaseEvent):
    object:MessageEventObject


class PhotoNew(BaseEvent):
    object:PhotoNewObject

class PhotoCommentNew(BaseEvent):
    object:PhotoObject

class PhotoCommentEdit(BaseEvent):
    object:PhotoObject

class PhotoCommentRestore(BaseEvent):
    object:PhotoObject


class AudioNew(BaseEvent):
    object:AudioNewObject


class VideoNew(BaseEvent):
    object:VideoNewObject

class VideoCommentNew(BaseEvent):
    object:VideoCommentObject

class VideoCommentEdit(BaseEvent):
    object:VideoCommentObject

class VideoCommentRestore(BaseEvent):
    object:VideoCommentObject

class VideoCommentDelete(BaseEvent):
    object:VideoCommentDeleteObject


class WallPostNew(BaseEvent):
    object:WallObject

class WallRepost(BaseEvent):
    object:WallObject


class WallReplyNew(BaseEvent):
    object:WallReplyObject

class WallReplyEdit(BaseEvent):
    object:WallReplyObject

class WallReplyRestore(BaseEvent):
    object:WallReplyObject

class WallReplyDelete(BaseEvent):
    object:WallReplyDeleteObject


class LikeAdd(BaseEvent):
    object:LikeObject

class LikeRemove(BaseEvent):
    object:LikeObject


class BoardPostNew(BaseEvent):
    object:BoardPostObject

class BoardPostEdit(BaseEvent):
    object:BoardPostObject

class BoardPostRestore(BaseEvent):
    object:BoardPostObject

class BoardPostDelete(BaseEvent):
    object:BoardPostDeleteObject


class MarketCommentNew(BaseEvent):
    object:MarketCommentObject

class MarketCommentEdit(BaseEvent):
    object:MarketCommentObject

class MarketCommentRestore(BaseEvent):
    object:MarketCommentObject

class MarketCommentDelete(BaseEvent):
    object:MarketCommentDeleteObject

class MarketOrderNew(BaseEvent):
    object:MarketOrderObject

class MarketOrderEdit(BaseEvent):
    object:MarketOrderObject


class GroupJoin(BaseEvent):
    object:GroupJoinObject

class GroupLeave(BaseEvent):
    object:GroupLeaveObject

class UserBlock(BaseEvent):
    object:UserBlockObject

class UserUnblock(BaseEvent):
    object:UserUnblockObject


class PollVoteNew(BaseEvent):
    object:PollVoteNewObject

class GroupOfficersEdit(BaseEvent):
    object:GroupOfficersEditObject

class GroupChangeSettings(BaseEvent):
    object:GroupChangeSettingsObject

class GroupChangePhoto(BaseEvent):
    object:GroupChangePhotoObject

class VkPayTransaction(BaseEvent):
    object:VkPayTransactionObject

class AppPayload(BaseEvent):
    object:AppPayloadObject


class DonutSubscriptionCreate(BaseEvent):
    object:DonutSubscriptionCreateObject

class DonutSubscriptionProlonged(BaseEvent):
    object:DonutSubscriptionProlongedObject

class DonutSubscriptionExpired(BaseEvent):
    object:DonutSubscriptionExpiredObject

class DonutSubscriptionCancelled(BaseEvent):
    object:DonutSubscriptionCancelledObject

class DonutSubscriptionPriceChanged(BaseEvent):
    object:DonutSubscriptionPriceChangedObject

class DonutMoneyWithdraw(BaseEvent):
    object:DonutMoneyWithdrawObject

class DonutMoneyWithdrawError(BaseEvent):
    object:DonutMoneyWithdrawErrorObject

AnyBotEvent = Union[MessageNew, MessageReply, MessageEdit, MessageAllow, MessageDeny, MessageTypingState, MessageEvent, PhotoNew, PhotoCommentNew, PhotoCommentEdit, PhotoCommentRestore, AudioNew, VideoNew, VideoCommentNew, VideoCommentEdit, VideoCommentRestore, VideoCommentDelete, WallPostNew, WallRepost, WallReplyNew, WallReplyEdit, WallReplyRestore, WallReplyDelete, LikeAdd, LikeRemove, BoardPostNew, BoardPostEdit, BoardPostRestore, BoardPostDelete, MarketCommentNew, MarketCommentEdit, MarketCommentRestore, MarketCommentDelete, MarketOrderNew, MarketOrderEdit, GroupJoin, GroupLeave, UserBlock, UserUnblock, PollVoteNew, GroupOfficersEdit, GroupChangeSettings, GroupChangePhoto, VkPayTransaction, AppPayload, DonutSubscriptionCreate, DonutSubscriptionProlonged, DonutSubscriptionExpired, DonutSubscriptionCancelled, DonutSubscriptionPriceChanged, DonutMoneyWithdraw, DonutMoneyWithdrawError]

def _get_event(**kwargs) -> AnyBotEvent:
        for i in AnyBotEvent.__args__:
            try:
                return i(**kwargs, raw=kwargs)
            except: pass
        raise WrongEventException('Event not found! Please create a problem at github.com/kravandir/kavk_api\nRaw event:',
                                  kwargs)

__all__ = (
"MessageNew","MessageReply","MessageEdit","MessageAllow","MessageDeny","MessageTypingState","MessageEvent","PhotoNew",
"PhotoCommentNew","PhotoCommentEdit","PhotoCommentRestore","AudioNew","VideoNew","VideoCommentNew","VideoCommentEdit",
"VideoCommentRestore","VideoCommentDelete","WallPostNew","WallRepost","WallReplyNew","WallReplyEdit",
"WallReplyRestore","WallReplyDelete","LikeAdd","LikeRemove","BoardPostNew","BoardPostEdit",
"BoardPostRestore","BoardPostDelete","MarketCommentNew","MarketCommentEdit","MarketCommentRestore",
"MarketCommentDelete","MarketOrderNew","MarketOrderEdit","GroupJoin","GroupLeave", "UserBlock","UserUnblock",
"PollVoteNew", "GroupOfficersEdit", "GroupChangeSettings", "GroupChangePhoto", "VkPayTransaction", "AppPayload",
"DonutSubscriptionCreate", "DonutSubscriptionProlonged", "DonutSubscriptionExpired","DonutSubscriptionCancelled",
"DonutSubscriptionPriceChanged", "DonutMoneyWithdraw", "DonutMoneyWithdrawError", 'WrongEventException', 'AnyBotEvent', '_get_event'
)
