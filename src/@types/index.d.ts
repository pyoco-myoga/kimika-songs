
export type Length = "full" | "short";

// live: セトリの決まったライブ
// known: チャレンジではない、一度やったことがあるような歌
// improvised: チャレンジなどの即興演奏
export type SingType = "live" | "known" | "improvised"

export interface Song {
    uuid: string;
    name: string;
    video: string;
    t: number;
    length?: Length;
    SingType?: SingType;
}

declare module "*/songs.json" {
    const value: {[artist: string]: Song[]};
    export = value;
}
