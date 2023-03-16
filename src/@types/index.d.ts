
export type Quality = "full" | "short";

export interface Song {
    name: string;
    id: string;
    t: number;
    quality?: Quality;
}

declare module "*/songs.json" {
    const value: {[artist: string]: Song[]};
    export = value;
}
