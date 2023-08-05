from enum import Enum
from inspect import isclass
from typing import NewType, Optional, Union
from .base import BM
from .base import BaseList as BL

class AccountNameRequestStatus(Enum):
	SUCCESS = "success"
	PROCESSING = "processing"
	DECLINED = "declined"
	WAS_ACCEPTED = "was_accepted"
	WAS_DECLINED = "was_declined"
	DECLINED_WITH_LINK = "declined_with_link"
	RESPONSE = "response"
	RESPONSE_WITH_LINK = "response_with_link"

class AccountPushParamsMode(Enum):
	ON = "on"
	OFF = "off"
	NO_SOUND = "no_sound"
	NO_TEXT = "no_text"

class AccountPushParamsOnoff(Enum):
	ON = "on"
	OFF = "off"

class AccountPushParamsSettings(Enum):
	ON = "on"
	OFF = "off"
	FR_OF_FR = "fr_of_fr"

class AccountAccountCounters(BM):
	app_requests:Optional[int] = None
	events:Optional[int] = None
	faves:Optional[int] = None
	friends:Optional[int] = None
	friends_suggestions:Optional[int] = None
	friends_recommendations:Optional[int] = None
	gifts:Optional[int] = None
	groups:Optional[int] = None
	menu_discover_badge:Optional[int] = None
	menu_clips_badge:Optional[int] = None
	messages:Optional[int] = None
	memories:Optional[int] = None
	notes:Optional[int] = None
	notifications:Optional[int] = None
	photos:Optional[int] = None
	sdk:Optional[int] = None


class AccountInfo(BM):
	wishlists_ae_promo_banner_show:Optional[bool] = None
	_2fa_required:Optional[bool] = None
	country:Optional[str] = None
	https_required:Optional[bool] = None
	intro:Optional[bool] = None
	show_vk_apps_intro:Optional[bool] = None
	mini_apps_ads_slot_id:Optional[int] = None
	qr_promotion:Optional[int] = None
	link_redirects:Optional[object] = None
	lang:Optional[int] = None
	no_wall_replies:Optional[bool] = None
	own_posts_default:Optional[bool] = None
	subscriptions:Optional[object] = None


class AccountNameRequest(BM):
	first_name:Optional[str] = None
	id:Optional[int] = None
	last_name:Optional[str] = None
	status:Optional["AccountNameRequestStatus"] = None
	lang:Optional[str] = None
	link_href:Optional[str] = None
	link_label:Optional[str] = None


class AccountOffer(BM):
	description:Optional[str] = None
	id:Optional[int] = None
	img:Optional[str] = None
	instruction:Optional[str] = None
	instruction_html:Optional[str] = None
	price:Optional[int] = None
	short_description:Optional[str] = None
	tag:Optional[str] = None
	title:Optional[str] = None
	currency_amount:Optional[int] = None
	link_id:Optional[int] = None
	link_type:Optional[str] = None


class AccountPushConversations(BM):
	count:Optional[int] = None
	items:Optional[list["AccountPushConversationsItem"]] = None


class AccountPushConversationsItem(BM):
	disabled_until:int
	peer_id:int
	sound:bool
	disabled_mentions:Optional[bool] = None
	disabled_mass_mentions:Optional[bool] = None


class AccountPushParams(BM):
	msg:Optional[list["AccountPushParamsMode"]] = None
	chat:Optional[list["AccountPushParamsMode"]] = None
	like:Optional[list["AccountPushParamsSettings"]] = None
	repost:Optional[list["AccountPushParamsSettings"]] = None
	comment:Optional[list["AccountPushParamsSettings"]] = None
	mention:Optional[list["AccountPushParamsSettings"]] = None
	reply:Optional[list["AccountPushParamsOnoff"]] = None
	new_post:Optional[list["AccountPushParamsOnoff"]] = None
	wall_post:Optional[list["AccountPushParamsOnoff"]] = None
	wall_publish:Optional[list["AccountPushParamsOnoff"]] = None
	friend:Optional[list["AccountPushParamsOnoff"]] = None
	friend_found:Optional[list["AccountPushParamsOnoff"]] = None
	friend_accepted:Optional[list["AccountPushParamsOnoff"]] = None
	group_invite:Optional[list["AccountPushParamsOnoff"]] = None
	group_accepted:Optional[list["AccountPushParamsOnoff"]] = None
	birthday:Optional[list["AccountPushParamsOnoff"]] = None
	event_soon:Optional[list["AccountPushParamsOnoff"]] = None
	app_request:Optional[list["AccountPushParamsOnoff"]] = None
	sdk_open:Optional[list["AccountPushParamsOnoff"]] = None


class AccountPushSettings(BM):
	disabled:Optional[bool] = None
	disabled_until:Optional[int] = None
	settings:Optional["AccountPushParams"] = None
	conversations:Optional["AccountPushConversations"] = None


class AccountSubscriptions(int):
	pass

class AccountUserSettingsInterest(BM):
	title:str
	value:str


class AccountUserSettingsInterests(BM):
	activities:Optional["AccountUserSettingsInterest"] = None
	interests:Optional["AccountUserSettingsInterest"] = None
	music:Optional["AccountUserSettingsInterest"] = None
	tv:Optional["AccountUserSettingsInterest"] = None
	movies:Optional["AccountUserSettingsInterest"] = None
	books:Optional["AccountUserSettingsInterest"] = None
	games:Optional["AccountUserSettingsInterest"] = None
	quotes:Optional["AccountUserSettingsInterest"] = None
	about:Optional["AccountUserSettingsInterest"] = None




class AddressesFields(Enum):
	ID = "id"
	TITLE = "title"
	ADDRESS = "address"
	ADDITIONAL_ADDRESS = "additional_address"
	COUNTRY_ID = "country_id"
	CITY_ID = "city_id"
	METRO_STATION_ID = "metro_station_id"
	LATITUDE = "latitude"
	LONGITUDE = "longitude"
	DISTANCE = "distance"
	WORK_INFO_STATUS = "work_info_status"
	TIMETABLE = "timetable"
	PHONE = "phone"
	TIME_OFFSET = "time_offset"



class AdsAccessRole(Enum):
	ADMIN = "admin"
	MANAGER = "manager"
	REPORTS = "reports"

class AdsAccessRolePublic(Enum):
	MANAGER = "manager"
	REPORTS = "reports"

class AdsAccountType(Enum):
	GENERAL = "general"
	AGENCY = "agency"

class AdsAdApproved(Enum):
	NOT_MODERATED = 0
	PENDING_MODERATION = 1
	APPROVED = 2
	REJECTED = 3

class AdsAdCostType(Enum):
	PER_CLICKS = 0
	PER_IMPRESSIONS = 1
	PER_ACTIONS = 2
	PER_IMPRESSIONS_OPTIMIZED = 3

class AdsAdStatus(Enum):
	STOPPED = 0
	STARTED = 1
	DELETED = 2

class AdsCampaignStatus(Enum):
	STOPPED = 0
	STARTED = 1
	DELETED = 2

class AdsCampaignType(Enum):
	NORMAL = "normal"
	VK_APPS_MANAGED = "vk_apps_managed"
	MOBILE_APPS = "mobile_apps"
	PROMOTED_POSTS = "promoted_posts"
	ADAPTIVE_ADS = "adaptive_ads"
	STORIES = "stories"

class AdsCriteriaSex(Enum):
	ANY = 0
	MALE = 1
	FEMALE = 2

class AdsObjectType(Enum):
	AD = "ad"
	CAMPAIGN = "campaign"
	CLIENT = "client"
	OFFICE = "office"

class AdsStatsSexValue(Enum):
	FEMALE = "f"
	MALE = "m"

class AdsTargSuggestionsSchoolsType(Enum):
	SCHOOL = "school"
	UNIVERSITY = "university"
	FACULTY = "faculty"
	CHAIR = "chair"

class AdsAccesses(BM):
	client_id:Optional[str] = None
	role:Optional["AdsAccessRole"] = None


class AdsAccount(BM):
	access_role:"AdsAccessRole"
	account_id:int
	account_status:bool
	account_type:"AdsAccountType"
	account_name:str
	can_view_budget:bool


class AdsAd(BM):
	ad_format:int
	ad_platform:Optional[list[int|str]] = None
	all_limit:int
	approved:"AdsAdApproved"
	campaign_id:int
	category1_id:Optional[int] = None
	category2_id:Optional[int] = None
	cost_type:"AdsAdCostType"
	cpc:Optional[int] = None
	cpm:Optional[int] = None
	cpa:Optional[int] = None
	ocpm:Optional[int] = None
	autobidding_max_cost:Optional[int] = None
	disclaimer_medical:Optional[bool] = None
	disclaimer_specialist:Optional[bool] = None
	disclaimer_supplements:Optional[bool] = None
	id:int
	impressions_limit:Optional[int] = None
	impressions_limited:Optional[bool] = None
	name:str
	status:"AdsAdStatus"
	video:Optional[bool] = None


class AdsAdLayout(BM):
	ad_format:int
	campaign_id:int
	cost_type:"AdsAdCostType"
	description:str
	id:str
	image_src:str
	image_src_2x:Optional[str] = None
	link_domain:Optional[str] = None
	link_url:str
	preview_link:Optional[str] = None
	title:str
	video:Optional[bool] = None


class AdsCampaign(BM):
	ads_count:Optional[int] = None
	all_limit:str
	create_time:Optional[int] = None
	goal_type:Optional[int] = None
	user_goal_type:Optional[int] = None
	is_cbo_enabled:Optional[bool] = None
	day_limit:str
	id:int
	name:str
	start_time:int
	status:"AdsCampaignStatus"
	stop_time:int
	type:"AdsCampaignType"
	update_time:Optional[int] = None
	views_limit:Optional[int] = None


class AdsCategory(BM):
	id:int
	name:str
	subcategories:Optional[list["AdsCategory"]] = None


class AdsClient(BM):
	all_limit:str
	day_limit:str
	id:int
	name:str


class AdsCreateAdStatus(BM):
	id:int
	post_id:Optional[int] = None
	error_code:Optional[int] = None
	error_desc:Optional[str] = None


class AdsCreateCampaignStatus(BM):
	id:int
	error_code:Optional[int] = None
	error_desc:Optional[str] = None


class AdsCriteria(BM):
	age_from:Optional[int] = None
	age_to:Optional[int] = None
	apps:Optional[str] = None
	apps_not:Optional[str] = None
	birthday:Optional[int] = None
	cities:Optional[str] = None
	cities_not:Optional[str] = None
	country:Optional[int] = None
	districts:Optional[str] = None
	groups:Optional[str] = None
	interest_categories:Optional[str] = None
	interests:Optional[str] = None
	paying:Optional[bool] = None
	positions:Optional[str] = None
	religions:Optional[str] = None
	retargeting_groups:Optional[str] = None
	retargeting_groups_not:Optional[str] = None
	school_from:Optional[int] = None
	school_to:Optional[int] = None
	schools:Optional[str] = None
	sex:Optional["AdsCriteriaSex"] = None
	stations:Optional[str] = None
	statuses:Optional[str] = None
	streets:Optional[str] = None
	travellers:Optional["BasePropertyExists"] = None
	uni_from:Optional[int] = None
	uni_to:Optional[int] = None
	user_browsers:Optional[str] = None
	user_devices:Optional[str] = None
	user_os:Optional[str] = None


class AdsDemoStats(BM):
	id:Optional[int] = None
	stats:Optional["AdsDemostatsFormat"] = None
	type:Optional["AdsObjectType"] = None


class AdsDemostatsFormat(BM):
	age:Optional[list["AdsStatsAge"]] = None
	cities:Optional[list["AdsStatsCities"]] = None
	day:Optional[str] = None
	month:Optional[str] = None
	overall:Optional[int] = None
	sex:Optional[list["AdsStatsSex"]] = None
	sex_age:Optional[list["AdsStatsSexAge"]] = None


class AdsFloodStats(BM):
	left:int
	refresh:int


class AdsLinkStatus(BM):
	description:str
	redirect_url:str
	status:str


class AdsLookalikeRequest(BM):
	id:int
	create_time:int
	update_time:int
	scheduled_delete_time:Optional[int] = None
	status:str
	source_type:str
	source_retargeting_group_id:Optional[int] = None
	source_name:Optional[str] = None
	audience_count:Optional[int] = None
	save_audience_levels:Optional[list["AdsLookalikeRequestSaveAudienceLevel"]] = None


class AdsLookalikeRequestSaveAudienceLevel(BM):
	level:Optional[int] = None
	audience_count:Optional[int] = None


class AdsMusician(BM):
	id:int
	name:str
	avatar:Optional[str] = None


class AdsParagraphs(BM):
	paragraph:Optional[str] = None


class AdsPromotedPostReach(BM):
	hide:int
	id:int
	join_group:int
	links:int
	reach_subscribers:int
	reach_total:int
	report:int
	to_group:int
	unsubscribe:int
	video_views_100p:Optional[int] = None
	video_views_25p:Optional[int] = None
	video_views_3s:Optional[int] = None
	video_views_50p:Optional[int] = None
	video_views_75p:Optional[int] = None
	video_views_start:Optional[int] = None


class AdsRejectReason(BM):
	comment:Optional[str] = None
	rules:Optional[list["AdsRules"]] = None


class AdsRules(BM):
	paragraphs:Optional[list["AdsParagraphs"]] = None
	title:Optional[str] = None


class AdsStats(BM):
	id:Optional[int] = None
	stats:Optional["AdsStatsFormat"] = None
	type:Optional["AdsObjectType"] = None
	views_times:Optional["AdsStatsViewsTimes"] = None


class AdsStatsAge(BM):
	clicks_rate:Optional[int] = None
	impressions_rate:Optional[int] = None
	value:Optional[str] = None


class AdsStatsCities(BM):
	clicks_rate:Optional[int] = None
	impressions_rate:Optional[int] = None
	name:Optional[str] = None
	value:Optional[int] = None


class AdsStatsFormat(BM):
	clicks:Optional[int] = None
	link_external_clicks:Optional[int] = None
	day:Optional[str] = None
	impressions:Optional[int] = None
	join_rate:Optional[int] = None
	month:Optional[str] = None
	overall:Optional[int] = None
	reach:Optional[int] = None
	spent:Optional[int] = None
	video_clicks_site:Optional[int] = None
	video_views:Optional[int] = None
	video_views_full:Optional[int] = None
	video_views_half:Optional[int] = None


class AdsStatsSex(BM):
	clicks_rate:Optional[int] = None
	impressions_rate:Optional[int] = None
	value:Optional["AdsStatsSexValue"] = None


class AdsStatsSexAge(BM):
	clicks_rate:Optional[int] = None
	impressions_rate:Optional[int] = None
	value:Optional[str] = None


class AdsStatsViewsTimes(BM):
	views_ads_times_1:Optional[int] = None
	views_ads_times_2:Optional[int] = None
	views_ads_times_3:Optional[int] = None
	views_ads_times_4:Optional[int] = None
	views_ads_times_5:Optional[str] = None
	views_ads_times_6:Optional[int] = None
	views_ads_times_7:Optional[int] = None
	views_ads_times_8:Optional[int] = None
	views_ads_times_9:Optional[int] = None
	views_ads_times_10:Optional[int] = None
	views_ads_times_11_plus:Optional[int] = None


class AdsTargStats(BM):
	audience_count:int
	recommended_cpc:Optional[int] = None
	recommended_cpm:Optional[int] = None
	recommended_cpc_50:Optional[int] = None
	recommended_cpm_50:Optional[int] = None
	recommended_cpc_70:Optional[int] = None
	recommended_cpm_70:Optional[int] = None
	recommended_cpc_90:Optional[int] = None
	recommended_cpm_90:Optional[int] = None


class AdsTargSuggestions(BM):
	id:Optional[int] = None
	name:Optional[str] = None


class AdsTargSuggestionsCities(BM):
	id:Optional[int] = None
	name:Optional[str] = None
	parent:Optional[str] = None


class AdsTargSuggestionsRegions(BM):
	id:Optional[int] = None
	name:Optional[str] = None
	type:Optional[str] = None


class AdsTargSuggestionsSchools(BM):
	desc:Optional[str] = None
	id:Optional[int] = None
	name:Optional[str] = None
	parent:Optional[str] = None
	type:Optional["AdsTargSuggestionsSchoolsType"] = None


class AdsTargetGroup(BM):
	audience_count:Optional[int] = None
	domain:Optional[str] = None
	id:Optional[int] = None
	lifetime:Optional[int] = None
	name:Optional[str] = None
	pixel:Optional[str] = None


class AdsUpdateOfficeUsersResult(BM):
	user_id:int
	is_success:bool
	error:Optional["BaseError"] = None


class AdsUserSpecification(BM):
	user_id:int
	role:"AdsAccessRolePublic"
	grant_access_to_all_clients:Optional[bool] = None
	client_ids:Optional[list[int]] = None
	view_budget:Optional[bool] = None


class AdsUserSpecificationCutted(BM):
	user_id:int
	role:"AdsAccessRolePublic"
	client_id:Optional[int] = None
	view_budget:Optional[bool] = None


class AdsUsers(BM):
	accesses:list["AdsAccesses"]
	user_id:int




class AdswebGetAdCategoriesResponseCategoriesCategory(BM):
	id:int
	name:str


class AdswebGetAdUnitsResponseAdUnitsAdUnit(BM):
	id:int
	site_id:int
	name:Optional[str] = None


class AdswebGetFraudHistoryResponseEntriesEntry(BM):
	site_id:int
	day:str


class AdswebGetSitesResponseSitesSite(BM):
	id:int
	status_user:Optional[str] = None
	status_moder:Optional[str] = None
	domains:Optional[str] = None


class AdswebGetStatisticsResponseItemsItem(BM):
	site_id:Optional[int] = None
	ad_unit_id:Optional[int] = None
	overall_count:Optional[int] = None
	months_count:Optional[int] = None
	month_min:Optional[str] = None
	month_max:Optional[str] = None
	days_count:Optional[int] = None
	day_min:Optional[str] = None
	day_max:Optional[str] = None
	hours_count:Optional[int] = None
	hour_min:Optional[str] = None
	hour_max:Optional[str] = None




class AppWidgetsPhoto(BM):
	id:str
	images:list["BaseImage"]


class AppWidgetsPhotos(BM):
	count:Optional[int] = None
	items:Optional[list["AppWidgetsPhoto"]] = None




class AppsAppLeaderboardType(Enum):
	NOT_SUPPORTED = 0
	LEVELS = 1
	POINTS = 2

class AppsAppType(Enum):
	APP = "app"
	GAME = "game"
	SITE = "site"
	STANDALONE = "standalone"
	VK_APP = "vk_app"
	COMMUNITY_APP = "community_app"
	HTML5_GAME = "html5_game"
	MINI_APP = "mini_app"

class AppsAppMin(BM):
	type:"AppsAppType"
	id:int
	title:str
	author_owner_id:Optional[int] = None
	is_installed:Optional[bool] = None
	icon_139:Optional[str] = None
	icon_150:Optional[str] = None
	icon_278:Optional[str] = None
	icon_576:Optional[str] = None
	background_loader_color:Optional[str] = None
	loader_icon:Optional[str] = None
	icon_75:Optional[str] = None


class AppsCatalogList(BM):
	count:int
	items:list["AppsApp"]
	profiles:Optional[list["UsersUserMin"]] = None


class AppsLeaderboard(BM):
	level:Optional[int] = None
	points:Optional[int] = None
	score:Optional[int] = None
	user_id:int


class AppsScope(BM):
	name:str
	title:Optional[str] = None




class AudioAudio(BM):
	access_key:Optional[str] = None
	artist:str
	id:int
	owner_id:int
	title:str
	url:Optional[str] = None
	duration:int
	date:Optional[int] = None
	album_id:Optional[int] = None
	genre_id:Optional[int] = None
	performer:Optional[str] = None




class bool(Enum):
	NO = 0
	YES = 1

class BaseLinkButtonActionType(Enum):
	OPEN_URL = "open_url"

class BaseLinkButtonStyle(Enum):
	PRIMARY = "primary"
	SECONDARY = "secondary"

class BaseLinkProductStatus(Enum):
	ACTIVE = "active"
	BLOCKED = "blocked"
	SOLD = "sold"
	DELETED = "deleted"
	ARCHIVED = "archived"

class BasePropertyExists(Enum):
	PROPERTY_EXISTS = 1

class BaseSex(Enum):
	UNKNOWN = 0
	FEMALE = 1
	MALE = 2

class BaseUserGroupFields(Enum):
	ABOUT = "about"
	ACTION_BUTTON = "action_button"
	ACTIVITIES = "activities"
	ACTIVITY = "activity"
	ADDRESSES = "addresses"
	ADMIN_LEVEL = "admin_level"
	AGE_LIMITS = "age_limits"
	AUTHOR_ID = "author_id"
	BAN_INFO = "ban_info"
	BDATE = "bdate"
	BLACKLISTED = "blacklisted"
	BLACKLISTED_BY_ME = "blacklisted_by_me"
	BOOKS = "books"
	CAN_CREATE_TOPIC = "can_create_topic"
	CAN_MESSAGE = "can_message"
	CAN_POST = "can_post"
	CAN_SEE_ALL_POSTS = "can_see_all_posts"
	CAN_SEE_AUDIO = "can_see_audio"
	CAN_SEND_FRIEND_REQUEST = "can_send_friend_request"
	CAN_UPLOAD_VIDEO = "can_upload_video"
	CAN_WRITE_PRIVATE_MESSAGE = "can_write_private_message"
	CAREER = "career"
	CITY = "city"
	COMMON_COUNT = "common_count"
	CONNECTIONS = "connections"
	CONTACTS = "contacts"
	COUNTERS = "counters"
	COUNTRY = "country"
	COVER = "cover"
	CROP_PHOTO = "crop_photo"
	DEACTIVATED = "deactivated"
	DESCRIPTION = "description"
	DOMAIN = "domain"
	EDUCATION = "education"
	EXPORTS = "exports"
	FINISH_DATE = "finish_date"
	FIXED_POST = "fixed_post"
	FOLLOWERS_COUNT = "followers_count"
	FRIEND_STATUS = "friend_status"
	GAMES = "games"
	HAS_MARKET_APP = "has_market_app"
	HAS_MOBILE = "has_mobile"
	HAS_PHOTO = "has_photo"
	HOME_TOWN = "home_town"
	ID = "id"
	INTERESTS = "interests"
	IS_ADMIN = "is_admin"
	IS_CLOSED = "is_closed"
	IS_FAVORITE = "is_favorite"
	IS_FRIEND = "is_friend"
	IS_HIDDEN_FROM_FEED = "is_hidden_from_feed"
	IS_MEMBER = "is_member"
	IS_MESSAGES_BLOCKED = "is_messages_blocked"
	CAN_SEND_NOTIFY = "can_send_notify"
	IS_SUBSCRIBED = "is_subscribed"
	LAST_SEEN = "last_seen"
	LINKS = "links"
	LISTS = "lists"
	MAIDEN_NAME = "maiden_name"
	MAIN_ALBUM_ID = "main_album_id"
	MAIN_SECTION = "main_section"
	MARKET = "market"
	MEMBER_STATUS = "member_status"
	MEMBERS_COUNT = "members_count"
	MILITARY = "military"
	MOVIES = "movies"
	MUSIC = "music"
	NAME = "name"
	NICKNAME = "nickname"
	OCCUPATION = "occupation"
	ONLINE = "online"
	ONLINE_STATUS = "online_status"
	PERSONAL = "personal"
	PHONE = "phone"
	PHOTO_100 = "photo_100"
	PHOTO_200 = "photo_200"
	PHOTO_200_ORIG = "photo_200_orig"
	PHOTO_400_ORIG = "photo_400_orig"
	PHOTO_50 = "photo_50"
	PHOTO_ID = "photo_id"
	PHOTO_MAX = "photo_max"
	PHOTO_MAX_ORIG = "photo_max_orig"
	QUOTES = "quotes"
	RELATION = "relation"
	RELATIVES = "relatives"
	SCHOOLS = "schools"
	SCREEN_NAME = "screen_name"
	SEX = "sex"
	SITE = "site"
	START_DATE = "start_date"
	STATUS = "status"
	TIMEZONE = "timezone"
	TRENDING = "trending"
	TV = "tv"
	TYPE = "type"
	UNIVERSITIES = "universities"
	VERIFIED = "verified"
	WALL_COMMENTS = "wall_comments"
	WIKI_PAGE = "wiki_page"
	FIRST_NAME = "first_name"
	FIRST_NAME_ACC = "first_name_acc"
	FIRST_NAME_DAT = "first_name_dat"
	FIRST_NAME_GEN = "first_name_gen"
	LAST_NAME = "last_name"
	LAST_NAME_ACC = "last_name_acc"
	LAST_NAME_DAT = "last_name_dat"
	LAST_NAME_GEN = "last_name_gen"
	CAN_SUBSCRIBE_STORIES = "can_subscribe_stories"
	IS_SUBSCRIBED_STORIES = "is_subscribed_stories"
	VK_ADMIN_STATUS = "vk_admin_status"
	CAN_UPLOAD_STORY = "can_upload_story"

class BaseCity(BM):
	id:int
	title:str


class BaseCommentsInfo(BM):
	can_post:Optional[bool] = None
	can_open:Optional[bool] = None
	can_close:Optional[bool] = None
	count:Optional[int] = None
	groups_can_post:Optional[bool] = None
	donut:Optional["WallWallpostCommentsDonut"] = None


class BaseCountry(BM):
	id:int
	title:str


class BaseCropPhoto(BM):
	photo:"PhotosPhoto"
	crop:"BaseCropPhotoCrop"
	rect:"BaseCropPhotoRect"


class BaseCropPhotoCrop(BM):
	x:int
	y:int
	x2:int
	y2:int


class BaseCropPhotoRect(BM):
	x:int
	y:int
	x2:int
	y2:int


class BaseError(BM):
	error_code:int
	error_subcode:Optional[int] = None
	error_msg:Optional[str] = None
	error_text:Optional[str] = None
	request_params:Optional[list["BaseRequestParam"]] = None


class BaseGeo(BM):
	coordinates:Optional["BaseGeoCoordinates"] = None
	place:Optional["BasePlace"] = None
	showmap:Optional[int] = None
	type:Optional[str] = None


class BaseGeoCoordinates(BM):
	latitude:int
	longitude:int


class BaseGradientPoint(BM):
	color:str
	position:int


class BaseImage(BM):
	id:Optional[str] = None
	url:str
	width:int
	height:int


class BaseLikes(BM):
	count:Optional[int] = None
	user_likes:Optional[bool] = None


class BaseLikesInfo(BM):
	can_like:bool
	can_publish:Optional[bool] = None
	count:int
	user_likes:int


class BaseLink(BM):
	application:Optional["BaseLinkApplication"] = None
	button:Optional["BaseLinkButton"] = None
	caption:Optional[str] = None
	description:Optional[str] = None
	id:Optional[str] = None
	is_favorite:Optional[bool] = None
	photo:Optional["PhotosPhoto"] = None
	preview_page:Optional[str] = None
	preview_url:Optional[str] = None
	product:Optional["BaseLinkProduct"] = None
	rating:Optional["BaseLinkRating"] = None
	title:Optional[str] = None
	url:str
	target_object:Optional["LinkTargetObject"] = None
	is_external:Optional[bool] = None
	video:Optional["VideoVideo"] = None


class BaseLinkApplication(BM):
	app_id:Optional[int] = None
	store:Optional["BaseLinkApplicationStore"] = None


class BaseLinkApplicationStore(BM):
	id:Optional[int] = None
	name:Optional[str] = None


class BaseLinkButton(BM):
	action:Optional["BaseLinkButtonAction"] = None
	title:Optional[str] = None
	block_id:Optional[str] = None
	section_id:Optional[str] = None
	curator_id:Optional[int] = None
	album_id:Optional[int] = None
	owner_id:Optional[int] = None
	icon:Optional[str] = None
	style:Optional["BaseLinkButtonStyle"] = None


class BaseLinkButtonAction(BM):
	type:"BaseLinkButtonActionType"
	url:Optional[str] = None
	consume_reason:Optional[str] = None


class BaseLinkProduct(BM):
	price:"MarketPrice"
	merchant:Optional[str] = None
	orders_count:Optional[int] = None


class BaseLinkProductCategory(str):
	pass

class BaseLinkRating(BM):
	reviews_count:Optional[int] = None
	stars:Optional[int] = None


class BaseMessageError(BM):
	code:Optional[int] = None
	description:Optional[str] = None


class BaseObject(BM):
	id:int
	title:str


class BaseObjectCount(BM):
	count:Optional[int] = None


class BaseObjectWithName(BM):
	id:int
	name:str


class BasePlace(BM):
	address:Optional[str] = None
	checkins:Optional[int] = None
	city:Optional[str] = None
	country:Optional[str] = None
	created:Optional[int] = None
	icon:Optional[str] = None
	id:Optional[int] = None
	latitude:Optional[int] = None
	longitude:Optional[int] = None
	title:Optional[str] = None
	type:Optional[str] = None


class BaseRepostsInfo(BM):
	count:int
	wall_count:Optional[int] = None
	mail_count:Optional[int] = None
	user_reposted:Optional[int] = None


class BaseRequestParam(BM):
	key:Optional[str] = None
	value:Optional[str] = None


class BaseStickerAnimation(BM):
	type:Optional[str] = None
	url:Optional[str] = None


class BaseStickerNew(BM):
	sticker_id:Optional[int] = None
	product_id:Optional[int] = None
	images:Optional[list["BaseImage"]] = None
	images_with_background:Optional[list["BaseImage"]] = None
	animation_url:Optional[str] = None
	animations:Optional[list["BaseStickerAnimation"]] = None
	is_allowed:Optional[bool] = None


class BaseStickerOld(BM):
	id:Optional[int] = None
	product_id:Optional[int] = None
	width:Optional[int] = None
	height:Optional[int] = None
	photo_128:Optional[str] = None
	photo_256:Optional[str] = None
	photo_352:Optional[str] = None
	photo_512:Optional[str] = None
	photo_64:Optional[str] = None
	is_allowed:Optional[bool] = None

BaseSticker = NewType('BaseSticker', Union[BaseStickerOld, BaseStickerNew])

class BaseStickersList(BL):
    __root__:list[BaseStickerNew]

class BaseUploadServer(BM):
	upload_url:str


class BaseUserId(BM):
	user_id:Optional[int] = None




class BoardDefaultOrder(Enum):
	DESC_UPDATED = 1
	DESC_CREATED = 2
	ASC_UPDATED = -1
	ASC_CREATED = -2

class BoardTopic(BM):
	comments:Optional[int] = None
	created:Optional[int] = None
	created_by:Optional[int] = None
	id:Optional[int] = None
	is_closed:Optional[bool] = None
	is_fixed:Optional[bool] = None
	title:Optional[str] = None
	updated:Optional[int] = None
	updated_by:Optional[int] = None
	first_comment:Optional[str] = None
	last_comment:Optional[str] = None


class BoardTopicComment(BM):
	attachments:Optional[list["WallCommentAttachment"]] = None
	date:int
	from_id:int
	id:int
	real_offset:Optional[int] = None
	text:str
	can_edit:Optional[bool] = None
	likes:Optional["BaseLikesInfo"] = None




class CallbackGroupJoinType(Enum):
	JOIN = "join"
	UNSURE = "unsure"
	ACCEPTED = "accepted"
	APPROVED = "approved"
	REQUEST = "request"

class CallbackGroupMarket(Enum):
	DISABLED = 0
	OPEN = 1

class CallbackGroupOfficerRole(Enum):
	NONE = 0
	MODERATOR = 1
	EDITOR = 2
	ADMINISTRATOR = 3

class CallbackType(Enum):
	AUDIO_NEW = "audio_new"
	BOARD_POST_NEW = "board_post_new"
	BOARD_POST_EDIT = "board_post_edit"
	BOARD_POST_RESTORE = "board_post_restore"
	BOARD_POST_DELETE = "board_post_delete"
	CONFIRMATION = "confirmation"
	GROUP_LEAVE = "group_leave"
	GROUP_JOIN = "group_join"
	GROUP_CHANGE_PHOTO = "group_change_photo"
	GROUP_CHANGE_SETTINGS = "group_change_settings"
	GROUP_OFFICERS_EDIT = "group_officers_edit"
	LEAD_FORMS_NEW = "lead_forms_new"
	MARKET_COMMENT_NEW = "market_comment_new"
	MARKET_COMMENT_DELETE = "market_comment_delete"
	MARKET_COMMENT_EDIT = "market_comment_edit"
	MARKET_COMMENT_RESTORE = "market_comment_restore"
	MESSAGE_NEW = "message_new"
	MESSAGE_REPLY = "message_reply"
	MESSAGE_EDIT = "message_edit"
	MESSAGE_ALLOW = "message_allow"
	MESSAGE_DENY = "message_deny"
	MESSAGE_READ = "message_read"
	MESSAGE_TYPING_STATE = "message_typing_state"
	MESSAGES_EDIT = "messages_edit"
	PHOTO_NEW = "photo_new"
	PHOTO_COMMENT_NEW = "photo_comment_new"
	PHOTO_COMMENT_DELETE = "photo_comment_delete"
	PHOTO_COMMENT_EDIT = "photo_comment_edit"
	PHOTO_COMMENT_RESTORE = "photo_comment_restore"
	POLL_VOTE_NEW = "poll_vote_new"
	USER_BLOCK = "user_block"
	USER_UNBLOCK = "user_unblock"
	VIDEO_NEW = "video_new"
	VIDEO_COMMENT_NEW = "video_comment_new"
	VIDEO_COMMENT_DELETE = "video_comment_delete"
	VIDEO_COMMENT_EDIT = "video_comment_edit"
	VIDEO_COMMENT_RESTORE = "video_comment_restore"
	WALL_POST_NEW = "wall_post_new"
	WALL_REPLY_NEW = "wall_reply_new"
	WALL_REPLY_EDIT = "wall_reply_edit"
	WALL_REPLY_DELETE = "wall_reply_delete"
	WALL_REPLY_RESTORE = "wall_reply_restore"
	WALL_REPOST = "wall_repost"

class CallbackBase(BM):
	type:str
	group_id:int
	event_id:str
	secret:Optional[str] = None


class CallbackBoardPostDelete(BM):
	topic_owner_id:int
	topic_id:int
	id:int


class CallbackDonutMoneyWithdraw(BM):
	amount:int
	amount_without_fee:int


class CallbackDonutMoneyWithdrawError(BM):
	reason:str


class CallbackDonutSubscriptionCancelled(BM):
	user_id:Optional[int] = None


class CallbackDonutSubscriptionCreate(BM):
	user_id:Optional[int] = None
	amount:int
	amount_without_fee:int


class CallbackDonutSubscriptionExpired(BM):
	user_id:Optional[int] = None


class CallbackDonutSubscriptionPriceChanged(BM):
	user_id:Optional[int] = None
	amount_old:int
	amount_new:int
	amount_diff:Optional[int] = None
	amount_diff_without_fee:Optional[int] = None


class CallbackDonutSubscriptionProlonged(BM):
	user_id:Optional[int] = None
	amount:int
	amount_without_fee:int


class CallbackGroupChangePhoto(BM):
	user_id:int
	photo:"PhotosPhoto"


class CallbackGroupChangeSettings(BM):
	user_id:int
	self:bool


class CallbackGroupJoin(BM):
	user_id:int
	join_type:"CallbackGroupJoinType"


class CallbackGroupLeave(BM):
	user_id:Optional[int] = None
	self:Optional[bool] = None


class CallbackGroupOfficersEdit(BM):
	admin_id:int
	user_id:int
	level_old:"CallbackGroupOfficerRole"
	level_new:"CallbackGroupOfficerRole"


class CallbackGroupSettingsChanges(BM):
	title:Optional[str] = None
	description:Optional[str] = None
	access:Optional["GroupsGroupIsClosed"] = None
	screen_name:Optional[str] = None
	public_category:Optional[int] = None
	public_subcategory:Optional[int] = None
	age_limits:Optional["GroupsGroupFullAgeLimits"] = None
	website:Optional[str] = None
	enable_status_default:Optional["GroupsGroupWall"] = None
	enable_audio:Optional["GroupsGroupAudio"] = None
	enable_video:Optional["GroupsGroupVideo"] = None
	enable_photo:Optional["GroupsGroupPhotos"] = None
	enable_market:Optional["CallbackGroupMarket"] = None


class CallbackLikeAddRemove(BM):
	liker_id:int
	object_type:str
	object_owner_id:int
	object_id:int
	post_id:int
	thread_reply_id:Optional[int] = None


class CallbackMarketComment(BM):
	id:int
	from_id:int
	date:int
	text:Optional[str] = None
	market_owner_id:Optional[int] = None
	photo_id:Optional[int] = None


class CallbackMarketCommentDelete(BM):
	owner_id:int
	id:int
	user_id:int
	item_id:int


class CallbackMessageAllowObject(BM):
	user_id:int
	key:str


class CallbackMessageDeny(BM):
	user_id:int


class CallbackMessageObject(BM):
	client_info:Optional["ClientInfoForBots"] = None
	message:Optional["MessagesMessage"] = None


class CallbackPhotoComment(BM):
	id:int
	from_id:int
	date:int
	text:str
	photo_owner_id:int


class CallbackPhotoCommentDelete(BM):
	id:int
	owner_id:int
	user_id:int
	photo_id:int


class CallbackPollVoteNew(BM):
	owner_id:int
	poll_id:int
	option_id:int
	user_id:int


class CallbackQrScan(BM):
	user_id:int
	data:str
	type:str
	subtype:str
	reread:bool


class CallbackUserBlock(BM):
	admin_id:int
	user_id:int
	unblock_date:int
	reason:int
	comment:Optional[str] = None


class CallbackUserUnblock(BM):
	admin_id:int
	user_id:int
	by_end_date:int


class CallbackVideoComment(BM):
	id:int
	from_id:int
	date:int
	text:str
	video_owner_id:int


class CallbackVideoCommentDelete(BM):
	id:int
	owner_id:int
	user_id:int
	video_id:int


class CallbackWallCommentDelete(BM):
	owner_id:int
	id:int
	user_id:int
	post_id:int




class CallsEndState(Enum):
	CANCELED_BY_INITIATOR = "canceled_by_initiator"
	CANCELED_BY_RECEIVER = "canceled_by_receiver"
	REACHED = "reached"

class CallsCall(BM):
	duration:Optional[int] = None
	initiator_id:int
	receiver_id:int
	state:"CallsEndState"
	time:int
	video:Optional[bool] = None
	participants:Optional["CallsParticipants"] = None


class CallsParticipants(BM):
	_list:Optional[list[int]] = None
	count:Optional[int] = None




class ClientInfoForBots(BM):
	button_actions:Optional[list["MessagesTemplateActionTypeNames"]] = None
	keyboard:Optional[bool] = None
	inline_keyboard:Optional[bool] = None
	carousel:Optional[bool] = None
	lang_id:Optional[int] = None




class CommentThread(BM):
	count:int
	items:Optional[list["WallWallComment"]] = None
	can_post:Optional[bool] = None
	show_reply_button:Optional[bool] = None
	groups_can_post:Optional[bool] = None




class DatabaseCityById(BaseObject):
	pass

class DatabaseFaculty(BM):
	id:Optional[int] = None
	title:Optional[str] = None


class DatabaseRegion(BM):
	id:Optional[int] = None
	title:Optional[str] = None


class DatabaseSchool(BM):
	id:Optional[int] = None
	title:Optional[str] = None


class DatabaseStation(BM):
	city_id:Optional[int] = None
	color:Optional[str] = None
	id:int
	name:str


class DatabaseUniversity(BM):
	id:Optional[int] = None
	title:Optional[str] = None




class DocsDocAttachmentType(Enum):
	DOC = "doc"
	GRAFFITI = "graffiti"
	AUDIO_MESSAGE = "audio_message"

class DocsDoc(BM):
	id:int
	owner_id:int
	title:str
	size:int
	ext:str
	url:Optional[str] = None
	date:int
	type:int
	preview:Optional["DocsDocPreview"] = None
	is_licensed:Optional[bool] = None
	access_key:Optional[str] = None
	tags:Optional[list[str]] = None


class DocsDocPreview(BM):
	audio_msg:Optional["DocsDocPreviewAudioMsg"] = None
	graffiti:Optional["DocsDocPreviewGraffiti"] = None
	photo:Optional["DocsDocPreviewPhoto"] = None
	video:Optional["DocsDocPreviewVideo"] = None


class DocsDocPreviewAudioMsg(BM):
	duration:int
	link_mp3:str
	link_ogg:str
	waveform:list[int]


class DocsDocPreviewGraffiti(BM):
	src:str
	width:int
	height:int


class DocsDocPreviewPhoto(BM):
	sizes:Optional[list["DocsDocPreviewPhotoSizes"]] = None


class DocsDocPreviewPhotoSizes(BM):
	src:str
	width:int
	height:int
	type:"PhotosPhotoSizesType"


class DocsDocPreviewVideo(BM):
	src:str
	width:int
	height:int
	file_size:int


class DocsDocTypes(BM):
	id:int
	name:str
	count:int




class DonutDonatorSubscriptionInfo(BM):
	owner_id:int
	next_payment_date:int
	amount:int
	status:str




class EventsEventAttach(BM):
	address:Optional[str] = None
	button_text:str
	friends:list[int]
	id:int
	is_favorite:bool
	member_status:Optional["GroupsGroupFullMemberStatus"] = None
	text:str
	time:Optional[int] = None




class FaveBookmarkType(Enum):
	POST = "post"
	VIDEO = "video"
	PRODUCT = "product"
	ARTICLE = "article"
	LINK = "link"

class FavePageType(Enum):
	USER = "user"
	GROUP = "group"
	HINTS = "hints"

class FaveBookmark(BM):
	added_date:int
	link:Optional["BaseLink"] = None
	post:Optional["WallWallpostFull"] = None
	product:Optional["MarketMarketItem"] = None
	seen:bool
	tags:list["FaveTag"]
	type:"FaveBookmarkType"
	video:Optional["VideoVideoFull"] = None


class FavePage(BM):
	description:str
	group:Optional["GroupsGroupFull"] = None
	tags:list["FaveTag"]
	type:"FavePageType"
	updated_date:Optional[int] = None
	user:Optional["UsersUserFull"] = None


class FaveTag(BM):
	id:Optional[int] = None
	name:Optional[str] = None




class FriendsFriendStatusStatus(Enum):
	NOT_A_FRIEND = 0
	OUTCOMING_REQUEST = 1
	INCOMING_REQUEST = 2
	IS_FRIEND = 3

class FriendsFriendStatus(BM):
	friend_status:"FriendsFriendStatusStatus"
	sign:Optional[str] = None
	user_id:int


class FriendsFriendsList(BM):
	id:int
	name:str


class FriendsMutualFriend(BM):
	common_count:Optional[int] = None
	common_friends:Optional[list[int]] = None
	id:Optional[int] = None


class FriendsRequests(BM):
	_from:Optional[str] = None
	mutual:Optional["FriendsRequestsMutual"] = None
	user_id:Optional[int] = None


class FriendsRequestsMutual(BM):
	count:Optional[int] = None
	users:Optional[list[int]] = None


class FriendsRequestsXtrMessage(BM):
	_from:Optional[str] = None
	message:Optional[str] = None
	mutual:Optional["FriendsRequestsMutual"] = None
	user_id:Optional[int] = None




class GiftsGiftPrivacy(Enum):
	NAME_AND_MESSAGE_FOR_ALL = 0
	NAME_FOR_ALL = 1
	NAME_AND_MESSAGE_FOR_RECIPIENT_ONLY = 2

class GiftsGift(BM):
	date:Optional[int] = None
	from_id:Optional[int] = None
	gift:Optional["GiftsLayout"] = None
	gift_hash:Optional[str] = None
	id:Optional[int] = None
	message:Optional[str] = None
	privacy:Optional["GiftsGiftPrivacy"] = None


class GiftsLayout(BM):
	id:Optional[int] = None
	thumb_512:Optional[str] = None
	thumb_256:Optional[str] = None
	thumb_48:Optional[str] = None
	thumb_96:Optional[str] = None
	stickers_product_id:Optional[int] = None
	is_stickers_style:Optional[bool] = None
	build_id:Optional[str] = None
	keywords:Optional[str] = None




class GroupsAddressWorkInfoStatus(Enum):
	NO_INFORMATION = "no_information"
	TEMPORARILY_CLOSED = "temporarily_closed"
	ALWAYS_OPENED = "always_opened"
	TIMETABLE = "timetable"
	FOREVER_CLOSED = "forever_closed"

class GroupsBanInfoReason(Enum):
	OTHER = 0
	SPAM = 1
	VERBAL_ABUSE = 2
	STRONG_LANGUAGE = 3
	FLOOD = 4

class GroupsFields(Enum):
	MARKET = "market"
	MEMBER_STATUS = "member_status"
	IS_FAVORITE = "is_favorite"
	IS_SUBSCRIBED = "is_subscribed"
	IS_SUBSCRIBED_PODCASTS = "is_subscribed_podcasts"
	CAN_SUBSCRIBE_PODCASTS = "can_subscribe_podcasts"
	CITY = "city"
	COUNTRY = "country"
	VERIFIED = "verified"
	DESCRIPTION = "description"
	WIKI_PAGE = "wiki_page"
	MEMBERS_COUNT = "members_count"
	REQUESTS_COUNT = "requests_count"
	COUNTERS = "counters"
	COVER = "cover"
	CAN_POST = "can_post"
	CAN_SUGGEST = "can_suggest"
	CAN_UPLOAD_STORY = "can_upload_story"
	CAN_UPLOAD_DOC = "can_upload_doc"
	CAN_UPLOAD_VIDEO = "can_upload_video"
	CAN_UPLOAD_CLIP = "can_upload_clip"
	CAN_SEE_ALL_POSTS = "can_see_all_posts"
	CAN_CREATE_TOPIC = "can_create_topic"
	CROP_PHOTO = "crop_photo"
	ACTIVITY = "activity"
	FIXED_POST = "fixed_post"
	HAS_PHOTO = "has_photo"
	STATUS = "status"
	MAIN_ALBUM_ID = "main_album_id"
	LINKS = "links"
	CONTACTS = "contacts"
	SITE = "site"
	MAIN_SECTION = "main_section"
	SECONDARY_SECTION = "secondary_section"
	WALL = "wall"
	TRENDING = "trending"
	CAN_MESSAGE = "can_message"
	IS_MARKET_CART_ENABLED = "is_market_cart_enabled"
	IS_MESSAGES_BLOCKED = "is_messages_blocked"
	CAN_SEND_NOTIFY = "can_send_notify"
	HAS_GROUP_CHANNEL = "has_group_channel"
	GROUP_CHANNEL = "group_channel"
	ONLINE_STATUS = "online_status"
	START_DATE = "start_date"
	FINISH_DATE = "finish_date"
	AGE_LIMITS = "age_limits"
	BAN_INFO = "ban_info"
	ACTION_BUTTON = "action_button"
	AUTHOR_ID = "author_id"
	PHONE = "phone"
	HAS_MARKET_APP = "has_market_app"
	ADDRESSES = "addresses"
	LIVE_COVERS = "live_covers"
	IS_ADULT = "is_adult"
	IS_HIDDEN_FROM_FEED = "is_hidden_from_feed"
	CAN_SUBSCRIBE_POSTS = "can_subscribe_posts"
	WARNING_NOTIFICATION = "warning_notification"
	MSG_PUSH_ALLOWED = "msg_push_allowed"
	STORIES_ARCHIVE_COUNT = "stories_archive_count"
	VIDEO_LIVE_LEVEL = "video_live_level"
	VIDEO_LIVE_COUNT = "video_live_count"
	CLIPS_COUNT = "clips_count"
	HAS_UNSEEN_STORIES = "has_unseen_stories"
	IS_BUSINESS = "is_business"
	TEXTLIVES_COUNT = "textlives_count"
	MEMBERS_COUNT_TEXT = "members_count_text"

class GroupsFilter(Enum):
	ADMIN = "admin"
	EDITOR = "editor"
	MODER = "moder"
	ADVERTISER = "advertiser"
	GROUPS = "groups"
	PUBLICS = "publics"
	EVENTS = "events"
	HAS_ADDRESSES = "has_addresses"

class GroupsGroupAccess(Enum):
	OPEN = 0
	CLOSED = 1
	PRIVATE = 2

class GroupsGroupAdminLevel(Enum):
	MODERATOR = 1
	EDITOR = 2
	ADMINISTRATOR = 3

class GroupsGroupAgeLimits(Enum):
	UNLIMITED = 1
	_16_PLUS = 2
	_18_PLUS = 3

class GroupsGroupAudio(Enum):
	DISABLED = 0
	OPEN = 1
	LIMITED = 2

class GroupsGroupDocs(Enum):
	DISABLED = 0
	OPEN = 1
	LIMITED = 2

class GroupsGroupFullAgeLimits(Enum):
	NO = 1
	OVER_16 = 2
	OVER_18 = 3

class GroupsGroupFullMemberStatus(Enum):
	NOT_A_MEMBER = 0
	MEMBER = 1
	NOT_SURE = 2
	DECLINED = 3
	HAS_SENT_A_REQUEST = 4
	INVITED = 5

class GroupsGroupFullSection(Enum):
	NONE = 0
	PHOTOS = 1
	TOPICS = 2
	AUDIOS = 3
	VIDEOS = 4
	MARKET = 5
	STORIES = 6
	APPS = 7
	FOLLOWERS = 8
	LINKS = 9
	EVENTS = 10
	PLACES = 11
	CONTACTS = 12
	APP_BTNS = 13
	DOCS = 14
	EVENT_COUNTERS = 15
	GROUP_MESSAGES = 16
	ALBUMS = 24
	CATEGORIES = 26
	ADMIN_HELP = 27
	APP_WIDGET = 31
	PUBLIC_HELP = 32
	HS_DONATION_APP = 33
	HS_MARKET_APP = 34
	ADDRESSES = 35
	ARTIST_PAGE = 36
	PODCAST = 37
	ARTICLES = 39
	ADMIN_TIPS = 40
	MENU = 41
	FIXED_POST = 42
	CHATS = 43
	EVERGREEN_NOTICE = 44
	MUSICIANS = 45
	NARRATIVES = 46
	DONUT_DONATE = 47
	CLIPS = 48
	MARKET_CART = 49
	CURATORS = 50
	MARKET_SERVICES = 51
	CLASSIFIEDS = 53
	TEXTLIVES = 54
	DONUT_FOR_DONS = 55
	BADGES = 57
	CHATS_CREATION = 58

class GroupsGroupIsClosed(Enum):
	OPEN = 0
	CLOSED = 1
	PRIVATE = 2

class GroupsGroupMarketCurrency(Enum):
	RUSSIAN_RUBLES = 643
	UKRAINIAN_HRYVNIA = 980
	KAZAKH_TENGE = 398
	EURO = 978
	US_DOLLARS = 840

class GroupsGroupPhotos(Enum):
	DISABLED = 0
	OPEN = 1
	LIMITED = 2

class GroupsGroupRole(Enum):
	MODERATOR = "moderator"
	EDITOR = "editor"
	ADMINISTRATOR = "administrator"
	ADVERTISER = "advertiser"

class GroupsGroupSubject(Enum):
	AUTO = 1
	ACTIVITY_HOLIDAYS = 2
	BUSINESS = 3
	PETS = 4
	HEALTH = 5
	DATING_AND_COMMUNICATION = 6
	GAMES = 7
	IT = 8
	CINEMA = 9
	BEAUTY_AND_FASHION = 10
	COOKING = 11
	ART_AND_CULTURE = 12
	LITERATURE = 13
	MOBILE_SERVICES_AND_INTERNET = 14
	MUSIC = 15
	SCIENCE_AND_TECHNOLOGY = 16
	REAL_ESTATE = 17
	NEWS_AND_MEDIA = 18
	SECURITY = 19
	EDUCATION = 20
	HOME_AND_RENOVATIONS = 21
	POLITICS = 22
	FOOD = 23
	INDUSTRY = 24
	TRAVEL = 25
	WORK = 26
	ENTERTAINMENT = 27
	RELIGION = 28
	FAMILY = 29
	SPORTS = 30
	INSURANCE = 31
	TELEVISION = 32
	GOODS_AND_SERVICES = 33
	HOBBIES = 34
	FINANCE = 35
	PHOTO = 36
	ESOTERICS = 37
	ELECTRONICS_AND_APPLIANCES = 38
	EROTIC = 39
	HUMOR = 40
	SOCIETY_HUMANITIES = 41
	DESIGN_AND_GRAPHICS = 42

class GroupsGroupSuggestedPrivacy(Enum):
	NONE = 0
	ALL = 1
	SUBSCRIBERS = 2

class GroupsGroupTopics(Enum):
	DISABLED = 0
	OPEN = 1
	LIMITED = 2

class GroupsGroupType(Enum):
	GROUP = "group"
	PAGE = "page"
	EVENT = "event"

class GroupsGroupVideo(Enum):
	DISABLED = 0
	OPEN = 1
	LIMITED = 2

class GroupsGroupWall(Enum):
	DISABLED = 0
	OPEN = 1
	LIMITED = 2
	CLOSED = 3

class GroupsGroupWiki(Enum):
	DISABLED = 0
	OPEN = 1
	LIMITED = 2

class GroupsMarketState(Enum):
	NONE = "none"
	BASIC = "basic"
	ADVANCED = "advanced"

class GroupsMemberRolePermission(Enum):
	ADS = "ads"

class GroupsMemberRoleStatus(Enum):
	MODERATOR = "moderator"
	EDITOR = "editor"
	ADMINISTRATOR = "administrator"
	CREATOR = "creator"
	ADVERTISER = "advertiser"

class GroupsOnlineStatusType(Enum):
	NONE = "none"
	ONLINE = "online"
	ANSWER_MARK = "answer_mark"

class GroupsOwnerXtrBanInfoType(Enum):
	GROUP = "group"
	PROFILE = "profile"

class GroupsRoleOptions(Enum):
	MODERATOR = "moderator"
	EDITOR = "editor"
	ADMINISTRATOR = "administrator"
	CREATOR = "creator"

class GroupsAddress(BM):
	additional_address:Optional[str] = None
	address:Optional[str] = None
	city_id:Optional[int] = None
	country_id:Optional[int] = None
	distance:Optional[int] = None
	id:int
	latitude:Optional[int] = None
	longitude:Optional[int] = None
	metro_station_id:Optional[int] = None
	phone:Optional[str] = None
	time_offset:Optional[int] = None
	timetable:Optional["GroupsAddressTimetable"] = None
	title:Optional[str] = None
	work_info_status:Optional["GroupsAddressWorkInfoStatus"] = None
	place_id:Optional[int] = None


class GroupsAddressTimetable(BM):
	fri:Optional["GroupsAddressTimetableDay"] = None
	mon:Optional["GroupsAddressTimetableDay"] = None
	sat:Optional["GroupsAddressTimetableDay"] = None
	sun:Optional["GroupsAddressTimetableDay"] = None
	thu:Optional["GroupsAddressTimetableDay"] = None
	tue:Optional["GroupsAddressTimetableDay"] = None
	wed:Optional["GroupsAddressTimetableDay"] = None


class GroupsAddressTimetableDay(BM):
	break_close_time:Optional[int] = None
	break_open_time:Optional[int] = None
	close_time:int
	open_time:int


class GroupsAddressesInfo(BM):
	is_enabled:bool
	main_address_id:Optional[int] = None


class GroupsBanInfo(BM):
	admin_id:Optional[int] = None
	comment:Optional[str] = None
	comment_visible:Optional[bool] = None
	is_closed:Optional[bool] = None
	date:Optional[int] = None
	end_date:Optional[int] = None
	reason:Optional["GroupsBanInfoReason"] = None


class GroupsCallbackServer(BM):
	id:int
	title:str
	creator_id:int
	url:str
	secret_key:str
	status:str


class GroupsCallbackSettings(BM):
	api_version:Optional[str] = None
	events:Optional["GroupsLongPollEvents"] = None


class GroupsContactsItem(BM):
	user_id:Optional[int] = None
	desc:Optional[str] = None
	phone:Optional[str] = None
	email:Optional[str] = None


class GroupsCountersGroup(BM):
	addresses:Optional[int] = None
	albums:Optional[int] = None
	audios:Optional[int] = None
	audio_playlists:Optional[int] = None
	docs:Optional[int] = None
	market:Optional[int] = None
	photos:Optional[int] = None
	topics:Optional[int] = None
	videos:Optional[int] = None
	market_services:Optional[int] = None
	podcasts:Optional[int] = None
	articles:Optional[int] = None
	narratives:Optional[int] = None
	clips:Optional[int] = None
	clips_followers:Optional[int] = None


class GroupsCover(BM):
	enabled:bool
	images:Optional[list["BaseImage"]] = None


class GroupsGroup(BM):
	id:int
	name:Optional[str] = None
	screen_name:Optional[str] = None
	is_closed:Optional["GroupsGroupIsClosed"] = None
	type:Optional["GroupsGroupType"] = None
	is_admin:Optional[bool] = None
	admin_level:Optional["GroupsGroupAdminLevel"] = None
	is_member:Optional[bool] = None
	is_advertiser:Optional[bool] = None
	start_date:Optional[int] = None
	finish_date:Optional[int] = None
	deactivated:Optional[str] = None
	photo_50:Optional[str] = None
	photo_100:Optional[str] = None
	photo_200:Optional[str] = None
	photo_200_orig:Optional[str] = None
	photo_400:Optional[str] = None
	photo_400_orig:Optional[str] = None
	photo_max:Optional[str] = None
	photo_max_orig:Optional[str] = None
	est_date:Optional[str] = None
	public_date_label:Optional[str] = None
	photo_max_size:Optional["GroupsPhotoSize"] = None
	is_video_live_notifications_blocked:Optional[bool] = None
	video_live:Optional["VideoLiveInfo"] = None


class GroupsGroupAttach(BM):
	id:int
	text:str
	status:str
	size:int
	is_favorite:bool


class GroupsGroupBanInfo(BM):
	comment:Optional[str] = None
	end_date:Optional[int] = None
	reason:Optional["GroupsBanInfoReason"] = None


class GroupsGroupCategory(BM):
	id:int
	name:str
	subcategories:Optional[list["BaseObjectWithName"]] = None


class GroupsGroupCategoryFull(BM):
	id:int
	name:str
	page_count:int
	page_previews:list["GroupsGroup"]
	subcategories:Optional[list["GroupsGroupCategory"]] = None


class GroupsGroupCategoryType(BM):
	id:int
	name:str


class GroupsGroupPublicCategoryList(BM):
	id:Optional[int] = None
	name:Optional[str] = None
	subcategories:Optional[list["GroupsGroupCategoryType"]] = None


class GroupsGroupTag(BM):
	id:int
	name:str
	color:str
	uses:Optional[int] = None


class GroupsGroupsArray(BM):
	count:int
	items:list[int]


class GroupsLinksItem(BM):
	name:Optional[str] = None
	desc:Optional[str] = None
	edit_title:Optional[bool] = None
	id:Optional[int] = None
	photo_100:Optional[str] = None
	photo_50:Optional[str] = None
	url:Optional[str] = None
	image_processing:Optional[bool] = None


class GroupsLiveCovers(BM):
	is_enabled:bool
	is_scalable:Optional[bool] = None
	story_ids:Optional[list[str]] = None


class GroupsLongPollEvents(BM):
	audio_new:bool
	board_post_delete:bool
	board_post_edit:bool
	board_post_new:bool
	board_post_restore:bool
	group_change_photo:bool
	group_change_settings:bool
	group_join:bool
	group_leave:bool
	group_officers_edit:bool
	lead_forms_new:Optional[bool] = None
	market_comment_delete:bool
	market_comment_edit:bool
	market_comment_new:bool
	market_comment_restore:bool
	market_order_new:Optional[bool] = None
	market_order_edit:Optional[bool] = None
	message_allow:bool
	message_deny:bool
	message_new:bool
	message_read:bool
	message_reply:bool
	message_typing_state:bool
	message_edit:bool
	photo_comment_delete:bool
	photo_comment_edit:bool
	photo_comment_new:bool
	photo_comment_restore:bool
	photo_new:bool
	poll_vote_new:bool
	user_block:bool
	user_unblock:bool
	video_comment_delete:bool
	video_comment_edit:bool
	video_comment_new:bool
	video_comment_restore:bool
	video_new:bool
	wall_post_new:bool
	wall_reply_delete:bool
	wall_reply_edit:bool
	wall_reply_new:bool
	wall_reply_restore:bool
	wall_repost:bool
	donut_subscription_create:bool
	donut_subscription_prolonged:bool
	donut_subscription_cancelled:bool
	donut_subscription_expired:bool
	donut_subscription_price_changed:bool
	donut_money_withdraw:bool
	donut_money_withdraw_error:bool


class GroupsLongPollServer(BM):
	key:str
	server:str
	ts:str


class GroupsLongPollSettings(BM):
	api_version:Optional[str] = None
	events:"GroupsLongPollEvents"
	is_enabled:bool


class GroupsMarketInfo(BM):
	type:Optional[str] = None
	contact_id:Optional[int] = None
	currency:Optional["MarketCurrency"] = None
	currency_text:Optional[str] = None
	enabled:Optional[bool] = None
	main_album_id:Optional[int] = None
	price_max:Optional[str] = None
	price_min:Optional[str] = None
	min_order_price:Optional["MarketPrice"] = None


class GroupsMemberRole(BM):
	id:int
	permissions:Optional[list["GroupsMemberRolePermission"]] = None
	role:Optional["GroupsMemberRoleStatus"] = None


class GroupsMemberStatus(BM):
	member:bool
	user_id:int


class GroupsMemberStatusFull(BM):
	can_invite:Optional[bool] = None
	can_recall:Optional[bool] = None
	invitation:Optional[bool] = None
	member:bool
	request:Optional[bool] = None
	user_id:int


class GroupsOnlineStatus(BM):
	minutes:Optional[int] = None
	status:"GroupsOnlineStatusType"


class GroupsOwnerXtrBanInfo(BM):
	ban_info:Optional["GroupsBanInfo"] = None
	group:Optional["GroupsGroup"] = None
	profile:Optional["UsersUser"] = None
	type:Optional["GroupsOwnerXtrBanInfoType"] = None


class GroupsBannedItem(GroupsOwnerXtrBanInfo):
	pass

class GroupsPhotoSize(BM):
	height:int
	width:int


class GroupsSectionsListItem(BL):
    __root__:list[int|str]

class GroupsSettingsTwitter(BM):
	status:str
	name:Optional[str] = None


class GroupsSubjectItem(BM):
	id:int
	name:str


class GroupsTokenPermissionSetting(BM):
	name:str
	setting:int




class LeadFormsAnswer(BM):
	key:str
	answer:Union["LeadFormsAnswerItem",list["LeadFormsAnswerItem"]]


class LeadFormsAnswerItem(BM):
	key:Optional[str] = None
	value:str


class LeadFormsForm(BM):
	form_id:int
	group_id:int
	photo:Optional[str] = None
	name:Optional[str] = None
	title:Optional[str] = None
	description:Optional[str] = None
	confirmation:Optional[str] = None
	site_link_url:Optional[str] = None
	policy_link_url:Optional[str] = None
	questions:Optional[list["LeadFormsQuestionItem"]] = None
	active:Optional[bool] = None
	leads_count:int
	pixel_code:Optional[str] = None
	once_per_user:Optional[int] = None
	notify_admins:Optional[str] = None
	notify_emails:Optional[str] = None
	url:str


class LeadFormsLead(BM):
	lead_id:int
	user_id:int
	date:int
	answers:list["LeadFormsAnswer"]
	ad_id:Optional[int] = None


class LeadFormsQuestionItem(BM):
	key:str
	type:str
	label:Optional[str] = None
	options:Optional[list["LeadFormsQuestionItemOption"]] = None


class LeadFormsQuestionItemOption(BM):
	key:Optional[str] = None
	label:str




class LikesType(Enum):
	POST = "post"
	COMMENT = "comment"
	PHOTO = "photo"
	AUDIO = "audio"
	VIDEO = "video"
	NOTE = "note"
	MARKET = "market"
	PHOTO_COMMENT = "photo_comment"
	VIDEO_COMMENT = "video_comment"
	TOPIC_COMMENT = "topic_comment"
	MARKET_COMMENT = "market_comment"
	SITEPAGE = "sitepage"
	TEXTPOST = "textpost"



class LinkTargetObject(BM):
	type:Optional[str] = None
	owner_id:Optional[int] = None
	item_id:Optional[int] = None




class MarketMarketItemAvailability(Enum):
	AVAILABLE = 0
	REMOVED = 1
	UNAVAILABLE = 2

class MarketServicesViewType(Enum):
	CARDS = 1
	ROWS = 2

class MarketCurrency(BM):
	id:int
	name:str
	title:str


class MarketMarketAlbum(BM):
	id:int
	owner_id:int
	title:str
	count:int
	is_main:Optional[bool] = None
	is_hidden:Optional[bool] = None
	photo:Optional["PhotosPhoto"] = None
	updated_time:int


class MarketMarketCategoryNested(BM):
	id:int
	name:str
	parent:Optional["MarketMarketCategoryNested"] = None


class MarketMarketCategoryOld(BM):
	id:int
	name:str
	section:"MarketSection"


class MarketMarketCategoryTree(BM):
	id:int
	name:str
	children:Optional[list["MarketMarketCategoryTree"]] = None


class MarketMarketItem(BM):
	access_key:Optional[str] = None
	availability:"MarketMarketItemAvailability"
	button_title:Optional[str] = None
	category:"MarketMarketCategory"
	date:Optional[int] = None
	description:str
	external_id:Optional[str] = None
	id:int
	is_favorite:Optional[bool] = None
	owner_id:int
	price:"MarketPrice"
	thumb_photo:Optional[str] = None
	title:str
	url:Optional[str] = None
	variants_grouping_id:Optional[int] = None
	is_main_variant:Optional[bool] = None
	sku:Optional[str] = None


class MarketOrder(BM):
	id:int
	group_id:int
	user_id:int
	display_order_id:Optional[str] = None
	date:int
	status:int
	items_count:int
	track_number:Optional[str] = None
	track_link:Optional[str] = None
	comment:Optional[str] = None
	address:Optional[str] = None
	merchant_comment:Optional[str] = None
	weight:Optional[int] = None
	total_price:"MarketPrice"
	preview_order_items:Optional[list["MarketOrderItem"]] = None
	cancel_info:Optional["BaseLink"] = None


class MarketOrderItem(BM):
	owner_id:int
	item_id:int
	price:"MarketPrice"
	quantity:int
	item:"MarketMarketItem"
	title:Optional[str] = None
	photo:Optional["PhotosPhoto"] = None
	variants:Optional[list[str]] = None


class MarketPrice(BM):
	amount:str
	currency:"MarketCurrency"
	discount_rate:Optional[int] = None
	old_amount:Optional[str] = None
	text:str
	old_amount_text:Optional[str] = None


class MarketSection(BM):
	id:int
	name:str


class MarketMarketCategory(MarketMarketCategoryOld):
	pass



class MessagesChatSettingsState(Enum):
	_IN = "in"
	KICKED = "kicked"
	LEFT = "left"

class MessagesConversationPeerType(Enum):
	CHAT = "chat"
	EMAIL = "email"
	USER = "user"
	GROUP = "group"

class MessagesHistoryMessageAttachmentType(Enum):
	PHOTO = "photo"
	VIDEO = "video"
	AUDIO = "audio"
	DOC = "doc"
	LINK = "link"
	MARKET = "market"
	WALL = "wall"
	SHARE = "share"
	GRAFFITI = "graffiti"
	AUDIO_MESSAGE = "audio_message"

class MessagesMessageActionStatus(Enum):
	CHAT_PHOTO_UPDATE = "chat_photo_update"
	CHAT_PHOTO_REMOVE = "chat_photo_remove"
	CHAT_CREATE = "chat_create"
	CHAT_TITLE_UPDATE = "chat_title_update"
	CHAT_INVITE_USER = "chat_invite_user"
	CHAT_KICK_USER = "chat_kick_user"
	CHAT_PIN_MESSAGE = "chat_pin_message"
	CHAT_UNPIN_MESSAGE = "chat_unpin_message"
	CHAT_INVITE_USER_BY_LINK = "chat_invite_user_by_link"
	CHAT_INVITE_USER_BY_MESSAGE_REQUEST = "chat_invite_user_by_message_request"
	CHAT_SCREENSHOT = "chat_screenshot"

class MessagesMessageAttachmentType(Enum):
	PHOTO = "photo"
	AUDIO = "audio"
	VIDEO = "video"
	DOC = "doc"
	LINK = "link"
	MARKET = "market"
	MARKET_ALBUM = "market_album"
	GIFT = "gift"
	STICKER = "sticker"
	WALL = "wall"
	WALL_REPLY = "wall_reply"
	ARTICLE = "article"
	POLL = "poll"
	CALL = "call"
	GRAFFITI = "graffiti"
	AUDIO_MESSAGE = "audio_message"

class MessagesTemplateActionTypeNames(Enum):
	TEXT = "text"
	START = "start"
	LOCATION = "location"
	VKPAY = "vkpay"
	OPEN_APP = "open_app"
	OPEN_PHOTO = "open_photo"
	OPEN_LINK = "open_link"
	CALLBACK = "callback"
	INTENT_SUBSCRIBE = "intent_subscribe"
	INTENT_UNSUBSCRIBE = "intent_unsubscribe"

class MessagesAudioMessage(BM):
	access_key:Optional[str] = None
	transcript_error:Optional[int] = None
	duration:int
	id:int
	link_mp3:str
	link_ogg:str
	owner_id:int
	waveform:list[int]


class MessagesChat(BM):
	admin_id:int
	id:int
	kicked:Optional[bool] = None
	left:Optional[bool] = None
	photo_100:Optional[str] = None
	photo_200:Optional[str] = None
	photo_50:Optional[str] = None
	push_settings:Optional["MessagesChatPushSettings"] = None
	title:Optional[str] = None
	type:str
	users:list[int]
	is_default_photo:Optional[bool] = None
	members_count:int
	is_group_channel:Optional[bool] = None


class MessagesChatFull(BM):
	admin_id:int
	id:int
	kicked:Optional[bool] = None
	left:Optional[bool] = None
	photo_100:Optional[str] = None
	photo_200:Optional[str] = None
	photo_50:Optional[str] = None
	push_settings:Optional["MessagesChatPushSettings"] = None
	title:Optional[str] = None
	type:str
	users:list["MessagesUserXtrInvitedBy"]


class MessagesChatPreview(BM):
	admin_id:Optional[int] = None
	joined:Optional[bool] = None
	local_id:Optional[int] = None
	members:Optional[list[int]] = None
	members_count:Optional[int] = None
	title:Optional[str] = None
	is_member:Optional[bool] = None
	photo:Optional["MessagesChatSettingsPhoto"] = None
	is_don:Optional[bool] = None
	is_group_channel:Optional[bool] = None
	button:Optional["BaseLinkButton"] = None


class MessagesChatPushSettings(BM):
	disabled_until:Optional[int] = None
	sound:Optional[bool] = None


class MessagesChatRestrictions(BM):
	admins_promote_users:Optional[bool] = None
	only_admins_edit_info:Optional[bool] = None
	only_admins_edit_pin:Optional[bool] = None
	only_admins_invite:Optional[bool] = None
	only_admins_kick:Optional[bool] = None


class MessagesChatSettings(BM):
	members_count:Optional[int] = None
	friends_count:Optional[int] = None
	owner_id:int
	title:str
	pinned_message:Optional["MessagesPinnedMessage"] = None
	state:"MessagesChatSettingsState"
	photo:Optional["MessagesChatSettingsPhoto"] = None
	admin_ids:Optional[list[int]] = None
	active_ids:list[int]
	is_group_channel:Optional[bool] = None
	acl:"MessagesChatSettingsAcl"
	permissions:Optional["MessagesChatSettingsPermissions"] = None
	is_disappearing:Optional[bool] = None
	theme:Optional[str] = None
	disappearing_chat_link:Optional[str] = None
	is_service:Optional[bool] = None


class MessagesChatSettingsAcl(BM):
	can_change_info:bool
	can_change_invite_link:bool
	can_change_pin:bool
	can_invite:bool
	can_promote_users:bool
	can_see_invite_link:bool
	can_moderate:bool
	can_copy_chat:bool
	can_call:bool
	can_use_mass_mentions:bool
	can_change_service_type:Optional[bool] = None


class MessagesChatSettingsPermissions(BM):
	invite:Optional[str] = None
	change_info:Optional[str] = None
	change_pin:Optional[str] = None
	use_mass_mentions:Optional[str] = None
	see_invite_link:Optional[str] = None
	call:Optional[str] = None
	change_admins:Optional[str] = None


class MessagesChatSettingsPhoto(BM):
	photo_50:Optional[str] = None
	photo_100:Optional[str] = None
	photo_200:Optional[str] = None
	is_default_photo:Optional[bool] = None
	is_default_call_photo:Optional[bool] = None


class MessagesConversation(BM):
	peer:"MessagesConversationPeer"
	sort_id:Optional["MessagesConversationSortId"] = None
	last_message_id:int
	last_conversation_message_id:Optional[int] = None
	in_read:int
	out_read:int
	unread_count:Optional[int] = None
	is_marked_unread:Optional[bool] = None
	out_read_by:Optional["MessagesOutReadBy"] = None
	important:Optional[bool] = None
	unanswered:Optional[bool] = None
	special_service_type:Optional[str] = None
	message_request_data:Optional["MessagesMessageRequestData"] = None
	mentions:Optional[list[int]] = None
	current_keyboard:Optional["MessagesKeyboard"] = None
	push_settings:Optional["MessagesPushSettings"] = None
	can_write:Optional["MessagesConversationCanWrite"] = None
	chat_settings:Optional["MessagesChatSettings"] = None


class MessagesConversationCanWrite(BM):
	allowed:bool
	reason:Optional[int] = None


class MessagesConversationMember(BM):
	can_kick:Optional[bool] = None
	invited_by:Optional[int] = None
	is_admin:Optional[bool] = None
	is_owner:Optional[bool] = None
	is_message_request:Optional[bool] = None
	join_date:Optional[int] = None
	request_date:Optional[int] = None
	member_id:int


class MessagesConversationPeer(BM):
	id:int
	local_id:Optional[int] = None
	type:"MessagesConversationPeerType"


class MessagesConversationSortId(BM):
	major_id:int
	minor_id:int


class MessagesConversationWithMessage(BM):
	conversation:"MessagesConversation"
	last_message:Optional["MessagesMessage"] = None


class MessagesForeignMessage(BM):
	attachments:Optional[list["MessagesMessageAttachment"]] = None
	conversation_message_id:Optional[int] = None
	date:int
	from_id:int
	fwd_messages:Optional[list["MessagesForeignMessage"]] = None
	geo:Optional["BaseGeo"] = None
	id:Optional[int] = None
	peer_id:Optional[int] = None
	reply_message:Optional["MessagesForeignMessage"] = None
	text:str
	update_time:Optional[int] = None
	was_listened:Optional[bool] = None
	payload:Optional[str] = None


class MessagesForward(BM):
	owner_id:Optional[int] = None
	peer_id:Optional[int] = None
	conversation_message_ids:Optional[list[int]] = None
	message_ids:Optional[list[int]] = None
	is_reply:Optional[bool] = None


class MessagesGetConversationById(BM):
	count:int
	items:list["MessagesConversation"]


class MessagesGetConversationMembers(BM):
	items:list["MessagesConversationMember"]
	count:int
	chat_restrictions:Optional["MessagesChatRestrictions"] = None
	profiles:Optional[list["UsersUserFull"]] = None
	groups:Optional[list["GroupsGroupFull"]] = None


class MessagesGraffiti(BM):
	access_key:Optional[str] = None
	id:int
	owner_id:int
	url:str
	width:int
	height:int


class MessagesHistoryAttachment(BM):
	attachment:"MessagesHistoryMessageAttachment"
	message_id:int
	from_id:int
	forward_level:Optional[int] = None
	was_listened:Optional[bool] = None


class MessagesHistoryMessageAttachment(BM):
	audio:Optional["AudioAudio"] = None
	audio_message:Optional["MessagesAudioMessage"] = None
	doc:Optional["DocsDoc"] = None
	graffiti:Optional["MessagesGraffiti"] = None
	link:Optional["BaseLink"] = None
	market:Optional["MarketMarketItem"] = None
	photo:Optional["PhotosPhoto"] = None
	type:"MessagesHistoryMessageAttachmentType"
	video:Optional["VideoVideo"] = None
	wall:Optional["WallWallpostFull"] = None


class MessagesKeyboard(BM):
	one_time:bool
	buttons:list[list["MessagesKeyboardButton"]]
	author_id:Optional[int] = None
	inline:Optional[bool] = None


class MessagesKeyboardButton(BM):
	action:"MessagesKeyboardButtonPropertyAction"
	color:Optional[str] = None


class MessagesKeyboardButtonActionCallback(BM):
	label:str
	payload:Optional[str] = None
	type:str


class MessagesKeyboardButtonActionLocation(BM):
	payload:Optional[str] = None
	type:str


class MessagesKeyboardButtonActionOpenApp(BM):
	app_id:int
	hash:Optional[str] = None
	label:str
	owner_id:int
	payload:Optional[str] = None
	type:str


class MessagesKeyboardButtonActionOpenLink(BM):
	label:str
	link:str
	payload:Optional[str] = None
	type:str


class MessagesKeyboardButtonActionOpenPhoto(BM):
	type:str


class MessagesKeyboardButtonActionText(BM):
	label:str
	payload:Optional[str] = None
	type:str


class MessagesKeyboardButtonActionVkpay(BM):
	hash:str
	payload:Optional[str] = None
	type:str


class MessagesKeyboardButtonPropertyAction(MessagesKeyboardButtonActionLocation,
                                           MessagesKeyboardButtonActionOpenApp,
                                           MessagesKeyboardButtonActionOpenLink,
                                           MessagesKeyboardButtonActionOpenPhoto,
                                           MessagesKeyboardButtonActionText,
                                           MessagesKeyboardButtonActionCallback,
                                           MessagesKeyboardButtonActionVkpay):
	pass

class MessagesLastActivity(BM):
	online:bool
	time:int


class MessagesLongpollMessages(BM):
	count:Optional[int] = None
	items:Optional[list["MessagesMessage"]] = None


class MessagesLongpollParams(BM):
	server:str
	key:str
	ts:int
	pts:Optional[int] = None


class MessagesMessage(BM):
	action:Optional["MessagesMessageAction"] = None
	admin_author_id:Optional[int] = None
	attachments:Optional[list["MessagesMessageAttachment"]] = None
	conversation_message_id:Optional[int] = None
	date:int
	deleted:Optional[bool] = None
	from_id:int
	fwd_messages:Optional[list["MessagesForeignMessage"]] = None
	geo:Optional["BaseGeo"] = None
	id:int
	important:Optional[bool] = None
	is_hidden:Optional[bool] = None
	is_cropped:Optional[bool] = None
	keyboard:Optional["MessagesKeyboard"] = None
	members_count:Optional[int] = None
	out:bool
	payload:Optional[str] = None
	peer_id:int
	random_id:Optional[int] = None
	ref:Optional[str] = None
	ref_source:Optional[str] = None
	reply_message:Optional["MessagesForeignMessage"] = None
	text:str
	update_time:Optional[int] = None
	was_listened:Optional[bool] = None
	pinned_at:Optional[int] = None
	is_silent:Optional[bool] = None


class MessagesMessageAction(BM):
	conversation_message_id:Optional[int] = None
	email:Optional[str] = None
	member_id:Optional[int] = None
	message:Optional[str] = None
	photo:Optional["MessagesMessageActionPhoto"] = None
	text:Optional[str] = None
	type:"MessagesMessageActionStatus"


class MessagesMessageActionPhoto(BM):
	photo_50:str
	photo_100:str
	photo_200:str


class MessagesMessageAttachment(BM):
	audio:Optional["AudioAudio"] = None
	audio_message:Optional["MessagesAudioMessage"] = None
	call:Optional["CallsCall"] = None
	doc:Optional["DocsDoc"] = None
	gift:Optional["GiftsLayout"] = None
	graffiti:Optional["MessagesGraffiti"] = None
	market:Optional["MarketMarketItem"] = None
	market_market_album:Optional["MarketMarketAlbum"] = None
	photo:Optional["PhotosPhoto"] = None
	sticker:Optional["BaseSticker"] = None
	story:Optional["StoriesStory"] = None
	type:"MessagesMessageAttachmentType"
	video:Optional["VideoVideoFull"] = None
	wall_reply:Optional["WallWallComment"] = None
	poll:Optional["PollsPoll"] = None


class MessagesMessageRequestData(BM):
	status:Optional[str] = None
	inviter_id:Optional[int] = None
	request_date:Optional[int] = None


class MessagesMessagesArray(BM):
	count:Optional[int] = None
	items:Optional[list["MessagesMessage"]] = None


class MessagesOutReadBy(BM):
	count:Optional[int] = None
	member_ids:Optional[list[int]] = None


class MessagesPinnedMessage(BM):
	attachments:Optional[list["MessagesMessageAttachment"]] = None
	conversation_message_id:Optional[int] = None
	id:int
	date:int
	from_id:int
	fwd_messages:Optional[list["MessagesForeignMessage"]] = None
	geo:Optional["BaseGeo"] = None
	peer_id:int
	reply_message:Optional["MessagesForeignMessage"] = None
	text:str
	keyboard:Optional["MessagesKeyboard"] = None


class MessagesPushSettings(BM):
	disabled_forever:bool
	disabled_until:Optional[int] = None
	no_sound:bool
	disabled_mentions:Optional[bool] = None
	disabled_mass_mentions:Optional[bool] = None


class MessagesSendUserIdsResponseItem(BM):
	peer_id:int
	message_id:int
	conversation_message_id:Optional[int] = None
	error:Optional["BaseMessageError"] = None




class NewsfeedCommentsFilters(Enum):
	POST = "post"
	PHOTO = "photo"
	VIDEO = "video"
	TOPIC = "topic"
	NOTE = "note"

class NewsfeedIgnoreItemType(Enum):
	POST_ON_THE_WALL = "wall"
	TAG_ON_A_PHOTO = "tag"
	PROFILE_PHOTO = "profilephoto"
	VIDEO = "video"
	PHOTO = "photo"
	AUDIO = "audio"

class NewsfeedItemWallpostFeedbackType(Enum):
	BUTTONS = "buttons"
	STARS = "stars"

class NewsfeedNewsfeedItemType(Enum):
	POST = "post"
	PHOTO = "photo"
	PHOTO_TAG = "photo_tag"
	WALL_PHOTO = "wall_photo"
	FRIEND = "friend"
	AUDIO = "audio"
	VIDEO = "video"
	TOPIC = "topic"
	DIGEST = "digest"
	STORIES = "stories"
	NOTE = "note"
	AUDIO_PLAYLIST = "audio_playlist"
	CLIP = "clip"

class NewsfeedItemAudioAudio(BM):
	count:Optional[int] = None
	items:Optional[list["AudioAudio"]] = None


class NewsfeedItemBase(BM):
	type:"NewsfeedNewsfeedItemType"
	source_id:int
	date:int


class NewsfeedItemDigestButton(BM):
	title:str
	style:Optional[str] = None


class NewsfeedItemDigestFooter(BM):
	style:str
	text:str
	button:Optional["NewsfeedItemDigestButton"] = None


class NewsfeedItemDigestFullItem(BM):
	text:Optional[str] = None
	source_name:Optional[str] = None
	attachment_index:Optional[int] = None
	attachment:Optional["WallWallpostAttachment"] = None
	style:Optional[str] = None
	post:"WallWallpost"


class NewsfeedItemDigestHeader(BM):
	title:str
	subtitle:Optional[str] = None
	style:str
	button:Optional["NewsfeedItemDigestButton"] = None


class NewsfeedItemFriendFriends(BM):
	count:Optional[int] = None
	items:Optional[list["BaseUserId"]] = None


class NewsfeedItemHolidayRecommendationsBlockHeader(BM):
	title:Optional[str] = None
	subtitle:Optional[str] = None
	image:Optional[list["BaseImage"]] = None
	action:Optional["BaseLinkButtonAction"] = None


class NewsfeedItemPhotoPhotos(BM):
	count:Optional[int] = None
	items:Optional[list["NewsfeedNewsfeedPhoto"]] = None


class NewsfeedItemPhotoTagPhotoTags(BM):
	count:Optional[int] = None
	items:Optional[list["NewsfeedNewsfeedPhoto"]] = None


class NewsfeedItemPromoButtonAction(BM):
	url:Optional[str] = None
	type:Optional[str] = None
	target:Optional[str] = None


class NewsfeedItemPromoButtonImage(BM):
	width:Optional[int] = None
	height:Optional[int] = None
	url:Optional[str] = None


class NewsfeedItemVideoVideo(BM):
	count:Optional[int] = None
	items:Optional[list["VideoVideo"]] = None


class NewsfeedItemWallpostFeedback(BM):
	type:"NewsfeedItemWallpostFeedbackType"
	question:str
	answers:Optional[list["NewsfeedItemWallpostFeedbackAnswer"]] = None
	stars_count:Optional[int] = None
	gratitude:Optional[str] = None


class NewsfeedItemWallpostFeedbackAnswer(BM):
	title:str
	id:str


class NewsfeedList(BM):
	id:int
	title:str



class NotesNote(BM):
	read_comments:Optional[int] = None
	can_comment:Optional[bool] = None
	comments:int
	date:int
	id:int
	owner_id:int
	text:Optional[str] = None
	text_wiki:Optional[str] = None
	title:str
	view_url:str
	privacy_view:Optional[list[str]] = None
	privacy_comment:Optional[list[str]] = None


class NotesNoteComment(BM):
	date:int
	id:int
	message:str
	nid:int
	oid:int
	reply_to:Optional[int] = None
	uid:int




class NotificationsFeedback(BM):
	attachments:Optional[list["WallWallpostAttachment"]] = None
	from_id:Optional[int] = None
	geo:Optional["BaseGeo"] = None
	id:Optional[int] = None
	likes:Optional["BaseLikesInfo"] = None
	text:Optional[str] = None
	to_id:Optional[int] = None


class NotificationsNotification(BM):
	date:Optional[int] = None
	feedback:Optional["NotificationsFeedback"] = None
	parent:Optional["NotificationsNotification"] = None
	reply:Optional["NotificationsReply"] = None
	type:Optional[str] = None


class NotificationsNotificationItem(NotificationsNotification):
	pass

class NotificationsNotificationsComment(BM):
	date:Optional[int] = None
	id:Optional[int] = None
	owner_id:Optional[int] = None
	photo:Optional["PhotosPhoto"] = None
	post:Optional["WallWallpost"] = None
	text:Optional[str] = None
	topic:Optional["BoardTopic"] = None
	video:Optional["VideoVideo"] = None


class NotificationsReply(BM):
	date:Optional[int] = None
	id:Optional[int] = None
	text:Optional[int] = None


class NotificationsSendMessageError(BM):
	code:Optional[int] = None
	description:Optional[str] = None


class NotificationsSendMessageItem(BM):
	user_id:Optional[int] = None
	status:Optional[bool] = None
	error:Optional["NotificationsSendMessageError"] = None




class OauthError(BM):
	error:str
	error_description:str
	redirect_uri:Optional[str] = None




class OrdersAmount(BM):
	amounts:Optional[list["OrdersAmountItem"]] = None
	currency:Optional[str] = None


class OrdersAmountItem(BM):
	amount:Optional[int] = None
	description:Optional[str] = None
	votes:Optional[str] = None


class OrdersOrder(BM):
	amount:str
	app_order_id:str
	cancel_transaction_id:Optional[str] = None
	date:str
	id:str
	item:str
	receiver_id:str
	status:str
	transaction_id:Optional[str] = None
	user_id:str


class OrdersSubscription(BM):
	cancel_reason:Optional[str] = None
	create_time:int
	id:int
	item_id:str
	next_bill_time:Optional[int] = None
	expire_time:Optional[int] = None
	pending_cancel:Optional[bool] = None
	period:int
	period_start_time:int
	price:int
	title:Optional[str] = None
	app_id:Optional[int] = None
	application_name:Optional[str] = None
	photo_url:Optional[str] = None
	status:str
	test_mode:Optional[bool] = None
	trial_expire_time:Optional[int] = None
	update_time:int




class OwnerState(BM):
	state:Optional[int] = None
	description:Optional[str] = None




class PagesPrivacySettings(Enum):
	COMMUNITY_MANAGERS_ONLY = 0
	COMMUNITY_MEMBERS_ONLY = 1
	EVERYONE = 2

class PagesWikipage(BM):
	creator_id:Optional[int] = None
	creator_name:Optional[str] = None
	editor_id:Optional[int] = None
	editor_name:Optional[str] = None
	group_id:int
	id:int
	title:str
	views:int
	who_can_edit:"PagesPrivacySettings"
	who_can_view:"PagesPrivacySettings"


class PagesWikipageFull(BM):
	created:int
	creator_id:Optional[int] = None
	current_user_can_edit:Optional[bool] = None
	current_user_can_edit_access:Optional[bool] = None
	edited:int
	editor_id:Optional[int] = None
	group_id:int
	html:Optional[str] = None
	id:int
	source:Optional[str] = None
	title:str
	view_url:str
	views:int
	who_can_edit:"PagesPrivacySettings"
	who_can_view:"PagesPrivacySettings"
	url:Optional[str] = None
	parent:Optional[str] = None
	parent2:Optional[str] = None
	owner_id:Optional[int] = None


class PagesWikipageHistory(BM):
	id:int
	length:int
	date:int
	editor_id:int
	editor_name:str




class PhotosImageType(Enum):
	S = "s"
	M = "m"
	X = "x"
	L = "l"
	O = "o"
	P = "p"
	Q = "q"
	R = "r"
	Y = "y"
	Z = "z"
	W = "w"

class PhotosPhotoSizesType(Enum):
	S = "s"
	M = "m"
	X = "x"
	O = "o"
	P = "p"
	Q = "q"
	R = "r"
	K = "k"
	L = "l"
	Y = "y"
	Z = "z"
	C = "c"
	W = "w"
	A = "a"
	B = "b"
	E = "e"
	I = "i"
	D = "d"
	J = "j"
	TEMP = "temp"
	H = "h"
	G = "g"
	N = "n"
	F = "f"
	MAX = "max"

class PhotosImage(BM):
	height:Optional[int] = None
	type:Optional["PhotosImageType"] = None
	url:Optional[str] = None
	width:Optional[int] = None


class PhotosPhoto(BM):
	access_key:Optional[str] = None
	album_id:int
	date:int
	height:Optional[int] = None
	id:int
	images:Optional[list["PhotosImage"]] = None
	lat:Optional[int] = None
	long:Optional[int] = None
	owner_id:int
	photo_256:Optional[str] = None
	can_comment:Optional[bool] = None
	place:Optional[str] = None
	post_id:Optional[int] = None
	sizes:Optional[list["PhotosPhotoSizes"]] = None
	text:Optional[str] = None
	user_id:Optional[int] = None
	width:Optional[int] = None
	has_tags:bool
	likes:Optional["BaseLikes"] = None
	comments:Optional["BaseObjectCount"] = None
	reposts:Optional["BaseRepostsInfo"] = None
	tags:Optional["BaseObjectCount"] = None


class PhotosPhotoAlbum(BM):
	created:int
	description:Optional[str] = None
	id:int
	owner_id:int
	size:int
	thumb:Optional["PhotosPhoto"] = None
	title:str
	updated:int


class PhotosPhotoAlbumFull(BM):
	can_upload:Optional[bool] = None
	comments_disabled:Optional[bool] = None
	created:int
	description:Optional[str] = None
	can_delete:Optional[bool] = None
	id:int
	owner_id:int
	size:int
	sizes:Optional[list["PhotosPhotoSizes"]] = None
	thumb_id:Optional[int] = None
	thumb_is_last:Optional[bool] = None
	thumb_src:Optional[str] = None
	title:str
	updated:int
	upload_by_admins_only:Optional[bool] = None


class PhotosPhotoFalseable(str):
	pass

class PhotosPhotoFullXtrRealOffset(BM):
	access_key:Optional[str] = None
	album_id:int
	can_comment:Optional[bool] = None
	comments:Optional["BaseObjectCount"] = None
	date:int
	height:Optional[int] = None
	hidden:Optional["BasePropertyExists"] = None
	id:int
	lat:Optional[int] = None
	likes:Optional["BaseLikes"] = None
	long:Optional[int] = None
	owner_id:int
	photo_1280:Optional[str] = None
	photo_130:Optional[str] = None
	photo_2560:Optional[str] = None
	photo_604:Optional[str] = None
	photo_75:Optional[str] = None
	photo_807:Optional[str] = None
	post_id:Optional[int] = None
	real_offset:Optional[int] = None
	reposts:Optional["BaseObjectCount"] = None
	sizes:Optional[list["PhotosPhotoSizes"]] = None
	tags:Optional["BaseObjectCount"] = None
	text:Optional[str] = None
	user_id:Optional[int] = None
	width:Optional[int] = None


class PhotosPhotoSizes(BM):
	height:int
	url:str
	src:Optional[str] = None
	type:"PhotosPhotoSizesType"
	width:int


class PhotosPhotoTag(BM):
	date:int
	id:int
	placer_id:int
	tagged_name:str
	description:Optional[str] = None
	user_id:int
	viewed:bool
	x:int
	x2:int
	y:int
	y2:int


class PhotosPhotoUpload(BM):
	album_id:int
	upload_url:str
	fallback_upload_url:Optional[str] = None
	user_id:int
	group_id:Optional[int] = None


class PhotosPhotoXtrRealOffset(BM):
	access_key:Optional[str] = None
	album_id:int
	date:int
	height:Optional[int] = None
	hidden:Optional["BasePropertyExists"] = None
	id:int
	lat:Optional[int] = None
	long:Optional[int] = None
	owner_id:int
	photo_1280:Optional[str] = None
	photo_130:Optional[str] = None
	photo_2560:Optional[str] = None
	photo_604:Optional[str] = None
	photo_75:Optional[str] = None
	photo_807:Optional[str] = None
	post_id:Optional[int] = None
	real_offset:Optional[int] = None
	sizes:Optional[list["PhotosPhotoSizes"]] = None
	text:Optional[str] = None
	user_id:Optional[int] = None
	width:Optional[int] = None


class PhotosPhotoXtrTagInfo(BM):
	access_key:Optional[str] = None
	album_id:int
	date:int
	height:Optional[int] = None
	id:int
	lat:Optional[int] = None
	long:Optional[int] = None
	owner_id:int
	photo_1280:Optional[str] = None
	photo_130:Optional[str] = None
	photo_2560:Optional[str] = None
	photo_604:Optional[str] = None
	photo_75:Optional[str] = None
	photo_807:Optional[str] = None
	placer_id:Optional[int] = None
	post_id:Optional[int] = None
	sizes:Optional[list["PhotosPhotoSizes"]] = None
	tag_created:Optional[int] = None
	tag_id:Optional[int] = None
	text:Optional[str] = None
	user_id:Optional[int] = None
	width:Optional[int] = None


class PhotosTagsSuggestionItem(BM):
	title:Optional[str] = None
	caption:Optional[str] = None
	type:Optional[str] = None
	buttons:Optional[list["PhotosTagsSuggestionItemButton"]] = None
	photo:Optional["PhotosPhoto"] = None
	tags:Optional[list["PhotosPhotoTag"]] = None
	track_code:Optional[str] = None


class PhotosTagsSuggestionItemButton(BM):
	title:Optional[str] = None
	action:Optional[str] = None
	style:Optional[str] = None




class PodcastCover(BM):
	sizes:Optional[list["PhotosPhotoSizes"]] = None


class PodcastExternalData(BM):
	url:Optional[str] = None
	owner_url:Optional[str] = None
	title:Optional[str] = None
	owner_name:Optional[str] = None
	cover:Optional["PodcastCover"] = None




class PollsAnswer(BM):
	id:int
	rate:int
	text:str
	votes:int


class PollsBackground(BM):
	angle:Optional[int] = None
	color:Optional[str] = None
	height:Optional[int] = None
	id:Optional[int] = None
	name:Optional[str] = None
	images:Optional[list["BaseImage"]] = None
	points:Optional[list["BaseGradientPoint"]] = None
	type:Optional[str] = None
	width:Optional[int] = None


class PollsFriend(BM):
	id:int


class PollsPoll(BM):
	anonymous:Optional["PollsPollAnonymous"] = None
	friends:Optional[list["PollsFriend"]] = None
	multiple:bool
	answer_id:Optional[int] = None
	end_date:int
	answer_ids:Optional[list[int]] = None
	closed:bool
	is_board:bool
	can_edit:bool
	can_vote:bool
	can_report:bool
	can_share:bool
	embed_hash:Optional[str] = None
	photo:Optional["PollsBackground"] = None
	answers:list["PollsAnswer"]
	created:int
	id:int
	owner_id:int
	author_id:Optional[int] = None
	question:str
	background:Optional["PollsBackground"] = None
	votes:int
	disable_unvote:bool


PollsPollAnonymous = NewType('PollsPollAnonymous', bool)

class PollsVoters(BM):
	answer_id:Optional[int] = None
	users:Optional["PollsVotersUsers"] = None


class PollsVotersUsers(BM):
	count:Optional[int] = None
	items:Optional[list[int]] = None




class PrettyCardsPrettyCard(BM):
	button:Optional[Union[str,"BaseLinkButton"]] = None
	button_text:Optional[str] = None
	card_id:str
	images:Optional[list["BaseImage"]] = None
	link_url:str
	photo:str
	price:Optional[str] = None
	price_old:Optional[str] = None
	title:str


class PrettyCardsPrettyCardOrError(PrettyCardsPrettyCard, BaseError):
	pass



class SearchHintSection(Enum):
	GROUPS = "groups"
	EVENTS = "events"
	PUBLICS = "publics"
	CORRESPONDENTS = "correspondents"
	PEOPLE = "people"
	FRIENDS = "friends"
	MUTUAL_FRIENDS = "mutual_friends"
	PROMO = "promo"

class SearchHintType(Enum):
	GROUP = "group"
	PROFILE = "profile"
	VK_APP = "vk_app"
	APP = "app"
	HTML5_GAME = "html5_game"
	LINK = "link"

class SearchHint(BM):
	app:Optional["AppsApp"] = None
	description:str
	_global:Optional[bool] = None
	group:Optional["GroupsGroup"] = None
	profile:Optional["UsersUserMin"] = None
	section:Optional["SearchHintSection"] = None
	type:"SearchHintType"
	link:Optional["BaseLink"] = None




class SecureGiveEventStickerItem(BM):
	user_id:Optional[int] = None
	status:Optional[str] = None


class SecureLevel(BM):
	level:Optional[int] = None
	uid:Optional[int] = None


class SecureSetCounterItem(BM):
	id:int
	result:bool


class SecureSmsNotification(BM):
	app_id:Optional[str] = None
	date:Optional[str] = None
	id:Optional[str] = None
	message:Optional[str] = None
	user_id:Optional[str] = None


class SecureTokenChecked(BM):
	date:Optional[int] = None
	expire:Optional[int] = None
	success:Optional[int] = None
	user_id:Optional[int] = None


class SecureTransaction(BM):
	date:Optional[int] = None
	id:Optional[int] = None
	uid_from:Optional[int] = None
	uid_to:Optional[int] = None
	votes:Optional[int] = None




class StatsActivity(BM):
	comments:Optional[int] = None
	copies:Optional[int] = None
	hidden:Optional[int] = None
	likes:Optional[int] = None
	subscribed:Optional[int] = None
	unsubscribed:Optional[int] = None


class StatsCity(BM):
	count:Optional[int] = None
	name:Optional[str] = None
	value:Optional[int] = None


class StatsCountry(BM):
	code:Optional[str] = None
	count:Optional[int] = None
	name:Optional[str] = None
	value:Optional[int] = None


class StatsPeriod(BM):
	activity:Optional["StatsActivity"] = None
	period_from:Optional[int] = None
	period_to:Optional[int] = None
	reach:Optional["StatsReach"] = None
	visitors:Optional["StatsViews"] = None


class StatsReach(BM):
	age:Optional[list["StatsSexAge"]] = None
	cities:Optional[list["StatsCity"]] = None
	countries:Optional[list["StatsCountry"]] = None
	mobile_reach:Optional[int] = None
	reach:Optional[int] = None
	reach_subscribers:Optional[int] = None
	sex:Optional[list["StatsSexAge"]] = None
	sex_age:Optional[list["StatsSexAge"]] = None


class StatsSexAge(BM):
	count:Optional[int] = None
	value:str
	reach:Optional[int] = None
	reach_subscribers:Optional[int] = None
	count_subscribers:Optional[int] = None


class StatsViews(BM):
	age:Optional[list["StatsSexAge"]] = None
	cities:Optional[list["StatsCity"]] = None
	countries:Optional[list["StatsCountry"]] = None
	mobile_views:Optional[int] = None
	sex:Optional[list["StatsSexAge"]] = None
	sex_age:Optional[list["StatsSexAge"]] = None
	views:Optional[int] = None
	visitors:Optional[int] = None


class StatsWallpostStat(BM):
	post_id:Optional[int] = None
	hide:Optional[int] = None
	join_group:Optional[int] = None
	links:Optional[int] = None
	reach_subscribers:Optional[int] = None
	reach_subscribers_count:Optional[int] = None
	reach_total:Optional[int] = None
	reach_total_count:Optional[int] = None
	reach_viral:Optional[int] = None
	reach_ads:Optional[int] = None
	report:Optional[int] = None
	to_group:Optional[int] = None
	unsubscribe:Optional[int] = None
	sex_age:Optional[list["StatsSexAge"]] = None




class StatusStatus(BM):
	text:str
	audio:Optional["AudioAudio"] = None




class StickersImageSet(BM):
	base_url:str
	version:Optional[int] = None




class StorageValue(BM):
	key:str
	value:str




class StoreProduct(BM):
	id:int
	type:str
	is_new:Optional[bool] = None
	purchased:Optional[bool] = None
	active:Optional[bool] = None
	promoted:Optional[bool] = None
	purchase_date:Optional[int] = None
	title:Optional[str] = None
	stickers:Optional["BaseStickersList"] = None
	style_sticker_ids:Optional[list[int]] = None
	icon:Optional["StoreProductIcon"] = None
	previews:Optional[list["BaseImage"]] = None
	has_animation:Optional[bool] = None
	subtitle:Optional[str] = None
	payment_region:Optional[str] = None


class StoreProductIcon(BL):
    __root__:BaseImage

class StoreStickersKeyword(BM):
	words:list[str]
	user_stickers:Optional["StoreStickersKeywordStickers"] = None
	promoted_stickers:Optional["StoreStickersKeywordStickers"] = None
	stickers:Optional[list["StoreStickersKeywordSticker"]] = None


class StoreStickersKeywordSticker(BM):
	pack_id:int
	sticker_id:int


class StoreStickersKeywordStickers(BaseStickersList):
	pass



class StoriesStoryStatsState(Enum):
	ON = "on"
	OFF = "off"
	HIDDEN = "hidden"

class StoriesStoryType(Enum):
	PHOTO = "photo"
	VIDEO = "video"
	LIVE_ACTIVE = "live_active"
	LIVE_FINISHED = "live_finished"
	BIRTHDAY_INVITE = "birthday_invite"

class StoriesUploadLinkText(Enum):
	TO_STORE = "to_store"
	VOTE = "vote"
	MORE = "more"
	BOOK = "book"
	ORDER = "order"
	ENROLL = "enroll"
	FILL = "fill"
	SIGNUP = "signup"
	BUY = "buy"
	TICKET = "ticket"
	WRITE = "write"
	OPEN = "open"
	LEARN_MORE = "learn_more"
	VIEW = "view"
	GO_TO = "go_to"
	CONTACT = "contact"
	WATCH = "watch"
	PLAY = "play"
	INSTALL = "install"
	READ = "read"
	CALENDAR = "calendar"

class StoriesClickableArea(BM):
	x:int
	y:int


class StoriesClickableSticker(BM):
	clickable_area:list["StoriesClickableArea"]
	id:int
	hashtag:Optional[str] = None
	link_object:Optional["BaseLink"] = None
	mention:Optional[str] = None
	tooltip_text:Optional[str] = None
	owner_id:Optional[int] = None
	story_id:Optional[int] = None
	question:Optional[str] = None
	question_button:Optional[str] = None
	place_id:Optional[int] = None
	market_item:Optional["MarketMarketItem"] = None
	audio:Optional["AudioAudio"] = None
	audio_start_time:Optional[int] = None
	style:Optional[str] = None
	type:str
	subtype:Optional[str] = None
	post_owner_id:Optional[int] = None
	post_id:Optional[int] = None
	poll:Optional["PollsPoll"] = None
	color:Optional[str] = None
	sticker_id:Optional[int] = None
	sticker_pack_id:Optional[int] = None
	app:Optional["AppsAppMin"] = None
	app_context:Optional[str] = None
	has_new_interactions:Optional[bool] = None
	is_broadcast_notify_allowed:Optional[bool] = None
	situational_theme_id:Optional[int] = None
	situational_app_url:Optional[str] = None


class StoriesClickableStickers(BM):
	clickable_stickers:list["StoriesClickableSticker"]
	original_height:int
	original_width:int


class StoriesFeedItem(BM):
	type:str
	id:Optional[str] = None
	stories:Optional[list["StoriesStory"]] = None
	grouped:Optional[list["StoriesFeedItem"]] = None
	app:Optional["AppsAppMin"] = None
	promo_data:Optional["StoriesPromoBlock"] = None
	birthday_user_id:Optional[int] = None
	track_code:Optional[str] = None
	has_unseen:Optional[bool] = None
	name:Optional[str] = None


class StoriesPromoBlock(BM):
	name:str
	photo_50:str
	photo_100:str
	not_animated:bool


class StoriesReplies(BM):
	count:int
	new:Optional[int] = None


class StoriesStatLine(BM):
	name:str
	counter:Optional[int] = None
	is_unavailable:Optional[bool] = None


class StoriesStory(BM):
	access_key:Optional[str] = None
	can_comment:Optional[bool] = None
	can_reply:Optional[bool] = None
	can_see:Optional[bool] = None
	can_like:Optional[bool] = None
	can_share:Optional[bool] = None
	can_hide:Optional[bool] = None
	date:Optional[int] = None
	expires_at:Optional[int] = None
	id:int
	is_deleted:Optional[bool] = None
	is_expired:Optional[bool] = None
	link:Optional["StoriesStoryLink"] = None
	owner_id:int
	parent_story:Optional["StoriesStory"] = None
	parent_story_access_key:Optional[str] = None
	parent_story_id:Optional[int] = None
	parent_story_owner_id:Optional[int] = None
	photo:Optional["PhotosPhoto"] = None
	replies:Optional["StoriesReplies"] = None
	seen:Optional[bool] = None
	type:Optional["StoriesStoryType"] = None
	clickable_stickers:Optional["StoriesClickableStickers"] = None
	video:Optional["VideoVideoFull"] = None
	views:Optional[int] = None
	can_ask:Optional[bool] = None
	can_ask_anonymous:Optional[bool] = None
	narratives_count:Optional[int] = None
	first_narrative_title:Optional[str] = None
	birthday_wish_user_id:Optional[int] = None
	can_use_in_narrative:Optional[bool] = None


class StoriesStoryLink(BM):
	text:str
	url:str
	link_url_target:Optional[str] = None


class StoriesStoryStats(BM):
	answer:"StoriesStoryStatsStat"
	bans:"StoriesStoryStatsStat"
	open_link:"StoriesStoryStatsStat"
	replies:"StoriesStoryStatsStat"
	shares:"StoriesStoryStatsStat"
	subscribers:"StoriesStoryStatsStat"
	views:"StoriesStoryStatsStat"
	likes:"StoriesStoryStatsStat"


class StoriesStoryStatsStat(BM):
	count:Optional[int] = None
	state:"StoriesStoryStatsState"


class StoriesViewersItem(BM):
	is_liked:bool
	user_id:int
	user:Optional["UsersUserFull"] = None




class UsersFields(Enum):
	FIRST_NAME_NOM = "first_name_nom"
	FIRST_NAME_GEN = "first_name_gen"
	FIRST_NAME_DAT = "first_name_dat"
	FIRST_NAME_ACC = "first_name_acc"
	FIRST_NAME_INS = "first_name_ins"
	FIRST_NAME_ABL = "first_name_abl"
	LAST_NAME_NOM = "last_name_nom"
	LAST_NAME_GEN = "last_name_gen"
	LAST_NAME_DAT = "last_name_dat"
	LAST_NAME_ACC = "last_name_acc"
	LAST_NAME_INS = "last_name_ins"
	LAST_NAME_ABL = "last_name_abl"
	PHOTO_ID = "photo_id"
	VERIFIED = "verified"
	SEX = "sex"
	BDATE = "bdate"
	BDATE_VISIBILITY = "bdate_visibility"
	CITY = "city"
	COUNTRY = "country"
	HOME_TOWN = "home_town"
	HAS_PHOTO = "has_photo"
	PHOTO = "photo"
	PHOTO_REC = "photo_rec"
	PHOTO_50 = "photo_50"
	PHOTO_100 = "photo_100"
	PHOTO_200_ORIG = "photo_200_orig"
	PHOTO_200 = "photo_200"
	PHOTO_400 = "photo_400"
	PHOTO_400_ORIG = "photo_400_orig"
	PHOTO_BIG = "photo_big"
	PHOTO_MEDIUM = "photo_medium"
	PHOTO_MEDIUM_REC = "photo_medium_rec"
	PHOTO_MAX = "photo_max"
	PHOTO_MAX_ORIG = "photo_max_orig"
	PHOTO_MAX_SIZE = "photo_max_size"
	THIRD_PARTY_BUTTONS = "third_party_buttons"
	ONLINE = "online"
	LISTS = "lists"
	DOMAIN = "domain"
	HAS_MOBILE = "has_mobile"
	CONTACTS = "contacts"
	LANGUAGE = "language"
	SITE = "site"
	EDUCATION = "education"
	UNIVERSITIES = "universities"
	SCHOOLS = "schools"
	STATUS = "status"
	LAST_SEEN = "last_seen"
	FOLLOWERS_COUNT = "followers_count"
	COUNTERS = "counters"
	COMMON_COUNT = "common_count"
	ONLINE_INFO = "online_info"
	OCCUPATION = "occupation"
	NICKNAME = "nickname"
	RELATIVES = "relatives"
	RELATION = "relation"
	PERSONAL = "personal"
	CONNECTIONS = "connections"
	EXPORTS = "exports"
	WALL_COMMENTS = "wall_comments"
	WALL_DEFAULT = "wall_default"
	ACTIVITIES = "activities"
	ACTIVITY = "activity"
	INTERESTS = "interests"
	MUSIC = "music"
	MOVIES = "movies"
	TV = "tv"
	BOOKS = "books"
	IS_NO_INDEX = "is_no_index"
	GAMES = "games"
	ABOUT = "about"
	QUOTES = "quotes"
	CAN_POST = "can_post"
	CAN_SEE_ALL_POSTS = "can_see_all_posts"
	CAN_SEE_AUDIO = "can_see_audio"
	CAN_SEE_GIFTS = "can_see_gifts"
	WORK = "work"
	PLACES = "places"
	CAN_WRITE_PRIVATE_MESSAGE = "can_write_private_message"
	CAN_SEND_FRIEND_REQUEST = "can_send_friend_request"
	CAN_UPLOAD_DOC = "can_upload_doc"
	IS_FAVORITE = "is_favorite"
	IS_HIDDEN_FROM_FEED = "is_hidden_from_feed"
	TIMEZONE = "timezone"
	SCREEN_NAME = "screen_name"
	MAIDEN_NAME = "maiden_name"
	CROP_PHOTO = "crop_photo"
	IS_FRIEND = "is_friend"
	FRIEND_STATUS = "friend_status"
	CAREER = "career"
	MILITARY = "military"
	BLACKLISTED = "blacklisted"
	BLACKLISTED_BY_ME = "blacklisted_by_me"
	CAN_SUBSCRIBE_POSTS = "can_subscribe_posts"
	DESCRIPTIONS = "descriptions"
	TRENDING = "trending"
	MUTUAL = "mutual"
	FRIENDSHIP_WEEKS = "friendship_weeks"
	CAN_INVITE_TO_CHATS = "can_invite_to_chats"
	STORIES_ARCHIVE_COUNT = "stories_archive_count"
	HAS_UNSEEN_STORIES = "has_unseen_stories"
	VIDEO_LIVE = "video_live"
	VIDEO_LIVE_LEVEL = "video_live_level"
	VIDEO_LIVE_COUNT = "video_live_count"
	CLIPS_COUNT = "clips_count"
	SERVICE_DESCRIPTION = "service_description"
	CAN_SEE_WISHES = "can_see_wishes"
	IS_SUBSCRIBED_PODCASTS = "is_subscribed_podcasts"
	CAN_SUBSCRIBE_PODCASTS = "can_subscribe_podcasts"

class UsersUserRelation(Enum):
	NOT_SPECIFIED = 0
	SINGLE = 1
	IN_A_RELATIONSHIP = 2
	ENGAGED = 3
	MARRIED = 4
	COMPLICATED = 5
	ACTIVELY_SEARCHING = 6
	IN_LOVE = 7
	IN_A_CIVIL_UNION = 8

class UsersUserType(Enum):
	PROFILE = "profile"

class UsersCareer(BM):
	city_id:Optional[int] = None
	city_name:Optional[str] = None
	company:Optional[str] = None
	country_id:Optional[int] = None
	_from:Optional[int] = None
	group_id:Optional[int] = None
	id:Optional[int] = None
	position:Optional[str] = None
	until:Optional[int] = None


class UsersExports(BM):
	facebook:Optional[int] = None
	livejournal:Optional[int] = None
	twitter:Optional[int] = None


class UsersLastSeen(BM):
	platform:Optional[int] = None
	time:Optional[int] = None


class UsersMilitary(BM):
	country_id:int
	_from:Optional[int] = None
	id:Optional[int] = None
	unit:str
	unit_id:int
	until:Optional[int] = None


class UsersOccupation(BM):
	id:Optional[int] = None
	name:Optional[str] = None
	type:Optional[str] = None


class UsersOnlineInfo(BM):
	visible:bool
	last_seen:Optional[int] = None
	is_online:Optional[bool] = None
	app_id:Optional[int] = None
	is_mobile:Optional[bool] = None
	status:Optional[str] = None


class UsersPersonal(BM):
	alcohol:Optional[int] = None
	inspired_by:Optional[str] = None
	langs:Optional[list[str]] = None
	life_main:Optional[int] = None
	people_main:Optional[int] = None
	political:Optional[int] = None
	religion:Optional[str] = None
	religion_id:Optional[int] = None
	smoking:Optional[int] = None


class UsersRelative(BM):
	birth_date:Optional[str] = None
	id:Optional[int] = None
	name:Optional[str] = None
	type:str


class UsersSchool(BM):
	city:Optional[int] = None
	_class:Optional[str] = None
	country:Optional[int] = None
	id:Optional[str] = None
	name:Optional[str] = None
	type:Optional[int] = None
	type_str:Optional[str] = None
	year_from:Optional[int] = None
	year_graduated:Optional[int] = None
	year_to:Optional[int] = None
	speciality:Optional[str] = None


class UsersUniversity(BM):
	chair:Optional[int] = None
	chair_name:Optional[str] = None
	city:Optional[int] = None
	country:Optional[int] = None
	education_form:Optional[str] = None
	education_status:Optional[str] = None
	faculty:Optional[int] = None
	faculty_name:Optional[str] = None
	graduation:Optional[int] = None
	id:Optional[int] = None
	name:Optional[str] = None
	university_group_id:Optional[int] = None


class UsersUserConnections(BM):
	skype:str
	facebook:str
	facebook_name:Optional[str] = None
	twitter:str
	livejournal:Optional[str] = None
	instagram:str


class UsersUserCounters(BM):
	albums:Optional[int] = None
	badges:Optional[int] = None
	audios:Optional[int] = None
	followers:Optional[int] = None
	friends:Optional[int] = None
	gifts:Optional[int] = None
	groups:Optional[int] = None
	notes:Optional[int] = None
	online_friends:Optional[int] = None
	pages:Optional[int] = None
	photos:Optional[int] = None
	subscriptions:Optional[int] = None
	user_photos:Optional[int] = None
	user_videos:Optional[int] = None
	videos:Optional[int] = None
	new_photo_tags:Optional[int] = None
	new_recognition_tags:Optional[int] = None
	mutual_friends:Optional[int] = None
	posts:Optional[int] = None
	articles:Optional[int] = None
	wishes:Optional[int] = None
	podcasts:Optional[int] = None
	clips:Optional[int] = None
	clips_followers:Optional[int] = None


class UsersUserMin(BM):
	deactivated:Optional[str] = None
	first_name:Optional[str] = None
	hidden:Optional[int] = None
	id:int
	last_name:Optional[str] = None
	can_access_closed:Optional[bool] = None
	is_closed:Optional[bool] = None


class UsersUserSettingsXtr(BM):
	connections:Optional["UsersUserConnections"] = None
	bdate:Optional[str] = None
	bdate_visibility:Optional[int] = None
	city:Optional["BaseCity"] = None
	country:Optional["BaseCountry"] = None
	first_name:Optional[str] = None
	home_town:str
	last_name:Optional[str] = None
	maiden_name:Optional[str] = None
	name_request:Optional["AccountNameRequest"] = None
	personal:Optional["UsersPersonal"] = None
	phone:Optional[str] = None
	relation:Optional["UsersUserRelation"] = None
	relation_partner:Optional["UsersUserMin"] = None
	relation_pending:Optional[bool] = None
	relation_requests:Optional[list["UsersUserMin"]] = None
	screen_name:Optional[str] = None
	sex:Optional["BaseSex"] = None
	status:str
	status_audio:Optional["AudioAudio"] = None
	interests:Optional["AccountUserSettingsInterests"] = None
	languages:Optional[list[str]] = None


class UsersUsersArray(BM):
	count:int
	items:list[int]




class UtilsDomainResolvedType(Enum):
	USER = "user"
	GROUP = "group"
	APPLICATION = "application"
	PAGE = "page"
	VK_APP = "vk_app"
	COMMUNITY_APPLICATION = "community_application"

class UtilsLinkCheckedStatus(Enum):
	NOT_BANNED = "not_banned"
	BANNED = "banned"
	PROCESSING = "processing"

class UtilsDomainResolved(BM):
	object_id:Optional[int] = None
	group_id:Optional[int] = None
	type:Optional["UtilsDomainResolvedType"] = None


class UtilsLastShortenedLink(BM):
	access_key:Optional[str] = None
	key:Optional[str] = None
	short_url:Optional[str] = None
	timestamp:Optional[int] = None
	url:Optional[str] = None
	views:Optional[int] = None


class UtilsLinkChecked(BM):
	link:Optional[str] = None
	status:Optional["UtilsLinkCheckedStatus"] = None


class UtilsLinkStats(BM):
	key:Optional[str] = None
	stats:Optional[list["UtilsStats"]] = None


class UtilsLinkStatsExtended(BM):
	key:Optional[str] = None
	stats:Optional[list["UtilsStatsExtended"]] = None


class UtilsShortLink(BM):
	access_key:Optional[str] = None
	key:Optional[str] = None
	short_url:Optional[str] = None
	url:Optional[str] = None


class UtilsStats(BM):
	timestamp:Optional[int] = None
	views:Optional[int] = None


class UtilsStatsCity(BM):
	city_id:Optional[int] = None
	views:Optional[int] = None


class UtilsStatsCountry(BM):
	country_id:Optional[int] = None
	views:Optional[int] = None


class UtilsStatsExtended(BM):
	cities:Optional[list["UtilsStatsCity"]] = None
	countries:Optional[list["UtilsStatsCountry"]] = None
	sex_age:Optional[list["UtilsStatsSexAge"]] = None
	timestamp:Optional[int] = None
	views:Optional[int] = None


class UtilsStatsSexAge(BM):
	age_range:Optional[str] = None
	female:Optional[int] = None
	male:Optional[int] = None




class VideoLiveInfo(BM):
	enabled:bool
	is_notifications_blocked:Optional[bool] = None


class VideoLiveSettings(BM):
	can_rewind:Optional[bool] = None
	is_endless:Optional[bool] = None
	max_duration:Optional[int] = None


class VideoSaveResult(BM):
	access_key:Optional[str] = None
	description:Optional[str] = None
	owner_id:Optional[int] = None
	title:Optional[str] = None
	upload_url:str
	video_id:Optional[int] = None


class VideoVideo(BM):
	access_key:Optional[str] = None
	adding_date:Optional[int] = None
	can_comment:Optional[bool] = None
	can_edit:Optional[bool] = None
	can_like:Optional[bool] = None
	can_repost:Optional[bool] = None
	can_subscribe:Optional[bool] = None
	can_add_to_faves:Optional[bool] = None
	can_add:Optional[bool] = None
	can_attach_link:Optional[bool] = None
	is_private:Optional[bool] = None
	comments:Optional[int] = None
	date:Optional[int] = None
	description:Optional[str] = None
	duration:Optional[int] = None
	image:Optional[list["VideoVideoImage"]] = None
	first_frame:Optional[list["VideoVideoImage"]] = None
	width:Optional[int] = None
	height:Optional[int] = None
	id:Optional[int] = None
	owner_id:Optional[int] = None
	user_id:Optional[int] = None
	title:Optional[str] = None
	is_favorite:Optional[bool] = None
	player:Optional[str] = None
	processing:Optional["BasePropertyExists"] = None
	converting:Optional[bool] = None
	added:Optional[bool] = None
	is_subscribed:Optional[bool] = None
	track_code:Optional[str] = None
	repeat:Optional["BasePropertyExists"] = None
	type:Optional[str] = None
	views:Optional[int] = None
	local_views:Optional[int] = None
	content_restricted:Optional[int] = None
	content_restricted_message:Optional[str] = None
	balance:Optional[int] = None
	live_status:Optional[str] = None
	live:Optional["BasePropertyExists"] = None
	upcoming:Optional["BasePropertyExists"] = None
	live_start_time:Optional[int] = None
	live_notify:Optional[bool] = None
	spectators:Optional[int] = None
	platform:Optional[str] = None
	likes:Optional["BaseLikes"] = None
	reposts:Optional["BaseRepostsInfo"] = None


class VideoVideoAlbum(BM):
	id:int
	owner_id:int
	title:str


class VideoVideoFiles(BM):
	external:Optional[str] = None
	mp4_144:Optional[str] = None
	mp4_240:Optional[str] = None
	mp4_360:Optional[str] = None
	mp4_480:Optional[str] = None
	mp4_720:Optional[str] = None
	mp4_1080:Optional[str] = None
	mp4_1440:Optional[str] = None
	mp4_2160:Optional[str] = None
	flv_320:Optional[str] = None




class WallCommentAttachmentType(Enum):
	PHOTO = "photo"
	AUDIO = "audio"
	VIDEO = "video"
	DOC = "doc"
	LINK = "link"
	NOTE = "note"
	PAGE = "page"
	MARKET_MARKET_ALBUM = "market_market_album"
	MARKET = "market"
	STICKER = "sticker"

class WallGetFilter(Enum):
	OWNER = "owner"
	OTHERS = "others"
	ALL = "all"
	POSTPONED = "postponed"
	SUGGESTS = "suggests"
	ARCHIVED = "archived"
	DONUT = "donut"

class WallPostSourceType(Enum):
	VK = "vk"
	WIDGET = "widget"
	API = "api"
	RSS = "rss"
	SMS = "sms"
	MVK = "mvk"

class WallPostType(Enum):
	POST = "post"
	COPY = "copy"
	REPLY = "reply"
	POSTPONE = "postpone"
	SUGGEST = "suggest"
	POST_ADS = "post_ads"
	PHOTO = "photo"
	VIDEO = "video"

class WallWallpostAttachmentType(Enum):
	PHOTO = "photo"
	PHOTOS_LIST = "photos_list"
	POSTED_PHOTO = "posted_photo"
	AUDIO = "audio"
	AUDIO_PLAYLIST = "audio_playlist"
	VIDEO = "video"
	DOC = "doc"
	LINK = "link"
	GRAFFITI = "graffiti"
	NOTE = "note"
	APP = "app"
	POLL = "poll"
	PAGE = "page"
	ALBUM = "album"
	MARKET_ALBUM = "market_album"
	MARKET = "market"
	EVENT = "event"
	DONUT_LINK = "donut_link"
	ARTICLE = "article"
	TEXTLIVE = "textlive"
	TEXTPOST = "textpost"
	TEXTPOST_PUBLISH = "textpost_publish"
	SITUATIONAL_THEME = "situational_theme"
	GROUP = "group"
	STICKER = "sticker"
	PODCAST = "podcast"

class WallAppPost(BM):
	id:Optional[int] = None
	name:Optional[str] = None
	photo_130:Optional[str] = None
	photo_604:Optional[str] = None


class WallAttachedNote(BM):
	comments:int
	date:int
	id:int
	owner_id:int
	read_comments:int
	title:str
	text:Optional[str] = None
	privacy_view:Optional[list[str]] = None
	privacy_comment:Optional[list[str]] = None
	can_comment:Optional[int] = None
	text_wiki:Optional[str] = None
	view_url:str


class WallCarouselBase(BM):
	carousel_offset:Optional[int] = None


class WallCommentAttachment(BM):
	audio:Optional["AudioAudio"] = None
	doc:Optional["DocsDoc"] = None
	link:Optional["BaseLink"] = None
	market:Optional["MarketMarketItem"] = None
	market_market_album:Optional["MarketMarketAlbum"] = None
	note:Optional["WallAttachedNote"] = None
	page:Optional["PagesWikipageFull"] = None
	photo:Optional["PhotosPhoto"] = None
	sticker:Optional["BaseSticker"] = None
	type:"WallCommentAttachmentType"
	video:Optional["VideoVideo"] = None


class WallGeo(BM):
	coordinates:Optional[str] = None
	place:Optional["BasePlace"] = None
	showmap:Optional[int] = None
	type:Optional[str] = None


class WallGraffiti(BM):
	id:Optional[int] = None
	owner_id:Optional[int] = None
	photo_200:Optional[str] = None
	photo_586:Optional[str] = None
	height:Optional[int] = None
	url:Optional[str] = None
	width:Optional[int] = None
	access_key:Optional[str] = None


class WallPostCopyright(BM):
	id:Optional[int] = None
	link:str
	name:str
	type:str


class WallPostSource(BM):
	data:Optional[str] = None
	platform:Optional[str] = None
	type:Optional["WallPostSourceType"] = None
	url:Optional[str] = None
	link:Optional["BaseLink"] = None


class WallPostedPhoto(BM):
	id:Optional[int] = None
	owner_id:Optional[int] = None
	photo_130:Optional[str] = None
	photo_604:Optional[str] = None


class WallViews(BM):
	count:Optional[int] = None


class WallWallComment(BM):
	id:int
	from_id:int
	can_edit:Optional[bool] = None
	post_id:Optional[int] = None
	owner_id:Optional[int] = None
	parents_stack:Optional[list[int]] = None
	photo_id:Optional[int] = None
	video_id:Optional[int] = None
	date:int
	text:str
	attachments:Optional[list["WallCommentAttachment"]] = None
	donut:Optional["WallWallCommentDonut"] = None
	likes:Optional["BaseLikesInfo"] = None
	real_offset:Optional[int] = None
	reply_to_user:Optional[int] = None
	reply_to_comment:Optional[int] = None
	thread:Optional["CommentThread"] = None
	deleted:Optional[bool] = None
	pid:Optional[int] = None


class WallWallCommentDonut(BM):
	is_don:Optional[bool] = None
	placeholder:Optional["WallWallCommentDonutPlaceholder"] = None


class WallWallCommentDonutPlaceholder(BM):
	text:str


class WallWallpost(BM):
	access_key:Optional[str] = None
	is_deleted:Optional[bool] = None
	attachments:Optional[list["WallWallpostAttachment"]] = None
	copyright:Optional["WallPostCopyright"] = None
	date:Optional[int] = None
	edited:Optional[int] = None
	from_id:Optional[int] = None
	geo:Optional["WallGeo"] = None
	id:Optional[int] = None
	is_archived:Optional[bool] = None
	is_favorite:Optional[bool] = None
	likes:Optional["BaseLikesInfo"] = None
	owner_id:Optional[int] = None
	post_id:Optional[int] = None
	parents_stack:Optional[list[int]] = None
	post_source:Optional["WallPostSource"] = None
	post_type:Optional["WallPostType"] = None
	reposts:Optional["BaseRepostsInfo"] = None
	signer_id:Optional[int] = None
	text:Optional[str] = None
	views:Optional["WallViews"] = None


class WallWallpostAttachment(BM):
	access_key:Optional[str] = None
	album:Optional["PhotosPhotoAlbum"] = None
	app:Optional["WallAppPost"] = None
	audio:Optional["AudioAudio"] = None
	doc:Optional["DocsDoc"] = None
	event:Optional["EventsEventAttach"] = None
	group:Optional["GroupsGroupAttach"] = None
	graffiti:Optional["WallGraffiti"] = None
	link:Optional["BaseLink"] = None
	market:Optional["MarketMarketItem"] = None
	market_album:Optional["MarketMarketAlbum"] = None
	note:Optional["NotesNote"] = None
	page:Optional["PagesWikipageFull"] = None
	photo:Optional["PhotosPhoto"] = None
	poll:Optional["PollsPoll"] = None
	posted_photo:Optional["WallPostedPhoto"] = None
	type:"WallWallpostAttachmentType"
	video:Optional["VideoVideoFull"] = None


class WallWallpostCommentsDonut(BM):
	placeholder:Optional["WallWallpostCommentsDonutPlaceholder"] = None


class WallWallpostCommentsDonutPlaceholder(BM):
	text:str


class WallWallpostDonut(BM):
	is_donut:bool
	paid_duration:Optional[int] = None
	placeholder:Optional["WallWallpostDonutPlaceholder"] = None
	can_publish_free_copy:Optional[bool] = None
	edit_mode:Optional[str] = None


class WallWallpostDonutPlaceholder(BM):
	text:str


class WallWallpostToId(BM):
	attachments:Optional[list["WallWallpostAttachment"]] = None
	comments:Optional["BaseCommentsInfo"] = None
	copy_owner_id:Optional[int] = None
	copy_post_id:Optional[int] = None
	date:Optional[int] = None
	from_id:Optional[int] = None
	geo:Optional["WallGeo"] = None
	id:Optional[int] = None
	is_favorite:Optional[bool] = None
	likes:Optional["BaseLikesInfo"] = None
	post_id:Optional[int] = None
	post_source:Optional["WallPostSource"] = None
	post_type:Optional["WallPostType"] = None
	reposts:Optional["BaseRepostsInfo"] = None
	signer_id:Optional[int] = None
	text:Optional[str] = None
	to_id:Optional[int] = None




class WidgetsCommentMediaType(Enum):
	AUDIO = "audio"
	PHOTO = "photo"
	VIDEO = "video"

class WidgetsCommentMedia(BM):
	item_id:Optional[int] = None
	owner_id:Optional[int] = None
	thumb_src:Optional[str] = None
	type:Optional["WidgetsCommentMediaType"] = None


class WidgetsCommentReplies(BM):
	can_post:Optional[bool] = None
	count:Optional[int] = None
	replies:Optional[list["WidgetsCommentRepliesItem"]] = None


class WidgetsCommentRepliesItem(BM):
	cid:Optional[int] = None
	date:Optional[int] = None
	likes:Optional["WidgetsWidgetLikes"] = None
	text:Optional[str] = None
	uid:Optional[int] = None
	user:Optional["UsersUserFull"] = None


class WidgetsWidgetComment(BM):
	attachments:Optional[list["WallCommentAttachment"]] = None
	can_delete:Optional[bool] = None
	comments:Optional["WidgetsCommentReplies"] = None
	date:int
	from_id:int
	id:int
	likes:Optional["BaseLikesInfo"] = None
	media:Optional["WidgetsCommentMedia"] = None
	post_source:Optional["WallPostSource"] = None
	post_type:int
	reposts:Optional["BaseRepostsInfo"] = None
	text:str
	to_id:int
	user:Optional["UsersUserFull"] = None


class WidgetsWidgetLikes(BM):
	count:Optional[int] = None


class WidgetsWidgetPage(BM):
	comments:Optional["BaseObjectCount"] = None
	date:Optional[int] = None
	description:Optional[str] = None
	id:Optional[int] = None
	likes:Optional["BaseObjectCount"] = None
	page_id:Optional[str] = None
	photo:Optional[str] = None
	title:Optional[str] = None
	url:Optional[str] = None




class AccountUserSettings(UsersUserMin, UsersUserSettingsXtr):
	photo_200:Optional[str] = None
	is_service_account:Optional[bool] = None

class AdsTargSettings(AdsCriteria):
	id:Optional[int] = None
	campaign_id:Optional[int] = None

class AppsApp(AppsAppMin):
	author_url:Optional[str] = None
	banner_1120:Optional[str] = None
	banner_560:Optional[str] = None
	icon_16:Optional[str] = None
	is_new:Optional[bool] = None
	push_enabled:Optional[bool] = None
	screen_orientation:Optional[int] = None
	friends:Optional[list[int]] = None
	catalog_position:Optional[int] = None
	description:Optional[str] = None
	genre:Optional[str] = None
	genre_id:Optional[int] = None
	international:Optional[bool] = None
	is_in_catalog:Optional[int] = None
	leaderboard_type:Optional["AppsAppLeaderboardType"] = None
	members_count:Optional[int] = None
	platform_id:Optional[str] = None
	published_date:Optional[int] = None
	screen_name:Optional[str] = None
	section:Optional[str] = None

class CallbackConfirmation(CallbackBase):
	type:Optional[str] = None

class CallbackMessageAllow(CallbackBase):
	type:Optional[str] = None
	object:"CallbackMessageAllowObject"

class CallbackMessageEdit(CallbackBase):
	type:Optional[str] = None
	object:"MessagesMessage"

class CallbackMessageNew(CallbackBase):
	type:Optional[str] = None
	object:object

class CallbackMessageReply(CallbackBase):
	type:Optional[str] = None
	object:"MessagesMessage"

class DatabaseCity(BaseObject):
	area:Optional[str] = None
	region:Optional[str] = None
	important:Optional[bool] = None

class FriendsFriendExtendedStatus(FriendsFriendStatus):
	is_request_unread:Optional[bool] = None

class GroupsGroupFull(GroupsGroup):
	market:Optional["GroupsMarketInfo"] = None
	member_status:Optional["GroupsGroupFullMemberStatus"] = None
	is_adult:Optional[bool] = None
	is_hidden_from_feed:Optional[bool] = None
	is_favorite:Optional[bool] = None
	is_subscribed:Optional[bool] = None
	city:Optional["BaseObject"] = None
	country:Optional["BaseCountry"] = None
	verified:Optional[bool] = None
	description:Optional[str] = None
	wiki_page:Optional[str] = None
	members_count:Optional[int] = None
	members_count_text:Optional[str] = None
	requests_count:Optional[int] = None
	video_live_level:Optional[int] = None
	video_live_count:Optional[int] = None
	clips_count:Optional[int] = None
	counters:Optional["GroupsCountersGroup"] = None
	cover:Optional["GroupsCover"] = None
	can_post:Optional[bool] = None
	can_suggest:Optional[bool] = None
	can_upload_story:Optional[bool] = None
	can_upload_doc:Optional[bool] = None
	can_upload_video:Optional[bool] = None
	can_see_all_posts:Optional[bool] = None
	can_create_topic:Optional[bool] = None
	activity:Optional[str] = None
	fixed_post:Optional[int] = None
	has_photo:Optional[bool] = None
	crop_photo:Optional["BaseCropPhoto"] = None
	status:Optional[str] = None
	status_audio:Optional["AudioAudio"] = None
	main_album_id:Optional[int] = None
	links:Optional[list["GroupsLinksItem"]] = None
	contacts:Optional[list["GroupsContactsItem"]] = None
	wall:Optional[int] = None
	site:Optional[str] = None
	main_section:Optional["GroupsGroupFullSection"] = None
	secondary_section:Optional["GroupsGroupFullSection"] = None
	trending:Optional[bool] = None
	can_message:Optional[bool] = None
	is_messages_blocked:Optional[bool] = None
	can_send_notify:Optional[bool] = None
	online_status:Optional["GroupsOnlineStatus"] = None
	invited_by:Optional[int] = None
	age_limits:Optional["GroupsGroupFullAgeLimits"] = None
	ban_info:Optional["GroupsGroupBanInfo"] = None
	has_market_app:Optional[bool] = None
	using_vkpay_market_app:Optional[bool] = None
	has_group_channel:Optional[bool] = None
	addresses:Optional["GroupsAddressesInfo"] = None
	is_subscribed_podcasts:Optional[bool] = None
	can_subscribe_podcasts:Optional[bool] = None
	can_subscribe_posts:Optional[bool] = None
	live_covers:Optional["GroupsLiveCovers"] = None
	stories_archive_count:Optional[int] = None
	has_unseen_stories:Optional[bool] = None

class MarketMarketItemFull(MarketMarketItem):
	albums_ids:Optional[list[int]] = None
	photos:Optional[list["PhotosPhoto"]] = None
	can_comment:Optional[bool] = None
	can_repost:Optional[bool] = None
	likes:Optional["BaseLikes"] = None
	reposts:Optional["BaseRepostsInfo"] = None
	views_count:Optional[int] = None
	wishlist_item_id:Optional[int] = None
	cancel_info:Optional["BaseLink"] = None
	user_agreement_info:Optional[str] = None
	ad_id:Optional[int] = None

class MessagesGetConversationByIdExtended(MessagesGetConversationById):
	profiles:Optional[list["UsersUserFull"]] = None
	groups:Optional[list["GroupsGroupFull"]] = None

class NewsfeedItemAudio(NewsfeedItemBase):
	audio:Optional["NewsfeedItemAudioAudio"] = None
	post_id:Optional[int] = None

class NewsfeedItemDigest(NewsfeedItemBase):
	feed_id:Optional[str] = None
	items:Optional[list["NewsfeedItemDigestItem"]] = None
	main_post_ids:Optional[list[str]] = None
	template:Optional[str] = None
	header:Optional["NewsfeedItemDigestHeader"] = None
	footer:Optional["NewsfeedItemDigestFooter"] = None
	track_code:Optional[str] = None

class NewsfeedItemFriend(NewsfeedItemBase):
	friends:Optional["NewsfeedItemFriendFriends"] = None

class NewsfeedItemPhoto(WallCarouselBase, NewsfeedItemBase):
	photos:Optional["NewsfeedItemPhotoPhotos"] = None
	post_id:Optional[int] = None

class NewsfeedItemPhotoTag(WallCarouselBase, NewsfeedItemBase):
	photo_tags:Optional["NewsfeedItemPhotoTagPhotoTags"] = None
	post_id:Optional[int] = None

class NewsfeedItemPromoButton(NewsfeedItemBase):
	text:Optional[str] = None
	title:Optional[str] = None
	action:Optional["NewsfeedItemPromoButtonAction"] = None
	images:Optional[list["NewsfeedItemPromoButtonImage"]] = None
	track_code:Optional[str] = None

class NewsfeedItemTopic(NewsfeedItemBase):
	comments:Optional["BaseCommentsInfo"] = None
	likes:Optional["BaseLikesInfo"] = None
	post_id:int
	text:str

class NewsfeedItemVideo(WallCarouselBase, NewsfeedItemBase):
	video:Optional["NewsfeedItemVideoVideo"] = None

class NewsfeedListFull(NewsfeedList):
	no_reposts:Optional[bool] = None
	source_ids:Optional[list[int]] = None

class NewsfeedNewsfeedPhoto(PhotosPhoto):
	likes:Optional["BaseLikes"] = None
	comments:Optional["BaseObjectCount"] = None
	can_repost:Optional[bool] = None

class NotificationsNotificationParent(WallWallpostToId, PhotosPhoto, BoardTopic, VideoVideo, NotificationsNotificationsComment):
	pass
class UsersUser(UsersUserMin):
	sex:Optional["BaseSex"] = None
	screen_name:Optional[str] = None
	photo_50:Optional[str] = None
	photo_100:Optional[str] = None
	online_info:Optional["UsersOnlineInfo"] = None
	online:Optional[bool] = None
	online_mobile:Optional[bool] = None
	online_app:Optional[int] = None
	verified:Optional[bool] = None
	trending:Optional[bool] = None
	friend_status:Optional["FriendsFriendStatusStatus"] = None
	mutual:Optional["FriendsRequestsMutual"] = None

class UsersUserFull(UsersUser):
	first_name_nom:Optional[str] = None
	first_name_gen:Optional[str] = None
	first_name_dat:Optional[str] = None
	first_name_acc:Optional[str] = None
	first_name_ins:Optional[str] = None
	first_name_abl:Optional[str] = None
	last_name_nom:Optional[str] = None
	last_name_gen:Optional[str] = None
	last_name_dat:Optional[str] = None
	last_name_acc:Optional[str] = None
	last_name_ins:Optional[str] = None
	last_name_abl:Optional[str] = None
	nickname:Optional[str] = None
	maiden_name:Optional[str] = None
	contact_name:Optional[str] = None
	domain:Optional[str] = None
	bdate:Optional[str] = None
	city:Optional["BaseCity"] = None
	country:Optional["BaseCountry"] = None
	timezone:Optional[int] = None
	owner_state:Optional["OwnerState"] = None
	photo_200:Optional[str] = None
	photo_max:Optional[str] = None
	photo_200_orig:Optional[str] = None
	photo_400_orig:Optional[str] = None
	photo_max_orig:Optional[str] = None
	photo_id:Optional[str] = None
	has_photo:Optional[bool] = None
	has_mobile:Optional[bool] = None
	is_friend:Optional[bool] = None
	wall_comments:Optional[bool] = None
	can_post:Optional[bool] = None
	can_see_all_posts:Optional[bool] = None
	can_see_audio:Optional[bool] = None
	type:Optional["UsersUserType"] = None
	email:Optional[str] = None
	skype:Optional[str] = None
	facebook:Optional[str] = None
	facebook_name:Optional[str] = None
	twitter:Optional[str] = None
	livejournal:Optional[str] = None
	instagram:Optional[str] = None
	test:Optional[bool] = None
	video_live:Optional["VideoLiveInfo"] = None
	is_video_live_notifications_blocked:Optional[bool] = None
	is_service:Optional[bool] = None
	service_description:Optional[str] = None
	photo_rec:Optional["PhotosPhotoFalseable"] = None
	photo_medium:Optional["PhotosPhotoFalseable"] = None
	photo_medium_rec:Optional["PhotosPhotoFalseable"] = None
	photo:Optional[str] = None
	photo_big:Optional[str] = None
	photo_400:Optional[str] = None
	photo_max_size:Optional["PhotosPhoto"] = None
	language:Optional[str] = None
	stories_archive_count:Optional[int] = None
	has_unseen_stories:Optional[bool] = None
	wall_default:Optional[str] = None
	can_call:Optional[bool] = None
	can_call_from_group:Optional[bool] = None
	can_see_wishes:Optional[bool] = None
	can_see_gifts:Optional[bool] = None
	interests:Optional[str] = None
	books:Optional[str] = None
	tv:Optional[str] = None
	quotes:Optional[str] = None
	about:Optional[str] = None
	games:Optional[str] = None
	movies:Optional[str] = None
	activities:Optional[str] = None
	music:Optional[str] = None
	can_write_private_message:Optional[bool] = None
	can_send_friend_request:Optional[bool] = None
	can_be_invited_group:Optional[bool] = None
	mobile_phone:Optional[str] = None
	home_phone:Optional[str] = None
	site:Optional[str] = None
	status_audio:Optional["AudioAudio"] = None
	status:Optional[str] = None
	activity:Optional[str] = None
	last_seen:Optional["UsersLastSeen"] = None
	exports:Optional["UsersExports"] = None
	crop_photo:Optional["BaseCropPhoto"] = None
	followers_count:Optional[int] = None
	video_live_level:Optional[int] = None
	video_live_count:Optional[int] = None
	clips_count:Optional[int] = None
	blacklisted:Optional[bool] = None
	blacklisted_by_me:Optional[bool] = None
	is_favorite:Optional[bool] = None
	is_hidden_from_feed:Optional[bool] = None
	common_count:Optional[int] = None
	occupation:Optional["UsersOccupation"] = None
	career:Optional[list["UsersCareer"]] = None
	military:Optional[list["UsersMilitary"]] = None
	university:Optional[int] = None
	university_name:Optional[str] = None
	university_group_id:Optional[int] = None
	faculty:Optional[int] = None
	faculty_name:Optional[str] = None
	graduation:Optional[int] = None
	education_form:Optional[str] = None
	education_status:Optional[str] = None
	home_town:Optional[str] = None
	relation:Optional["UsersUserRelation"] = None
	relation_partner:Optional["UsersUserMin"] = None
	personal:Optional["UsersPersonal"] = None
	universities:Optional[list["UsersUniversity"]] = None
	schools:Optional[list["UsersSchool"]] = None
	relatives:Optional[list["UsersRelative"]] = None
	is_subscribed_podcasts:Optional[bool] = None
	can_subscribe_podcasts:Optional[bool] = None
	can_subscribe_posts:Optional[bool] = None
	counters:Optional["UsersUserCounters"] = None
	access_key:Optional[str] = None
	can_upload_doc:Optional[bool] = None
	hash:Optional[str] = None
	is_no_index:Optional[bool] = None
	contact_id:Optional[int] = None
	is_message_request:Optional[bool] = None
	descriptions:Optional[list[str]] = None
	lists:Optional[list[int]] = None

class UsersUserXtrType(UsersUser):
	type:Optional["UsersUserType"] = None

class VideoVideoAlbumFull(VideoVideoAlbum):
	count:int
	image:Optional[list["VideoVideoImage"]] = None
	image_blur:Optional["BasePropertyExists"] = None
	is_system:Optional["BasePropertyExists"] = None
	updated_time:int

class VideoVideoFull(VideoVideo):
	files:Optional["VideoVideoFiles"] = None
	trailer:Optional["VideoVideoFiles"] = None
	live_settings:Optional["VideoLiveSettings"] = None

class VideoVideoImage(BaseImage):
	with_padding:Optional["BasePropertyExists"] = None

class WallWallpostFull(WallCarouselBase, WallWallpost):
	copy_history:Optional[list["WallWallpostFull"]] = None
	can_edit:Optional[bool] = None
	created_by:Optional[int] = None
	can_delete:Optional[bool] = None
	can_pin:Optional[bool] = None
	donut:Optional["WallWallpostDonut"] = None
	is_pinned:Optional[int] = None
	comments:Optional["BaseCommentsInfo"] = None
	marked_as_ads:Optional[bool] = None
	topic_id:Optional[int] = None
	short_text_rate:Optional[int] = None
	hash:Optional[str] = None

class MessagesUserXtrInvitedBy(UsersUserXtrType):
	invited_by:Optional[int] = None

class NewsfeedItemWallpost(NewsfeedItemBase, WallWallpostFull):
	feedback:Optional["NewsfeedItemWallpostFeedback"] = None

class GroupsUserXtrRole(UsersUserFull):
	role:Optional["GroupsRoleOptions"] = None

class FriendsUserXtrPhone(UsersUserFull):
	phone:Optional[str] = None

class NewsfeedItemDigestItem(WallWallpost):
	pass

class UsersSubscriptionsItem(UsersUserXtrType, GroupsGroupFull):
	pass

NewsfeedNewsfeedItem = NewType('NewsfeedNewsfeedItem', 
        Union[
            NewsfeedItemWallpost,
            NewsfeedItemPhoto,
            NewsfeedItemPhotoTag,
            NewsfeedItemFriend,
            NewsfeedItemAudio,
            NewsfeedItemVideo,
            NewsfeedItemTopic,
            NewsfeedItemDigest,
            NewsfeedItemPromoButton]
        )


for i in locals().copy().values():
    if isclass(i):
        if issubclass(i,BM):
            i.update_forward_refs()

__all__ = ('AccountAccountCounters', 'AccountInfo', 'AccountNameRequest', 'AccountNameRequestStatus', 'AccountOffer', 'AccountPushConversations', 'AccountPushConversationsItem', 'AccountPushParams', 'AccountPushParamsMode', 'AccountPushParamsOnoff', 'AccountPushParamsSettings', 'AccountPushSettings', 'AccountSubscriptions', 'AccountUserSettings', 'AccountUserSettingsInterest', 'AccountUserSettingsInterests', 'AddressesFields', 'AdsAccessRole', 'AdsAccessRolePublic', 'AdsAccesses', 'AdsAccount', 'AdsAccountType', 'AdsAd', 'AdsAdApproved', 'AdsAdCostType', 'AdsAdLayout', 'AdsAdStatus', 'AdsCampaign', 'AdsCampaignStatus', 'AdsCampaignType', 'AdsCategory', 'AdsClient', 'AdsCreateAdStatus', 'AdsCreateCampaignStatus', 'AdsCriteria', 'AdsCriteriaSex', 'AdsDemoStats', 'AdsDemostatsFormat', 'AdsFloodStats', 'AdsLinkStatus', 'AdsLookalikeRequest', 'AdsLookalikeRequestSaveAudienceLevel', 'AdsMusician', 'AdsObjectType', 'AdsParagraphs', 'AdsPromotedPostReach', 'AdsRejectReason', 'AdsRules', 'AdsStats', 'AdsStatsAge', 'AdsStatsCities', 'AdsStatsFormat', 'AdsStatsSex', 'AdsStatsSexAge', 'AdsStatsSexValue', 'AdsStatsViewsTimes', 'AdsTargSettings', 'AdsTargStats', 'AdsTargSuggestions', 'AdsTargSuggestionsCities', 'AdsTargSuggestionsRegions', 'AdsTargSuggestionsSchools', 'AdsTargSuggestionsSchoolsType', 'AdsTargetGroup', 'AdsUpdateOfficeUsersResult', 'AdsUserSpecification', 'AdsUserSpecificationCutted', 'AdsUsers', 'AdswebGetAdCategoriesResponseCategoriesCategory', 'AdswebGetAdUnitsResponseAdUnitsAdUnit', 'AdswebGetFraudHistoryResponseEntriesEntry', 'AdswebGetSitesResponseSitesSite', 'AdswebGetStatisticsResponseItemsItem', 'AppWidgetsPhoto', 'AppWidgetsPhotos', 'AppsApp', 'AppsAppLeaderboardType', 'AppsAppMin', 'AppsAppType', 'AppsCatalogList', 'AppsLeaderboard', 'AppsScope', 'AudioAudio', 'bool', 'BaseCity', 'BaseCommentsInfo', 'BaseCountry', 'BaseCropPhoto', 'BaseCropPhotoCrop', 'BaseCropPhotoRect', 'BaseError', 'BaseGeo', 'BaseGeoCoordinates', 'BaseGradientPoint', 'BaseImage', 'BaseLikes', 'BaseLikesInfo', 'BaseLink', 'BaseLinkApplication', 'BaseLinkApplicationStore', 'BaseLinkButton', 'BaseLinkButtonAction', 'BaseLinkButtonActionType', 'BaseLinkButtonStyle', 'BaseLinkProduct', 'BaseLinkProductCategory', 'BaseLinkProductStatus', 'BaseLinkRating', 'BaseMessageError', 'BaseObject', 'BaseObjectCount', 'BaseObjectWithName', 'BasePlace', 'BasePropertyExists', 'BaseRepostsInfo', 'BaseRequestParam', 'BaseSex', 'BaseSticker', 'BaseStickerAnimation', 'BaseStickerNew', 'BaseStickerOld', 'BaseStickersList', 'BaseUploadServer', 'BaseUserGroupFields', 'BaseUserId', 'BoardDefaultOrder', 'BoardTopic', 'BoardTopicComment', 'CallbackBase', 'CallbackBoardPostDelete', 'CallbackConfirmation', 'CallbackDonutMoneyWithdraw', 'CallbackDonutMoneyWithdrawError', 'CallbackDonutSubscriptionCancelled', 'CallbackDonutSubscriptionCreate', 'CallbackDonutSubscriptionExpired', 'CallbackDonutSubscriptionPriceChanged', 'CallbackDonutSubscriptionProlonged', 'CallbackGroupChangePhoto', 'CallbackGroupChangeSettings', 'CallbackGroupJoin', 'CallbackGroupJoinType', 'CallbackGroupLeave', 'CallbackGroupMarket', 'CallbackGroupOfficerRole', 'CallbackGroupOfficersEdit', 'CallbackGroupSettingsChanges', 'CallbackLikeAddRemove', 'CallbackMarketComment', 'CallbackMarketCommentDelete', 'CallbackMessageAllow', 'CallbackMessageAllowObject', 'CallbackMessageDeny', 'CallbackMessageEdit', 'CallbackMessageNew', 'CallbackMessageObject', 'CallbackMessageReply', 'CallbackPhotoComment', 'CallbackPhotoCommentDelete', 'CallbackPollVoteNew', 'CallbackQrScan', 'CallbackType', 'CallbackUserBlock', 'CallbackUserUnblock', 'CallbackVideoComment', 'CallbackVideoCommentDelete', 'CallbackWallCommentDelete', 'CallsCall', 'CallsEndState', 'CallsParticipants', 'ClientInfoForBots', 'CommentThread', 'DatabaseCity', 'DatabaseCityById', 'DatabaseFaculty', 'DatabaseRegion', 'DatabaseSchool', 'DatabaseStation', 'DatabaseUniversity', 'DocsDoc', 'DocsDocAttachmentType', 'DocsDocPreview', 'DocsDocPreviewAudioMsg', 'DocsDocPreviewGraffiti', 'DocsDocPreviewPhoto', 'DocsDocPreviewPhotoSizes', 'DocsDocPreviewVideo', 'DocsDocTypes', 'DonutDonatorSubscriptionInfo', 'EventsEventAttach', 'FaveBookmark', 'FaveBookmarkType', 'FavePage', 'FavePageType', 'FaveTag', 'FriendsFriendExtendedStatus', 'FriendsFriendStatus', 'FriendsFriendStatusStatus', 'FriendsFriendsList', 'FriendsMutualFriend', 'FriendsRequests', 'FriendsRequestsMutual', 'FriendsRequestsXtrMessage', 'FriendsUserXtrPhone', 'GiftsGift', 'GiftsGiftPrivacy', 'GiftsLayout', 'GroupsAddress', 'GroupsAddressTimetable', 'GroupsAddressTimetableDay', 'GroupsAddressWorkInfoStatus', 'GroupsAddressesInfo', 'GroupsBanInfo', 'GroupsBanInfoReason', 'GroupsBannedItem', 'GroupsCallbackServer', 'GroupsCallbackSettings', 'GroupsContactsItem', 'GroupsCountersGroup', 'GroupsCover', 'GroupsFields', 'GroupsFilter', 'GroupsGroup', 'GroupsGroupAccess', 'GroupsGroupAdminLevel', 'GroupsGroupAgeLimits', 'GroupsGroupAttach', 'GroupsGroupAudio', 'GroupsGroupBanInfo', 'GroupsGroupCategory', 'GroupsGroupCategoryFull', 'GroupsGroupCategoryType', 'GroupsGroupDocs', 'GroupsGroupFull', 'GroupsGroupFullAgeLimits', 'GroupsGroupFullMemberStatus', 'GroupsGroupFullSection', 'GroupsGroupIsClosed', 'GroupsGroupMarketCurrency', 'GroupsGroupPhotos', 'GroupsGroupPublicCategoryList', 'GroupsGroupRole', 'GroupsGroupSubject', 'GroupsGroupSuggestedPrivacy', 'GroupsGroupTag', 'GroupsGroupTopics', 'GroupsGroupType', 'GroupsGroupVideo', 'GroupsGroupWall', 'GroupsGroupWiki', 'GroupsGroupsArray', 'GroupsLinksItem', 'GroupsLiveCovers', 'GroupsLongPollEvents', 'GroupsLongPollServer', 'GroupsLongPollSettings', 'GroupsMarketInfo', 'GroupsMarketState', 'GroupsMemberRole', 'GroupsMemberRolePermission', 'GroupsMemberRoleStatus', 'GroupsMemberStatus', 'GroupsMemberStatusFull', 'GroupsOnlineStatus', 'GroupsOnlineStatusType', 'GroupsOwnerXtrBanInfo', 'GroupsOwnerXtrBanInfoType', 'GroupsPhotoSize', 'GroupsRoleOptions', 'GroupsSectionsListItem', 'GroupsSettingsTwitter', 'GroupsSubjectItem', 'GroupsTokenPermissionSetting', 'GroupsUserXtrRole', 'LeadFormsAnswer', 'LeadFormsAnswerItem', 'LeadFormsForm', 'LeadFormsLead', 'LeadFormsQuestionItem', 'LeadFormsQuestionItemOption', 'LikesType', 'LinkTargetObject', 'MarketCurrency', 'MarketMarketAlbum', 'MarketMarketCategory', 'MarketMarketCategoryNested', 'MarketMarketCategoryOld', 'MarketMarketCategoryTree', 'MarketMarketItem', 'MarketMarketItemAvailability', 'MarketMarketItemFull', 'MarketOrder', 'MarketOrderItem', 'MarketPrice', 'MarketSection', 'MarketServicesViewType', 'MessagesAudioMessage', 'MessagesChat', 'MessagesChatFull', 'MessagesChatPreview', 'MessagesChatPushSettings', 'MessagesChatRestrictions', 'MessagesChatSettings', 'MessagesChatSettingsAcl', 'MessagesChatSettingsPermissions', 'MessagesChatSettingsPhoto', 'MessagesChatSettingsState', 'MessagesConversation', 'MessagesConversationCanWrite', 'MessagesConversationMember', 'MessagesConversationPeer', 'MessagesConversationPeerType', 'MessagesConversationSortId', 'MessagesConversationWithMessage', 'MessagesForeignMessage', 'MessagesForward', 'MessagesGetConversationById', 'MessagesGetConversationByIdExtended', 'MessagesGetConversationMembers', 'MessagesGraffiti', 'MessagesHistoryAttachment', 'MessagesHistoryMessageAttachment', 'MessagesHistoryMessageAttachmentType', 'MessagesKeyboard', 'MessagesKeyboardButton', 'MessagesKeyboardButtonActionCallback', 'MessagesKeyboardButtonActionLocation', 'MessagesKeyboardButtonActionOpenApp', 'MessagesKeyboardButtonActionOpenLink', 'MessagesKeyboardButtonActionOpenPhoto', 'MessagesKeyboardButtonActionText', 'MessagesKeyboardButtonActionVkpay', 'MessagesKeyboardButtonPropertyAction', 'MessagesLastActivity', 'MessagesLongpollMessages', 'MessagesLongpollParams', 'MessagesMessage', 'MessagesMessageAction', 'MessagesMessageActionPhoto', 'MessagesMessageActionStatus', 'MessagesMessageAttachment', 'MessagesMessageAttachmentType', 'MessagesMessageRequestData', 'MessagesMessagesArray', 'MessagesOutReadBy', 'MessagesPinnedMessage', 'MessagesPushSettings', 'MessagesSendUserIdsResponseItem', 'MessagesTemplateActionTypeNames', 'MessagesUserXtrInvitedBy', 'NewsfeedCommentsFilters', 'NewsfeedIgnoreItemType', 'NewsfeedItemAudio', 'NewsfeedItemAudioAudio', 'NewsfeedItemBase', 'NewsfeedItemDigest', 'NewsfeedItemDigestButton', 'NewsfeedItemDigestFooter', 'NewsfeedItemDigestFullItem', 'NewsfeedItemDigestHeader', 'NewsfeedItemDigestItem', 'NewsfeedItemFriend', 'NewsfeedItemFriendFriends', 'NewsfeedItemHolidayRecommendationsBlockHeader', 'NewsfeedItemPhoto', 'NewsfeedItemPhotoPhotos', 'NewsfeedItemPhotoTag', 'NewsfeedItemPhotoTagPhotoTags', 'NewsfeedItemPromoButton', 'NewsfeedItemPromoButtonAction', 'NewsfeedItemPromoButtonImage', 'NewsfeedItemTopic', 'NewsfeedItemVideo', 'NewsfeedItemVideoVideo', 'NewsfeedItemWallpost', 'NewsfeedItemWallpostFeedback', 'NewsfeedItemWallpostFeedbackAnswer', 'NewsfeedItemWallpostFeedbackType', 'NewsfeedList', 'NewsfeedListFull', 'NewsfeedNewsfeedItem', 'NewsfeedNewsfeedItemType', 'NewsfeedNewsfeedPhoto', 'NotesNote', 'NotesNoteComment', 'NotificationsFeedback', 'NotificationsNotification', 'NotificationsNotificationItem', 'NotificationsNotificationParent', 'NotificationsNotificationsComment', 'NotificationsReply', 'NotificationsSendMessageError', 'NotificationsSendMessageItem', 'OauthError', 'OrdersAmount', 'OrdersAmountItem', 'OrdersOrder', 'OrdersSubscription', 'OwnerState', 'PagesPrivacySettings', 'PagesWikipage', 'PagesWikipageFull', 'PagesWikipageHistory', 'PhotosImage', 'PhotosImageType', 'PhotosPhoto', 'PhotosPhotoAlbum', 'PhotosPhotoAlbumFull', 'PhotosPhotoFalseable', 'PhotosPhotoFullXtrRealOffset', 'PhotosPhotoSizes', 'PhotosPhotoSizesType', 'PhotosPhotoTag', 'PhotosPhotoUpload', 'PhotosPhotoXtrRealOffset', 'PhotosPhotoXtrTagInfo', 'PhotosTagsSuggestionItem', 'PhotosTagsSuggestionItemButton', 'PodcastCover', 'PodcastExternalData', 'PollsAnswer', 'PollsBackground', 'PollsFriend', 'PollsPoll', 'PollsPollAnonymous', 'PollsVoters', 'PollsVotersUsers', 'PrettyCardsPrettyCard', 'PrettyCardsPrettyCardOrError', 'SearchHint', 'SearchHintSection', 'SearchHintType', 'SecureGiveEventStickerItem', 'SecureLevel', 'SecureSetCounterItem', 'SecureSmsNotification', 'SecureTokenChecked', 'SecureTransaction', 'StatsActivity', 'StatsCity', 'StatsCountry', 'StatsPeriod', 'StatsReach', 'StatsSexAge', 'StatsViews', 'StatsWallpostStat', 'StatusStatus', 'StickersImageSet', 'StorageValue', 'StoreProduct', 'StoreProductIcon', 'StoreStickersKeyword', 'StoreStickersKeywordSticker', 'StoreStickersKeywordStickers', 'StoriesClickableArea', 'StoriesClickableSticker', 'StoriesClickableStickers', 'StoriesFeedItem', 'StoriesPromoBlock', 'StoriesReplies', 'StoriesStatLine', 'StoriesStory', 'StoriesStoryLink', 'StoriesStoryStats', 'StoriesStoryStatsStat', 'StoriesStoryStatsState', 'StoriesStoryType', 'StoriesUploadLinkText', 'StoriesViewersItem', 'UsersCareer', 'UsersExports', 'UsersFields', 'UsersLastSeen', 'UsersMilitary', 'UsersOccupation', 'UsersOnlineInfo', 'UsersPersonal', 'UsersRelative', 'UsersSchool', 'UsersSubscriptionsItem', 'UsersUniversity', 'UsersUser', 'UsersUserConnections', 'UsersUserCounters', 'UsersUserFull', 'UsersUserMin', 'UsersUserRelation', 'UsersUserSettingsXtr', 'UsersUserType', 'UsersUserXtrType', 'UsersUsersArray', 'UtilsDomainResolved', 'UtilsDomainResolvedType', 'UtilsLastShortenedLink', 'UtilsLinkChecked', 'UtilsLinkCheckedStatus', 'UtilsLinkStats', 'UtilsLinkStatsExtended', 'UtilsShortLink', 'UtilsStats', 'UtilsStatsCity', 'UtilsStatsCountry', 'UtilsStatsExtended', 'UtilsStatsSexAge', 'VideoLiveInfo', 'VideoLiveSettings', 'VideoSaveResult', 'VideoVideo', 'VideoVideoAlbum', 'VideoVideoAlbumFull', 'VideoVideoFiles', 'VideoVideoFull', 'VideoVideoImage', 'WallAppPost', 'WallAttachedNote', 'WallCarouselBase', 'WallCommentAttachment', 'WallCommentAttachmentType', 'WallGeo', 'WallGetFilter', 'WallGraffiti', 'WallPostCopyright', 'WallPostSource', 'WallPostSourceType', 'WallPostType', 'WallPostedPhoto', 'WallViews', 'WallWallComment', 'WallWallCommentDonut', 'WallWallCommentDonutPlaceholder', 'WallWallpost', 'WallWallpostAttachment', 'WallWallpostAttachmentType', 'WallWallpostCommentsDonut', 'WallWallpostCommentsDonutPlaceholder', 'WallWallpostDonut', 'WallWallpostDonutPlaceholder', 'WallWallpostFull', 'WallWallpostToId', 'WidgetsCommentMedia', 'WidgetsCommentMediaType', 'WidgetsCommentReplies', 'WidgetsCommentRepliesItem', 'WidgetsWidgetComment', 'WidgetsWidgetLikes', 'WidgetsWidgetPage')
