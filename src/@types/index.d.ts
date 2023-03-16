
export type Quality = "full" | "short";

export interface Song {
    uuid: string;
    name: string;
    video: string;
    t: number;
    quality?: Quality;
}

declare module "*/songs.json" {
    const value: {[artist: string]: Song[]};
    export = value;
}
