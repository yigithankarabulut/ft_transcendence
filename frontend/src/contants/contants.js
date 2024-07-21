const BASE_DOMAIN = window.location.origin.split('/')[2];
const BASE_URL = "https://" + BASE_DOMAIN;
export const changeUrlBase = BASE_URL + "/api/user/pwd/update";
export const changeUsernameUrl = BASE_URL + "/api/user/username";
export const userDetailUrl = BASE_URL + "/api/user/details";
export const updateUserUrl = BASE_URL + "/api/user/update";
export const pictureUrl = BASE_URL + "/bucket/image/serve";
export const avatarUpdateUrl = BASE_URL + "/bucket/image";
export const forgotpasswordUrl = BASE_URL + "/api/user/pwd/forgot";
export const userGetByIdUrl = BASE_URL + "/api/user/get/id";
export const requestsList = BASE_URL + "/api/friends/request";
export const acceptUrl = BASE_URL + "/api/friends/accept";
export const rejectUrl = BASE_URL + "/api/friends/reject";
export const friendList = BASE_URL + "/api/friends/list";
export const friendDelete = BASE_URL + "/api/friends/delete";
export const singleUserDetailUrl = BASE_URL + "/api/user/get/id";
export const gameDetailUrl = BASE_URL + "/api/game/list";
export const joinUrl = BASE_URL + "/api/game/join";
export const matchHistoryUrl = BASE_URL + "/api/game/history";
export const gameCreateUrl = BASE_URL + "/api/game/room";
export const registerUrl = BASE_URL + "/api/user/register";
export const loginUrl = BASE_URL + "/api/user/login";
export const IntraOAuthUrl = BASE_URL + "/api/auth/intra"
export const resetUrlBase = BASE_URL + "/api/user/pwd/change";
export const url = BASE_URL + "/api/user/2fa";
export const twofaUrl = BASE_URL + "/api/user/2fa";
export const searchUrl = BASE_URL + "/api/user/search";
export const friendAdd = BASE_URL + "/api/friends/add";
export const ValidateAccessToken = BASE_URL + "/api/auth/token/validate";
export const ValidateRefreshToken = BASE_URL + "/api/auth/token/refresh";

export const GamePlaySocketUrl = "wss://"+BASE_DOMAIN+"/ws/game/";
export const StatusServiceSocketUrl = "wss://"+BASE_DOMAIN+"/ws/status/";
