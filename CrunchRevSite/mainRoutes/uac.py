"""
2024 - 2025, Written by the CrunchRev Authors

Route module description: controls everything under "/universial-app-configuration/" path
"""

from __main__ import *

@app.route("/universal-app-configuration/v1/behaviors/app-policy/content", methods=settings["HTTPMethods"])
def get_apc():
    return jsonify({
        "ChatConversationHeaderGroupDetails": True,
        "ChatHeaderSearch": True,
        "ChatHeaderCreateChatGroup": True,
        "ChatHeaderHomeButton": False,
        "ChatHeaderNotifications": True,
        "ChatPlayTogether": True,
        "ChatShareGameToChatFromChat": True,
        "ChatTapConversationThumbnail": True,
        "ChatViewProfileOption": True,
        "GamesDropDownList": True,
        "UseNewDropDown": False,
        "GameDetailsMorePage": True,
        "GameDetailsShowGlobalCounters": True,
        "GameDetailsPlayWithFriends": True,
        "GameDetailsSubtitle": True,
        "GameInfoList": True,
        "GameInfoListDeveloper": True,
        "GamePlaysAndRatings": True,
        "GameInfoShowBadges": True,
        "GameInfoShowCreated": True,
        "GameInfoShowGamepasses": True,
        "GameInfoShowGenre": True,
        "GameInfoShowMaxPlayers": True,
        "GameInfoShowServers": True,
        "GameInfoShowUpdated": True,
        "GameReportingDisabled": False,
        "GamePlayerCounts": True,
        "GiftCardsEnabled": False,
        "Notifications": True,
        "OfficialStoreEnabled": False,
        "RecommendedGames": True,
        "SearchBar": True,
        "MorePageType": "More",
        "AboutPageType": "About",
        "FriendFinder": True,
        "SocialLinks": True,
        "SocialGroupLinks": True,
        "EnableShareCaptureCTA": True,
        "SiteMessageBanner": True,
        "UseWidthBasedFormFactorRule": False,
        "UseHomePageWithAvatarAndPanel": False,
        "UseBottomBar": True,
        "AvatarHeaderIcon": "LuaApp/icons/ic-back",
        "AvatarEditorShowBuyRobuxOnTopBar": True,
        "HomeIcon": "LuaApp/icons/ic-roblox-close",
        "ShowYouTubeAgeAlert": False,
        "GameDetailsShareButton": True,
        "CatalogShareButton": True,
        "AccountProviderName": "",
        "InviteFromAccountProvider": False,
        "ShareToAccountProvider": False,
        "ShareToAccountProviderTimeout": 8,
        "ShowDisplayName": True,
        "GamesPageCreationCenterTitle": False,
        "ShowShareTargetGameCreator": True,
        "SearchAutoComplete": True,
        "CatalogShow3dView": True,
        "CatalogReportingDisabled": False,
        "CatalogCommunityCreations": True,
        "CatalogPremiumCategory": True,
        "CatalogPremiumContent": True,
        "ItemDetailsFullView": True,
        "UseAvatarExperienceLandingPage": True,
        "HomePageFriendSection": True,
        "HomePageProfileLink": True,
        "PurchasePromptIncludingWarning": False,
        "ShowVideoThumbnails": True,
        "VideoSharingTestContent": [],
        "SystemBarPlacement": "Bottom",
        "EnableInGameHomeIcon": False,
        "UseExternalBrowserForDisclaimerLinks": False,
        "ShowExitFullscreenToast": True,
        "ExitFullscreenToastEnabled": False,
        "UseLuobuAuthentication": False,
        "CheckUserAgreementsUpdatedOnLogin": True,
        "AddUserAgreementIdsToSignupRequest": True,
        "UseOmniRecommendation": True,
        "ShowAgeVerificationOverlayEnabled": False,
        "ShouldShowGroupsTile": True,
        "ShowVoiceUpsell": False,
        "ProfileShareEnabled": True,
        "ContactImporterEnabled": True,
        "FriendCodeQrCodeScannerEnabled": False,
        "RealNamesInDisplayNamesEnabled": False,
        "CsatSurveyRestrictTextInput": False,
        "RobloxCreatedItemsCreatedByLuobu": False,
        "GameInfoShowChatFeatures": True,
        "PlatformGroup": "Unknown",
        "UsePhoneSearchDiscoverEntry": False,
        "HomeLocalFeedItems": {
            "UserInfo": 1,
            "FriendCarousel": 2
        },
        "Routes": {
            "auth": {
            "connect": "v2/login",
            "login": "v2/login",
            "signup": "v2/signup"
            }
        },
        "PromotionalEmailsCheckboxEnabled": True,
        "PromotionalEmailsOptInByDefault": False,
        "EnablePremiumUserFeatures": True,
        "CanShowUnifiedChatUpsell": True,
        "RequireExplicitVoiceConsent": True,
        "RequireExplicitAvatarVideoConsent": True,
        "EnableVoiceReportAbuseMenu": True
    }), 200

@app.route("/universal-app-configuration/v1/behaviors/app-patch/content", methods=settings["HTTPMethods"])
def get_ap():
    return jsonify({
        "SchemaVersion": "1",
        "CanaryUserIds": [],
        "CanaryPercentage": 0
    }), 200