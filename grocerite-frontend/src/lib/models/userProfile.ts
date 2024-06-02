export class UserProfile {
    idx: number;
    username: string;
    email: string;
    userId: string;
    fUid: string;
    nickname: string;
    picture?: string;
    householdIds: string[];

    constructor({
        idx = -1,
        username = '',
        email = '',
        userId = '',
        fUid = '',
        nickname = '',
        picture = '',
        householdIds = []
    } : {
        idx?: number,
        username?: string,
        userId?: string,
        email?: string,
        fUid?: string,
        nickname?: string,
        picture?: string,
        householdIds?: string[]
    } = {}) {
        this.idx = idx;
        this.username = username;
        this.userId = userId;
        this.email = email;
        this.fUid = fUid;
        this.nickname = nickname;
        this.picture = picture;
        this.householdIds = householdIds;
    }

    static fromJson(json: any): UserProfile {
        return new UserProfile({
            idx: json.idx,
            username: json.username,
            userId: json.userId,
            email: json.email,
            fUid: json.fUid,
            nickname: json.nickname,
            picture: json.picture,
            householdIds: json.householdIds
        });
    }
}